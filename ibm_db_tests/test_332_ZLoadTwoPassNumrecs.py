#
#  Licensed Materials - Property of IBM
#

from __future__ import print_function

import unittest
from pathlib import Path

import ibm_db
from testfunctions import IbmDbTestFunctions

_DEL_FILE    = Path(__file__).parent / "data" / "block.cust.del"
_TABLE       = "ADMF001.CUSTOMER_LOCAL"
_CHUNK_SIZE  = 10_000_000
_NUM_RECS1   = 30000
_NUM_RECS2   = 3000
_UTILITY_ID1 = "PYZL332A"
_UTILITY_ID2 = "PYZL332B"


class IbmDbTestCase(unittest.TestCase):

    def test_332_ZLoadTwoPassNumrecs(self):
        required_apis = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag")
        missing = [name for name in required_apis if not hasattr(ibm_db, name)]
        if missing:
            self.skipTest("Missing ZLOAD APIs: %s" % ", ".join(missing))

        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_332)

    def run_test_332(self):
        data_file = str(_DEL_FILE)

        print("BEGIN ZLOAD 332")

        load1 = (
            "TEMPLATE SORTIN DSN &JO..&ST..SORTIN.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "TEMPLATE SORTOUT DSN &JO..&ST..SORTOUT.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
            "REPLACE PREFORMAT LOG(NO) REUSE NOCOPYPEND "
            "FORMAT DELIMITED EBCDIC INTO TABLE %s NUMRECS %d"
        ) % (_TABLE, _NUM_RECS1)

        load2 = (
            "TEMPLATE SORTIN DSN &JO..&ST..SORTIN.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "TEMPLATE SORTOUT DSN &JO..&ST..SORTOUT.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
            "REPLACE PREFORMAT LOG(NO) REUSE NOCOPYPEND "
            "FORMAT DELIMITED EBCDIC INTO TABLE %s NUMRECS %d"
        ) % (_TABLE, _NUM_RECS2)

        conn = None
        s1 = None
        s2 = None
        s3 = None
        s4 = None
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

            s1 = ibm_db.prepare(conn, "VALUES 1")
            s2 = ibm_db.prepare(conn, "VALUES 2")
            if not s1 or not s2:
                print("RESULT FAIL")
                return

            if not ibm_db.zload_begin(s1, load1, _UTILITY_ID1):
                print("RESULT FAIL")
                return

            with open(data_file, "rb") as fh:
                while True:
                    chunk = fh.read(_CHUNK_SIZE)
                    if not chunk:
                        break
                    if not ibm_db.zload_put_data(s1, chunk):
                        print("RESULT FAIL")
                        return

            if not ibm_db.zload_end(s1):
                print("RESULT FAIL")
                return

            d1 = ibm_db.zload_get_diag(s1) or {}
            rc1 = d1.get("retcode")
            if rc1 is None or int(rc1) > 4:
                print("RESULT FAIL")
                return

            ibm_db.commit(conn)

            s3 = ibm_db.prepare(conn, "VALUES 3")
            s4 = ibm_db.prepare(conn, "VALUES 4")
            if not s3 or not s4:
                print("RESULT FAIL")
                return

            if not ibm_db.zload_begin(s3, load2, _UTILITY_ID2):
                print("RESULT FAIL")
                return

            with open(data_file, "rb") as fh:
                while True:
                    chunk = fh.read(_CHUNK_SIZE)
                    if not chunk:
                        break
                    if not ibm_db.zload_put_data(s3, chunk):
                        print("RESULT FAIL")
                        return

            if not ibm_db.zload_end(s3):
                print("RESULT FAIL")
                return

            d2 = ibm_db.zload_get_diag(s3) or {}
            rc2 = d2.get("retcode")
            if rc2 is None or int(rc2) > 4:
                print("RESULT FAIL")
                return

            print("RC1: %d" % int(rc1))
            print("RC2: %d" % int(rc2))
            print("RESULT PASS")

        finally:
            for s in (s4, s3, s2, s1):
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
#BEGIN ZLOAD 332
#%s
#RESULT %s
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
