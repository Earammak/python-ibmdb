#
#  Licensed Materials - Property of IBM
#

from __future__ import print_function

import unittest

import ibm_db
from testfunctions import IbmDbTestFunctions

_TABLE    = "ADMF001.CUSTOMER_LOCAL"
_NUM_RECS = 30000
_MSGFILE  = "run/zload330.out"


class IbmDbTestCase(unittest.TestCase):

    def test_330_ZLoadConnLevelAttrs(self):
        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_330)

    def run_test_330(self):
        table_name = _TABLE
        num_recs   = _NUM_RECS
        msg_file   = _MSGFILE

        attr_msgfile = getattr(ibm_db, "SQL_ATTR_DB2ZLOAD_MSGFILE", 3042)
        attr_loadstmt = getattr(ibm_db, "SQL_ATTR_DB2ZLOAD_LOADSTMT", 3037)

        load_stmt = (
            "TEMPLATE SORTIN DSN &JO..&ST..SORTIN.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "TEMPLATE SORTOUT DSN &JO..&ST..SORTOUT.T&TIME. "
            "SPACE(10,10) CYL DISP(NEW,DELETE,DELETE) "
            "LOAD DATA INDDN SYSCLIEN WORKDDN(SORTIN) "
            "REPLACE PREFORMAT LOG(NO) REUSE NOCOPYPEND "
            "FORMAT DELIMITED UNICODE INTO TABLE %s NUMRECS %d"
        ) % (table_name, num_recs)

        print("BEGIN ZLOAD 330")

        conn = None
        rc_msg = 0
        rc_load = 0

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

            rc_msg = ibm_db.set_option(conn, {attr_msgfile: msg_file}, 1)
            rc_load = ibm_db.set_option(conn, {attr_loadstmt: load_stmt}, 1)

            print("SET_MSGFILE_RC: %d" % int(rc_msg))
            print("SET_LOADSTMT_RC: %d" % int(rc_load))
            print("RESULT PASS")

        except Exception:
            print("RESULT FAIL")

        finally:
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
#BEGIN ZLOAD 330
#SET_MSGFILE_RC: %d
#SET_LOADSTMT_RC: %d
#RESULT PASS
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
