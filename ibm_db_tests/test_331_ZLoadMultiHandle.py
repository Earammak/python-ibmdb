#
#  Licensed Materials - Property of IBM
#

from __future__ import print_function

import unittest
from pathlib import Path

import ibm_db
from testfunctions import IbmDbTestFunctions

_DATA_DIR   = Path(__file__).parent / "data"
_TABLE      = "ADMF001.CUSTOMER_LOCAL"
_CHUNK_SIZE = 10_000_000
_UTILITY_ID1 = "PYZL331A"
_UTILITY_ID2 = "PYZL331B"


class IbmDbTestCase(unittest.TestCase):

    def test_331_ZLoadMultiHandle(self):
        required_apis = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag")
        missing = [name for name in required_apis if not hasattr(ibm_db, name)]
        if missing:
            self.skipTest("Missing ZLOAD APIs: %s" % ", ".join(missing))

        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_331)

    def run_test_331(self):
        del_file = str(_DATA_DIR / "block.cust.del")
        int_file = str(_DATA_DIR / "block.cust.int")

        print("BEGIN ZLOAD 331")

        load_del = (
            "TEMPLATE SORTIN DSN &JO..&ST..SORTIN.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "TEMPLATE SORTOUT DSN &JO..&ST..SORTOUT.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
            "REPLACE PREFORMAT LOG(NO) REUSE NOCOPYPEND "
            "FORMAT DELIMITED EBCDIC INTO TABLE %s NUMRECS 30000"
        ) % _TABLE

        load_int = (
            "TEMPLATE SORTIN DSN &JO..&ST..SORTIN.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "TEMPLATE SORTOUT DSN &JO..&ST..SORTOUT.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
            "REPLACE RESUME NO PREFORMAT LOG(NO) REUSE NOCOPYPEND "
            "FORMAT INTERNAL STATISTICS TABLE(%s) INDEX(ALL) COLUMN(ALL) "
            "INTO TABLE %s NUMRECS 30000"
        ) % (_TABLE, _TABLE)

        conn = None
        stmt1 = None
        stmt2 = None
        stmt3 = None
        stmt4 = None
        rc1 = None
        rc2 = None

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

            stmt1 = ibm_db.prepare(conn, "VALUES 1")
            stmt2 = ibm_db.prepare(conn, "VALUES 2")
            if not stmt1 or not stmt2:
                print("RESULT FAIL")
                return

            if not ibm_db.zload_begin(stmt1, load_del, _UTILITY_ID1):
                print("RESULT FAIL")
                return

            with open(del_file, "rb") as fh:
                while True:
                    chunk = fh.read(_CHUNK_SIZE)
                    if not chunk:
                        break
                    if not ibm_db.zload_put_data(stmt1, chunk):
                        print("RESULT FAIL")
                        return

            if not ibm_db.zload_end(stmt1):
                print("RESULT FAIL")
                return

            d1 = ibm_db.zload_get_diag(stmt1) or {}
            rc1 = d1.get("retcode")
            if rc1 is None or int(rc1) > 4:
                print("RESULT FAIL")
                return

            del_stmt = ibm_db.exec_immediate(conn, "DELETE FROM %s" % _TABLE)
            if del_stmt:
                ibm_db.free_stmt(del_stmt)
            ibm_db.commit(conn)

            stmt3 = ibm_db.prepare(conn, "VALUES 3")
            stmt4 = ibm_db.prepare(conn, "VALUES 4")
            if not stmt3 or not stmt4:
                print("RESULT FAIL")
                return

            if not ibm_db.zload_begin(stmt3, load_int, _UTILITY_ID2):
                print("RESULT FAIL")
                return

            with open(int_file, "rb") as fh:
                while True:
                    chunk = fh.read(_CHUNK_SIZE)
                    if not chunk:
                        break
                    if not ibm_db.zload_put_data(stmt3, chunk):
                        print("RESULT FAIL")
                        return

            if not ibm_db.zload_end(stmt3):
                print("RESULT FAIL")
                return

            d2 = ibm_db.zload_get_diag(stmt3) or {}
            rc2 = d2.get("retcode")
            if rc2 is None or int(rc2) > 4:
                print("RESULT FAIL")
                return

            print("RC1: %d" % int(rc1))
            print("RC2: %d" % int(rc2))
            print("RESULT PASS")

        finally:
            for s in (stmt4, stmt3, stmt2, stmt1):
                try:
                    if s:
                        ibm_db.free_stmt(s)
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
#BEGIN ZLOAD 331
#%s
#RESULT %s
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
