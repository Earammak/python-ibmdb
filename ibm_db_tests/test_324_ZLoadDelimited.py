#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2026-2027
#

from __future__ import print_function

import unittest
from pathlib import Path

import ibm_db
from testfunctions import IbmDbTestFunctions

_DEL_FILE   = Path(__file__).parent / "data" / "block.cust.del"
_TABLE      = "ADMF001.CUSTOMER_LOCAL1"
_SORT_HLQ   = "ADMF001.ZLOAD"
_CHUNK_SIZE = 10_000_000
_UTILITY_ID = "PYZLOAD324"
_NUM_RECS   = 30000


class IbmDbTestCase(unittest.TestCase):

    def test_324_ZLoadDelimited(self):
        required_apis = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag")
        missing = [name for name in required_apis if not hasattr(ibm_db, name)]
        if missing:
            self.skipTest("Missing ZLOAD APIs: %s" % ", ".join(missing))

        if not _DEL_FILE.is_file():
            self.skipTest("data file not found: %s" % _DEL_FILE)

        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_324)

    def run_test_324(self):
        data_file = str(_DEL_FILE)

        load_statement = (
            "TEMPLATE SORTIN DSN %s.SORTIN.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "TEMPLATE SORTOUT DSN %s.SORTOUT.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
            "REPLACE PREFORMAT LOG(NO) REUSE NOCOPYPEND "
            "FORMAT DELIMITED EBCDIC "
            "INTO TABLE %s NUMRECS %d"
        ) % (_SORT_HLQ, _SORT_HLQ, _TABLE, _NUM_RECS)

        print("BEGIN ZLOAD 324")
        print("TABLE: %s" % _TABLE)

        conn = None
        stmt1 = None
        stmt2 = None
        verify_stmt = None
        retcode = None
        record_count = -1
        bytes_sent = 0
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

            stmt1 = ibm_db.prepare(conn, "VALUES 1")
            stmt2 = ibm_db.prepare(conn, "SELECT COUNT(*) FROM %s" % _TABLE)
            if not stmt1 or not stmt2:
                print("RESULT FAIL")
                return

            ibm_db.zload_begin(stmt1, load_statement, _UTILITY_ID)

            with open(data_file, "rb") as file_handle:
                while True:
                    chunk = file_handle.read(_CHUNK_SIZE)
                    if not chunk:
                        break
                    bytes_sent += len(chunk)
                    if not ibm_db.zload_put_data(stmt1, chunk):
                        print("RESULT FAIL")
                        return
            print("BYTES_SENT: %d" % bytes_sent)

            if not ibm_db.zload_end(stmt1):
                print("RESULT FAIL")
                return

            diag = ibm_db.zload_get_diag(stmt1) or {}
            retcode = diag.get("retcode")
            print("RETURNCODE: %d" % int(retcode))

            if retcode is None:
                print("RESULT FAIL")
                return
            if int(retcode) > 4:
                print("RESULT FAIL")
                return

            verify_stmt = ibm_db.exec_immediate(conn, "SELECT COUNT(*) FROM %s" % _TABLE)
            if verify_stmt:
                row = ibm_db.fetch_assoc(verify_stmt)
                if row:
                    record_count = int(next(iter(row.values())))
            print("ROWCOUNT: %d" % record_count)

            success = True

        finally:
            try:
                if stmt1:
                    ibm_db.free_stmt(stmt1)
            except Exception:
                pass
            try:
                if stmt2:
                    ibm_db.free_stmt(stmt2)
            except Exception:
                pass
            try:
                if verify_stmt:
                    ibm_db.free_result(verify_stmt)
            except Exception:
                pass
            try:
                if conn:
                    ibm_db.commit(conn)
                    ibm_db.close(conn)
            except Exception:
                pass

        if success:
            print("RESULT PASS")
        else:
            print("RESULT FAIL")


if __name__ == "__main__":
    unittest.main(verbosity=2)

#__END__
#__LUW_EXPECTED__
#
#__ZOS_EXPECTED__
#BEGIN ZLOAD 324
#TABLE: %s
#%s
#RESULT %s
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
