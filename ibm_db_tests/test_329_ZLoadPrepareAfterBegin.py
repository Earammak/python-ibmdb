#
#  Licensed Materials - Property of IBM
#

from __future__ import print_function

import unittest
from pathlib import Path

import ibm_db
from testfunctions import IbmDbTestFunctions

_DEL_FILE   = Path(__file__).parent / "data" / "block.cust.del"
_TABLE      = "ADMF001.CUSTOMER_LOCAL"
_CHUNK_SIZE = 10_000_000
_UTILITY_ID = "PYZLOAD329"


class IbmDbTestCase(unittest.TestCase):

    def test_329_ZLoadPrepareAfterBegin(self):
        if not hasattr(ibm_db, "zload_begin"):
            self.skipTest("zload APIs not available")

        if not _DEL_FILE.is_file():
            self.skipTest("data file not found: %s" % _DEL_FILE)

        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_329)

    def run_test_329(self):
        data_file = str(_DEL_FILE)

        load_stmt = (
            "TEMPLATE SORTIN DSN &JO..&ST..SORTIN.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "TEMPLATE SORTOUT DSN &JO..&ST..SORTOUT.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
            "REPLACE RESUME NO PREFORMAT LOG(NO) REUSE NOCOPYPEND "
            "FORMAT DELIMITED EBCDIC INTO TABLE %s NUMRECS 30000"
        ) % _TABLE

        print("BEGIN ZLOAD 329")

        conn = None
        stmt = None
        retcode = None
        bytes_sent = 0
        prepare_after_begin = "NO"

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

            if not ibm_db.zload_begin(stmt, load_stmt, _UTILITY_ID):
                print("RESULT FAIL")
                return

            try:
                tmp = ibm_db.prepare(conn, "select * from sysibm.sysdummy1")
                if tmp:
                    ibm_db.free_stmt(tmp)
                    prepare_after_begin = "YES"
            except Exception:
                prepare_after_begin = "NO"

            with open(data_file, "rb") as fh:
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

            print("PREPARE_AFTER_BEGIN: %s" % prepare_after_begin)
            print("BYTES_SENT: %d" % bytes_sent)
            print("RETURNCODE: %d" % int(retcode))
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
#BEGIN ZLOAD 329
#PREPARE_AFTER_BEGIN: %s
#BYTES_SENT: %d
#RETURNCODE: %d
#RESULT PASS
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
