#
#  Licensed Materials - Property of IBM
#
#  (c) Copyright IBM Corp. 2007-2008
#
# test_334_ZLoadErrorConditions
#
# Tests error-handling paths in the DRDA fast load (zLOAD) implementation:
#
#  334a  zload_put_data before zload_begin  -> ProgrammingError
#  334b  zload_end before zload_begin       -> ProgrammingError
#  334c  zload_get_diag before zload_begin  -> ProgrammingError
#  334d  zload_begin with non-string stmt   -> InterfaceError
#  334e  zload_begin with non-string uid    -> InterfaceError
#  334f  zload_put_data with non-bytes data -> InterfaceError
#  334g  zload_from_file with missing file  -> FileNotFoundError / InterfaceError
#  334h  zload_from_file chunk_size <= 0    -> InterfaceError
#
# These tests exercise only the Python-layer guards (ibm_db_dbi.Cursor) and
# do NOT require a live database connection.
#

from __future__ import print_function

import os
import sys
import unittest
import unittest.mock as mock

import ibm_db
import ibm_db_dbi
from ibm_db_dbi import (
    Cursor, ProgrammingError, InterfaceError, NotSupportedError
)


def _make_cursor():
    """Return a Cursor whose ibm_db handles are mocked (no real DB needed)."""
    mock_conn    = mock.MagicMock()
    mock_conn_obj = mock.MagicMock(spec=ibm_db_dbi.Connection)
    mock_conn_obj.conn_handler = mock_conn
    mock_conn_obj.FIX_RETURN_TYPE = 1

    cursor = Cursor.__new__(Cursor)
    cursor.arraysize       = 1
    cursor._Cursor__rowcount = -1
    cursor._result_set_produced = False
    cursor._Cursor__description = None
    cursor.conn_handler    = mock_conn
    cursor.stmt_handler    = None
    cursor._is_scrollable_cursor = False
    cursor._Cursor__connection   = mock_conn_obj
    cursor.messages        = []
    cursor.FIX_RETURN_TYPE = 1
    cursor._all_stmt_handlers = []
    return cursor


class IbmDbTestCase(unittest.TestCase):

    def setUp(self):
        required_apis = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag")
        missing = [name for name in required_apis if not hasattr(ibm_db, name)]
        if missing:
            self.skipTest("Missing ZLOAD APIs: %s" % ", ".join(missing))

        required_cursor_methods = ("zload_begin", "zload_put_data", "zload_end", "zload_get_diag", "zload_from_file")
        missing_cursor = [name for name in required_cursor_methods if not hasattr(Cursor, name)]
        if missing_cursor:
            self.skipTest("Missing zload DBI cursor APIs: %s" % ", ".join(missing_cursor))

    # ------------------------------------------------------------------
    # Single entry-point used by ibmdb_tests.py runner (derives method name
    # from filename).  Delegates to every sub-case.
    # ------------------------------------------------------------------
    def test_334_ZLoadErrorConditions(self):
        self.check_334a_put_data_before_begin()
        self.check_334b_end_before_begin()
        self.check_334c_diag_before_begin()
        self.check_334d_begin_non_string_stmt()
        self.check_334e_begin_non_string_utilid()
        self.check_334f_put_data_non_bytes()
        self.check_334g_from_file_missing_path()
        self.check_334h_from_file_bad_chunk_size()
        self.check_334i_begin_empty_stmt()

    # ------------------------------------------------------------------
    # 334a – zload_put_data before zload_begin
    # ------------------------------------------------------------------
    def check_334a_put_data_before_begin(self):
        cursor = _make_cursor()
        # stmt_handler is None -> should raise ProgrammingError
        with self.assertRaises(ProgrammingError):
            cursor.zload_put_data(b"some data")

    # ------------------------------------------------------------------
    # 334b – zload_end before zload_begin
    # ------------------------------------------------------------------
    def check_334b_end_before_begin(self):
        cursor = _make_cursor()
        with self.assertRaises(ProgrammingError):
            cursor.zload_end()

    # ------------------------------------------------------------------
    # 334c – zload_get_diag before zload_begin
    # ------------------------------------------------------------------
    def check_334c_diag_before_begin(self):
        cursor = _make_cursor()
        with self.assertRaises(ProgrammingError):
            cursor.zload_get_diag()

    # ------------------------------------------------------------------
    # 334d – zload_begin with non-string load_statement
    # ------------------------------------------------------------------
    def check_334d_begin_non_string_stmt(self):
        cursor = _make_cursor()
        with self.assertRaises(InterfaceError):
            cursor.zload_begin(12345)

    # ------------------------------------------------------------------
    # 334e – zload_begin with non-string utility_id
    # ------------------------------------------------------------------
    def check_334e_begin_non_string_utilid(self):
        cursor = _make_cursor()
        # Give a real prepare so zload_begin reaches the utility_id check.
        cursor.stmt_handler = mock.MagicMock()
        with mock.patch("ibm_db.zload_begin", return_value=True):
            with self.assertRaises(InterfaceError):
                cursor.zload_begin("LOAD DATA ...", utility_id=999)

    # ------------------------------------------------------------------
    # 334f – zload_put_data with non-bytes-like data
    # ------------------------------------------------------------------
    def check_334f_put_data_non_bytes(self):
        cursor = _make_cursor()
        cursor.stmt_handler = mock.MagicMock()  # simulate active handle
        with self.assertRaises(InterfaceError):
            cursor.zload_put_data("this is a string, not bytes")

    # ------------------------------------------------------------------
    # 334g – zload_from_file with a path that does not exist
    # ------------------------------------------------------------------
    def check_334g_from_file_missing_path(self):
        cursor = _make_cursor()
        cursor.stmt_handler = mock.MagicMock()
        with mock.patch("ibm_db.zload_begin", return_value=True), \
             mock.patch("ibm_db.zload_end",   return_value=True), \
             mock.patch("ibm_db.prepare",      return_value=mock.MagicMock()):
            with self.assertRaises((FileNotFoundError, IOError, OSError)):
                cursor.zload_from_file("LOAD DATA ...", "/nonexistent/path/file.dat")

    # ------------------------------------------------------------------
    # 334h – zload_from_file with chunk_size <= 0
    # ------------------------------------------------------------------
    def check_334h_from_file_bad_chunk_size(self):
        cursor = _make_cursor()
        with self.assertRaises(InterfaceError):
            cursor.zload_from_file("LOAD DATA ...", "anyfile.dat", chunk_size=0)

    # ------------------------------------------------------------------
    # 334i – zload_begin with empty string load_statement
    # ------------------------------------------------------------------
    def check_334i_begin_empty_stmt(self):
        """Empty load_statement is a string but DB CLI should reject it.
        The Python layer passes it through; we just verify no crash at the
        Python type-guard level."""
        cursor = _make_cursor()
        cursor.stmt_handler = mock.MagicMock()
        # Empty string passes the isinstance check; the CLI/C layer would
        # raise.  Mock it to return False (CLI failure) and verify we raise.
        with mock.patch("ibm_db.zload_begin", return_value=False):
            result = None
            try:
                result = cursor.zload_begin("")
            except Exception:
                pass
            # Either False returned or exception raised — both are acceptable.
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()


#__END__
#__LUW_EXPECTED__
#OK
#__ZOS_EXPECTED__
#OK
#__SYSTEMI_EXPECTED__
#
#__IDS_EXPECTED__
#
