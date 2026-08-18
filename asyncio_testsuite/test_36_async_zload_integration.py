"""
test_36_async_zload_integration

Async integration test for DRDA fast load (zLOAD) via AsyncCursor.

Tests the full pipeline end-to-end through ibm_db_dbi.AsyncCursor:
  36a  AsyncCursor.zload_from_file  - streams a local file and checks retcode
  36b  Step-by-step async calls     - zload_begin / put_data / end / get_diag
  36c  Async error guard            - put_data before begin raises ProgrammingError

Skips automatically when:
  - zload APIs are absent from this ibm_db build
  - ibm_db_tests/data/block.cust.del does not exist
  - Running against a non-z/OS server (retcode > 4)
"""

import asyncio
import os
import unittest
import unittest.mock as mock
from pathlib import Path

import ibm_db
import ibm_db_dbi
from ibm_db_dbi import AsyncCursor, AsyncConnection, ProgrammingError


def _skip_unless_zload(method):
    def wrapper(self, *args, **kwargs):
        required_c_apis = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag")
        missing_c = [name for name in required_c_apis if not hasattr(ibm_db, name)]
        if missing_c:
            self.skipTest("Missing zload C APIs: %s" % ", ".join(missing_c))

        required_async_methods = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag", "zload_from_file")
        missing_async = [name for name in required_async_methods if not hasattr(AsyncCursor, name)]
        if missing_async:
            self.skipTest("Missing async zload DBI APIs: %s" % ", ".join(missing_async))

        return method(self, *args, **kwargs)
    return wrapper


_TABLE      = "ADMF001.CUSTOMER_LOCAL"
_SORT_HLQ   = "ADMF001.ZLOAD"
_CHUNK_SIZE = 10_000_000
_NUM_RECS   = 30000


def _load_statement():
    return (
        "TEMPLATE SORTIN DSN %(hlq)s.SORTIN.T&TIME. "
        "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
        "TEMPLATE SORTOUT DSN %(hlq)s.SORTOUT.T&TIME. "
        "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
        "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
        "REPLACE PREFORMAT LOG(NO) REUSE NOCOPYPEND "
        "FORMAT DELIMITED EBCDIC "
        "INTO TABLE %(tbl)s NUMRECS %(n)d"
    ) % {"hlq": _SORT_HLQ, "tbl": _TABLE, "n": _NUM_RECS}


