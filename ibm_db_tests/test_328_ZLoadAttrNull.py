#
#  Licensed Materials - Property of IBM
#

from __future__ import print_function

import os
import unittest

import ibm_db
from testfunctions import IbmDbTestFunctions


class IbmDbTestCase(unittest.TestCase):

    def test_328_ZLoadAttrNull(self):
        if os.environ.get("ZLOAD_ENABLE_ATTR_NULL", "0") != "1":
            self.skipTest("Set ZLOAD_ENABLE_ATTR_NULL=1 to run this low-level attr-null test")

        if not hasattr(ibm_db, "SQL_ATTR_DB2ZLOAD_LOADSTMT"):
            self.skipTest("SQL_ATTR_DB2ZLOAD_LOADSTMT not exported")

        obj = IbmDbTestFunctions()
        obj.assert_expectf(self.run_test_328)

    def run_test_328(self):
        print("BEGIN ZLOAD 328")

        conn = None
        stmt = None
        rc = None

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

            rc = ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_DB2ZLOAD_LOADSTMT: None}, 0)
            print("SET_OPTION_RC: %d" % int(rc))
            print("RESULT PASS")

        except Exception:
            print("RESULT FAIL")

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
#BEGIN ZLOAD 328
#SET_OPTION_RC: %d
#RESULT PASS
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
