#
#  Licensed Materials - Property of IBM
#

from __future__ import print_function

import unittest
from pathlib import Path

import ibm_db
from testfunctions import IbmDbTestFunctions

_SPANNED_FILE = Path(__file__).parent / "data" / "block.lcus.spanned"
_TABLE        = "ADMF001.LCUSTOMER"
_UTILITY_ID   = "fastload123"
_MSGFILE      = "run/zload03.out"
_CHUNK_SIZE   = 10_000_000
_NUM_RECS     = 3000

_LOAD_STMT = (
    "TEMPLATE SORTIN DSN &JO..&ST..SORTIN.T&TIME. "
    "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
    "TEMPLATE SORTOUT DSN &JO..&ST..SORTOUT.T&TIME. "
    "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
    "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN,SORTOUT) "
    "REPLACE RESUME NO PREFORMAT LOG(NO) REUSE NOCOPYPEND "
    "EBCDIC CCSID(00037,00000,00000) FORMAT SPANNED YES "
    "INTO TABLE %(tbl)s WHEN(00001:00002)=X'000C' "
    "NUMRECS %(n)d IGNOREFIELDS YES "
    "(C_ID POSITION(00003:00006) CHAR(00004), "
    "C_D_ID POSITION(00007:00008) CHAR(00002), "
    "C_W_ID POSITION(00009:00012) CHAR(00004), "
    "C_FIRST POSITION(00013:00028) CHAR(00016), "
    "C_MIDDLE POSITION(00029:00030) CHAR(00002), "
    "C_LAST POSITION(00031:00046) CHAR(00016), "
    "C_PHONE POSITION(00047:00062) CHAR(00016), "
    "C_SINCE POSITION(00063:00088) TIMESTAMP EXTERNAL(026), "
    "C_CREDIT POSITION(00089:00090) CHAR(00002), "
    "C_CREDIT_LIM POSITION(00091:00094) DECIMAL PACKED, "
    "C_DISCOUNT POSITION(00095:00097) DECIMAL PACKED, "
    "C_BALANCE POSITION(00098:00103) DECIMAL PACKED, "
    "C_YTD_PAYMENT POSITION(00104:00110) DECIMAL PACKED, "
    "C_PAYMENT_CNT POSITION(00111:00112) SMALLINT, "
    "C_DELIVERY_CNT POSITION(00113:00114) SMALLINT, "
    "C_STATE POSITION(00115:00116) CHAR(00002), "
    "C_ZIP POSITION(00117:00125) CHAR(00009), "
    "C_STREET_1 POSITION(00126) VARCHAR, "
    "C_STREET_2 POSITION(*) VARCHAR, "
    "C_CITY POSITION(*) VARCHAR, "
    "C_DATA POSITION(*) VARCHAR, "
    "DSN_NULL_IND_00022 POSITION(*) CHAR(1), "
    "C_AGREEMENT POSITION(*) CLOB NULLIF(DSN_NULL_IND_00022)=X'FF', "
    "DSN_NULL_IND_00023 POSITION(*) CHAR(1), "
    "C_CREDITCHECK POSITION(*) CLOB NULLIF(DSN_NULL_IND_00023)=X'FF')"
) % {"tbl": _TABLE, "n": _NUM_RECS}


class IbmDbTestCase(unittest.TestCase):

    def test_335_ZLoadSpanned(self):
        if not hasattr(ibm_db, "zload_begin"):
            self.skipTest("zload APIs not available")

        if not _SPANNED_FILE.is_file():
            self.skipTest("data file not found: %s" % _SPANNED_FILE)

        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_335)

    def run_test_335(self):
        print("BEGIN ZLOAD 335")
        print("TABLE: %s" % _TABLE)

        conn = None
        stmt = None
        verify_stmt = None
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

            with open(str(_SPANNED_FILE), "rb") as fh:
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
            messages = (diag.get("messages") or "")[:300]
            if retcode is None or int(retcode) > 4:
                if messages:
                    print("MESSAGES: %s" % messages)
                print("RESULT FAIL")
                return

            verify_stmt = ibm_db.exec_immediate(
                conn, "SELECT COUNT(*) FROM %s" % _TABLE
            )
            if verify_stmt:
                row = ibm_db.fetch_assoc(verify_stmt)
                if row:
                    rowcount = int(next(iter(row.values())))
                try:
                    ibm_db.free_result(verify_stmt)
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
#BEGIN ZLOAD 335
#TABLE: %s
#%s
#RESULT %s
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
