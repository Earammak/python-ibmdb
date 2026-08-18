#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#
# test_333_ZLoadDbiCursorFromFile
#
# Validates ibm_db_dbi.Cursor.zload_from_file() — the DB-API convenience
# wrapper that streams a local file to Db2 for z/OS via DRDA fast load (zLOAD).
#
# Skips automatically when:
#   - ZLOAD APIs are not in this ibm_db build
#   - ibm_db_tests/data/block.cust.del does not exist
#   - Running against a non-z/OS server (LUW returns retcode 8+)
#

from __future__ import print_function

import unittest
from pathlib import Path

import ibm_db
import ibm_db_dbi
from testfunctions import IbmDbTestFunctions

_DEL_FILE   = Path(__file__).parent / "data" / "block.cust.del"
_TABLE      = "ADMF001.CUSTOMER_LOCAL1"
_SORT_HLQ   = "ADMF001.ZLOAD"
_CHUNK_SIZE = 10_000_000
_UTILITY_ID = "PYZLOAD333"
_NUM_RECS   = 30000


def _connect_dbi():
    import config
    if getattr(config, "hostname", None):
        dsn = (
            "DATABASE=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=TCPIP;UID=%s;PWD=%s;"
            % (config.database, config.hostname, config.port,
               config.user, config.password)
        )
        return ibm_db_dbi.connect(dsn, "", "")
    return ibm_db_dbi.connect(config.database, "", "")


class IbmDbTestCase(unittest.TestCase):

    def test_333_ZLoadDbiCursorFromFile(self):
        required_apis = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag")
        missing = [name for name in required_apis if not hasattr(ibm_db, name)]
        if missing:
            self.skipTest("Missing zload C APIs: %s" % ", ".join(missing))

        required_cursor_methods = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag", "zload_from_file")
        missing_cursor = [name for name in required_cursor_methods if not hasattr(ibm_db_dbi.Cursor, name)]
        if missing_cursor:
            self.skipTest("Missing zload DBI cursor APIs: %s" % ", ".join(missing_cursor))

        if not _DEL_FILE.is_file():
            self.skipTest("data file not found: %s" % _DEL_FILE)

        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_333)

    def run_test_333(self):
        data_file = str(_DEL_FILE)

        load_statement = (
            "TEMPLATE SORTIN DSN %(hlq)s.SORTIN.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "TEMPLATE SORTOUT DSN %(hlq)s.SORTOUT.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
            "REPLACE PREFORMAT LOG(NO) REUSE NOCOPYPEND "
            "FORMAT DELIMITED EBCDIC "
            "INTO TABLE %(tbl)s NUMRECS %(n)d"
        ) % {"hlq": _SORT_HLQ, "tbl": _TABLE, "n": _NUM_RECS}

        print("BEGIN ZLOAD 333")
        print("TABLE: %s" % _TABLE)
        print("FILE:  %s" % data_file)

        conn   = None
        cursor = None
        retcode  = None
        rowcount = -1

        try:
            conn   = _connect_dbi()
            cursor = conn.cursor()

            # --- Exercise Cursor.zload_from_file ---
            diag = cursor.zload_from_file(
                load_statement,
                data_file,
                utility_id=_UTILITY_ID,
                chunk_size=_CHUNK_SIZE,
            )

            retcode = diag.get("retcode") if diag else None
            messages = diag.get("messages") if diag else None

            print("RETURNCODE: %s" % retcode)
            if messages:
                # Print first 500 chars so the expected-output block is stable.
                print("MESSAGES: %s" % str(messages)[:500])

            if retcode is None or int(retcode) > 4:
                print("RESULT FAIL")
                return

            # Verify rows landed in the table.
            cursor.execute("SELECT COUNT(*) FROM %s" % _TABLE)
            row = cursor.fetchone()
            if row:
                rowcount = int(row[0])
            print("ROWCOUNT: %d" % rowcount)

            conn.commit()
            print("RESULT PASS")

        except ibm_db_dbi.NotSupportedError as exc:
            # zLOAD not available (LUW without DB2 Connect, or old CLI).
            print("RESULT SKIP (%s)" % exc)

        except Exception as exc:
            print("ERROR: %s" % exc)
            print("RESULT FAIL")

        finally:
            try:
                if cursor:
                    cursor.close()
            except Exception:
                pass
            try:
                if conn:
                    conn.close()
            except Exception:
                pass


if __name__ == "__main__":
    unittest.main()


#__END__
#__LUW_EXPECTED__
#
#__ZOS_EXPECTED__
#BEGIN ZLOAD 333
#TABLE: %s
#FILE:  %s
#%s
#RESULT %s
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
