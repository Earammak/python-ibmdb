#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

from __future__ import print_function

import unittest
from pathlib import Path

import ibm_db
from testfunctions import IbmDbTestFunctions

_DEL_FILE   = Path(__file__).parent / "data" / "block.cust.del"
_TABLE      = "ADMF001.CUSTOMER_LOCAL2"
_SORT_HLQ   = "ADMF001.ZLOAD"
_CHUNK_SIZE = 10_000_000
_UTILITY_ID = "PYZLOAD325"
_NUM_RECS   = 30000


class IbmDbTestCase(unittest.TestCase):

    def test_325_ZLoadDelimitedAlt(self):
        if not hasattr(ibm_db, "zload_begin"):
            self.skipTest("zload APIs not available")

        if not _DEL_FILE.is_file():
            self.skipTest("data file not found: %s" % _DEL_FILE)

        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_325)

    def run_test_325(self):
        data_file = str(_DEL_FILE)

        load_stmt = (
            "TEMPLATE SORTIN DSN %s.SORTIN.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "TEMPLATE SORTOUT DSN %s.SORTOUT.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
            "REPLACE PREFORMAT LOG(NO) REUSE NOCOPYPEND "
            "FORMAT DELIMITED EBCDIC "
            "INTO TABLE %s NUMRECS %d"
        ) % (_SORT_HLQ, _SORT_HLQ, _TABLE, _NUM_RECS)

        print("BEGIN ZLOAD 325")
        print("TABLE: %s" % _TABLE)

        conn = None
        stmt = None
        verify_stmt = None
        bytes_sent = 0
        rowcount = -1
        retcode = None
        success = False

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
            if conn is None:
                print("RESULT FAIL")
                return

            stmt = ibm_db.prepare(conn, "VALUES 1")
            if not stmt:
                print("RESULT FAIL")
                return

            if not ibm_db.zload_begin(stmt, load_stmt, _UTILITY_ID):
                print("RESULT FAIL")
                return

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

            verify_stmt = ibm_db.exec_immediate(conn, "SELECT COUNT(*) FROM %s" % _TABLE)
            if verify_stmt:
                row = ibm_db.fetch_assoc(verify_stmt)
                if row:
                    rowcount = int(next(iter(row.values())))

            success = True

        finally:
            try:
                if verify_stmt:
                    ibm_db.free_result(verify_stmt)
            except Exception:
                pass
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

        print("BYTES_SENT: %d" % bytes_sent)
        print("RETURNCODE: %d" % int(retcode))
        print("ROWCOUNT: %d" % rowcount)
        print("RESULT PASS" if success else "RESULT FAIL")


if __name__ == "__main__":
    unittest.main()

#__END__
#__LUW_EXPECTED__
#
#__ZOS_EXPECTED__
#BEGIN ZLOAD 325
#TABLE: %s
#%s
#RESULT %s
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