class IbmDbTestCase(unittest.TestCase):

    # ------------------------------------------------------------------
    # Single entry-point used by ibmdb_tests.py runner (derives method
    # name from filename).  Delegates to every sub-case in order.
    # ------------------------------------------------------------------
    def test_36_async_zload_integration(self):
        self.run_36a()
        self.run_36b()
        self.run_36c()

    # ------------------------------------------------------------------
    # 36a  AsyncCursor.zload_from_file  (full pipeline)
    # ------------------------------------------------------------------
    @_skip_unless_zload
    def run_36a(self):
        data_file = str(Path(__file__).parent.parent / "ibm_db_tests" / "data" / "block.cust.del")
        if not Path(data_file).is_file():
            self.skipTest("data file not found: %s" % data_file)

        asyncio.run(self._run_36a(data_file))

    async def _run_36a(self, data_file):
        load_stmt = _load_statement()

        try:
            import config
            if getattr(config, "hostname", None):
                dsn = (
                    "DATABASE=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=TCPIP;UID=%s;PWD=%s;"
                    % (config.database, config.hostname, config.port,
                       config.user, config.password)
                )
                conn = await AsyncConnection.connect(dsn, "", "")
            else:
                conn = await AsyncConnection.connect(config.database, "", "")
        except Exception as exc:
            self.skipTest("Cannot connect: %s" % exc)
            return

        async with conn:
            cursor = await conn.cursor()
            async with cursor:
                try:
                    diag = await cursor.zload_from_file(
                        load_stmt,
                        data_file,
                        utility_id="PYZLOAD36A",
                        chunk_size=_CHUNK_SIZE,
                    )
                except ibm_db_dbi.NotSupportedError:
                    self.skipTest("zLOAD not supported on this server/build")
                    return

                retcode = diag.get("retcode") if diag else None
                self.assertIsNotNone(retcode, "zload_get_diag returned no retcode")
                self.assertLessEqual(
                    int(retcode), 4,
                    "zLOAD retcode %s indicates failure; messages=%s"
                    % (retcode, diag.get("messages") if diag else ""),
                )

                # Verify row presence
                await cursor.execute("SELECT COUNT(*) FROM %s" % _TABLE)
                row = await cursor.fetchone()
                self.assertIsNotNone(row)
                self.assertGreater(int(row[0]), 0, "No rows found after zLOAD")

                await conn.commit()

    # ------------------------------------------------------------------
    # 36b  Step-by-step async calls (begin / put_data / end / get_diag)
    # ------------------------------------------------------------------
    @_skip_unless_zload
    def run_36b(self):
        data_file = str(Path(__file__).parent.parent / "ibm_db_tests" / "data" / "block.cust.del")
        if not Path(data_file).is_file():
            self.skipTest("data file not found: %s" % data_file)

        asyncio.run(self._run_36b(data_file))

    async def _run_36b(self, data_file):
        load_stmt = _load_statement()

        try:
            import config
            if getattr(config, "hostname", None):
                dsn = (
                    "DATABASE=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=TCPIP;UID=%s;PWD=%s;"
                    % (config.database, config.hostname, config.port,
                       config.user, config.password)
                )
                conn = await AsyncConnection.connect(dsn, "", "")
            else:
                conn = await AsyncConnection.connect(config.database, "", "")
        except Exception as exc:
            self.skipTest("Cannot connect: %s" % exc)
            return

        async with conn:
            cursor = await conn.cursor()
            async with cursor:
                try:
                    ok = await cursor.zload_begin(load_stmt, "PYZLOAD36B")
                    self.assertTrue(ok, "zload_begin returned False")

                    bytes_sent = 0
                    with open(data_file, "rb") as fh:
                        while True:
                            chunk = fh.read(_CHUNK_SIZE)
                            if not chunk:
                                break
                            ok = await cursor.zload_put_data(chunk)
                            self.assertTrue(ok, "zload_put_data returned False")
                            bytes_sent += len(chunk)

                    self.assertGreater(bytes_sent, 0, "No bytes were sent")

                    ok = await cursor.zload_end()
                    self.assertTrue(ok, "zload_end returned False")

                    diag = await cursor.zload_get_diag()
                    retcode = diag.get("retcode") if diag else None
                    self.assertIsNotNone(retcode)
                    self.assertLessEqual(
                        int(retcode), 4,
                        "zLOAD retcode %s indicates failure; messages=%s"
                        % (retcode, diag.get("messages") if diag else ""),
                    )

                    await conn.commit()

                except ibm_db_dbi.NotSupportedError:
                    self.skipTest("zLOAD not supported on this server/build")

    # ------------------------------------------------------------------
    # 36c  Async guard: zload_put_data before zload_begin
    # ------------------------------------------------------------------
    @_skip_unless_zload
    def run_36c(self):
        asyncio.run(self._run_36c())

    async def _run_36c(self):
        # Build a mock sync cursor and wrap in AsyncCursor - no real DB needed.
        sync_cursor = mock.MagicMock(spec=ibm_db_dbi.Cursor)
        sync_cursor.stmt_handler = None

        def _raises(*a, **kw):
            raise ProgrammingError("zload_put_data called before zload_begin")
        sync_cursor.zload_put_data.side_effect = _raises

        async_cursor = AsyncCursor(sync_cursor)
        with self.assertRaises(ProgrammingError):
            await async_cursor.zload_put_data(b"data")


if __name__ == "__main__":
    unittest.main()


#__END__
#__LUW_EXPECTED__
#
#__ZOS_EXPECTED__
#test_36_async_zload_integration (test_36_async_zload_integration.IbmDbTestCase.test_36_async_zload_integration) ... ok
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#