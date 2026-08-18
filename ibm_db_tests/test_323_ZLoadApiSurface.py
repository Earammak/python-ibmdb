#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#

import unittest
import sys
import os
import ibm_db
import ibm_db_dbi


class IbmDbTestCase(unittest.TestCase):

    def test_323_ZLoadApiSurface(self):
        required_c_apis = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag")
        missing_c = [name for name in required_c_apis if not hasattr(ibm_db, name)]
        if missing_c:
            self.skipTest("Missing zload C APIs: %s" % ", ".join(missing_c))

        required_dbi = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag", "zload_from_file")
        missing_dbi = [name for name in required_dbi if not hasattr(ibm_db_dbi.Cursor, name)]
        if missing_dbi:
            self.skipTest("Missing zload DBI cursor APIs: %s" % ", ".join(missing_dbi))

        missing_async = [name for name in required_dbi if not hasattr(ibm_db_dbi.AsyncCursor, name)]
        if missing_async:
            self.skipTest("Missing zload async DBI APIs: %s" % ", ".join(missing_async))

        # Core C-extension APIs should always be exported.
        self.assertTrue(hasattr(ibm_db, "zload_begin"))
        self.assertTrue(hasattr(ibm_db, "zload_put_data"))
        self.assertTrue(hasattr(ibm_db, "zload_end"))
        self.assertTrue(hasattr(ibm_db, "zload_get_diag"))

        # DBI cursor wrappers should be present.
        self.assertTrue(hasattr(ibm_db_dbi.Cursor, "zload_begin"))
        self.assertTrue(hasattr(ibm_db_dbi.Cursor, "zload_put_data"))
        self.assertTrue(hasattr(ibm_db_dbi.Cursor, "zload_end"))
        self.assertTrue(hasattr(ibm_db_dbi.Cursor, "zload_get_diag"))
        self.assertTrue(hasattr(ibm_db_dbi.Cursor, "zload_from_file"))

        # Async DBI wrappers should also be present.
        self.assertTrue(hasattr(ibm_db_dbi.AsyncCursor, "zload_begin"))
        self.assertTrue(hasattr(ibm_db_dbi.AsyncCursor, "zload_put_data"))
        self.assertTrue(hasattr(ibm_db_dbi.AsyncCursor, "zload_end"))
        self.assertTrue(hasattr(ibm_db_dbi.AsyncCursor, "zload_get_diag"))
        self.assertTrue(hasattr(ibm_db_dbi.AsyncCursor, "zload_from_file"))

        # Constants are intentionally conditional on CLI headers,
        # but names must exist at DBI layer even when value is None.
        self.assertTrue(hasattr(ibm_db_dbi, "SQL_ATTR_DB2ZLOAD_LOADSTMT"))
        self.assertTrue(hasattr(ibm_db_dbi, "SQL_ATTR_DB2ZLOAD_UTILITYID"))
        self.assertTrue(hasattr(ibm_db_dbi, "SQL_ATTR_DB2ZLOAD_BEGIN"))
        self.assertTrue(hasattr(ibm_db_dbi, "SQL_ATTR_DB2ZLOAD_END"))
        self.assertTrue(hasattr(ibm_db_dbi, "SQL_DIAG_DB2ZLOAD_RETCODE"))
        self.assertTrue(hasattr(ibm_db_dbi, "SQL_DIAG_DB2ZLOAD_LOAD_MSGS"))


if __name__ == "__main__":
    unittest.main()


#__END__
#__LUW_EXPECTED__
#test_323_ZLoadApiSurface (test_323_ZLoadApiSurface.IbmDbTestCase.test_323_ZLoadApiSurface) ... ok
#__ZOS_EXPECTED__
#test_323_ZLoadApiSurface (test_323_ZLoadApiSurface.IbmDbTestCase.test_323_ZLoadApiSurface) ... ok
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
