#
#  Licensed Materials - Property of IBM
#

from __future__ import print_function

import unittest
from pathlib import Path

import ibm_db
from testfunctions import IbmDbTestFunctions

_INT_FILE   = Path(__file__).parent / "data" / "block.cust.int"
_TABLE      = "ADMF001.CUSTOMER_LOCAL"
_UTILITY_ID = "fastload123"
_MSGFILE    = "run/zload02.out"
_CHUNK_SIZE = 10_000_000
_NUM_RECS   = 30000

_LOAD_STMT = (
    "TEMPLATE SORTIN DSN &JO..&ST..SORTIN.T&TIME. "
    "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
    "TEMPLATE SORTOUT DSN &JO..&ST..SORTOUT.T&TIME. "
    "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
    "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
    "REPLACE RESUME NO PREFORMAT LOG(NO) REUSE NOCOPYPEND "
    "FORMAT INTERNAL STATISTICS TABLE(%s) INDEX(ALL) COLUMN(ALL) "
    "INTO TABLE %s NUMRECS %d"
) % (_TABLE, _TABLE, _NUM_RECS)


class IbmDbTestCase(unittest.TestCase):

    def test_326_ZLoadInternal(self):
        if not hasattr(ibm_db, "zload_begin"):
            self.skipTest("zload APIs not available")

        if not _INT_FILE.is_file():
            self.skipTest("data file not found: %s" % _INT_FILE)

        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_326)

    def run_test_326(self):
        print("BEGIN ZLOAD 326")
        print("TABLE: %s" % _TABLE)

        conn = None
        stmt = None
        retcode = None
        bytes_sent = 0
        rowcount = -1

        try:
            import config
            if getattr(config, "hostname", None):
                dsn = (
                    "DATABASE=%s;HOSTNAME=%s;PORT=%s;PROTOCOL=TCPIP;UID=%s;PWD=%s;"
                    % (config.database, config.hostname, config.port,
                       config.user, config.password)
                )
                conn = ibm_db.connect(dsn, "", "")
            else:
                conn = ibm_db.connect(config.database, "", "")
            if not conn:
                print("RESULT FAIL")
                return

            stmt = ibm_db.prepare(conn, "VALUES 1")
            if not stmt:
                print("RESULT FAIL")
                return

            attr_msgfile = getattr(ibm_db, "SQL_ATTR_DB2ZLOAD_MSGFILE", None)
            if attr_msgfile:
                ibm_db.set_option(stmt, {attr_msgfile: _MSGFILE}, 0)

            if not ibm_db.zload_begin(stmt, _LOAD_STMT, _UTILITY_ID):
                print("RESULT FAIL")
                return

            with open(str(_INT_FILE), "rb") as fh:
                while True:
                    chunk = fh.read(_CHUNK_SIZE)
                    if not chunk:
                        break
                    bytes_sent += len(chunk)
                    if not ibm_db.zload_put_data(stmt, chunk):
                        print("RESULT FAIL")
                        return

            if not ibm_db.zload_end(stmt):
                print("RESULT FAIL")
                return

            diag = ibm_db.zload_get_diag(stmt) or {}
            retcode = diag.get("retcode")
            if retcode is None or int(retcode) > 4:
                print("RESULT FAIL")
                return

            verify = ibm_db.exec_immediate(conn, "SELECT COUNT(*) FROM %s" % _TABLE)
            if verify:
                row = ibm_db.fetch_assoc(verify)
                if row:
                    rowcount = int(next(iter(row.values())))
                try:
                    ibm_db.free_result(verify)
                except Exception:
                    pass

            print("BYTES_SENT: %d" % bytes_sent)
            print("RETURNCODE: %d" % int(retcode))
            print("ROWCOUNT: %d" % rowcount)
            print("RESULT PASS")

        finally:
            try:
                if stmt:
                    ibm_db.free_stmt(stmt)
            except Exception:
                pass
            try:
                if conn:
                    ibm_db.commit(conn)
                    ibm_db.close(conn)
            except Exception:
                pass


if __name__ == "__main__":
    unittest.main()

#__END__
#__LUW_EXPECTED__
#
#__ZOS_EXPECTED__
#BEGIN ZLOAD 326
#TABLE: %s
#BYTES_SENT: %d
#RETURNCODE: %d
#ROWCOUNT: %d
#RESULT PASS
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
