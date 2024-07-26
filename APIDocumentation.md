API description of ibm_db driver is given below. If you want to access the same for ibm_db_dbi wrapper, please visit [Python Database API Specification v2.0](http://www.python.org/dev/peps/pep-0249/)

# API Description for the ibm_db driver #

Table of Contents
-----------------
* [ibm_db.active](#ibm_dbactive)
* [ibm_db.autocommit](#ibm_dbautocommit)
* [ibm_db.bind_param](#ibm_dbbind_param)
* [ibm_db.callproc](#ibm_dbcallproc)
* [ibm_db.client_info](#ibm_dbclient_info)
* [ibm_db.close](#ibm_dbclose)
* [ibm_db.column_privileges](#ibm_dbcolumn_privileges)
* [ibm_db.columns](#ibm_dbcolumns)
* [ibm_db.commit](#ibm_dbcommit)
* [ibm_db.conn_error](#ibm_dbconn_error)
* [ibm_db.conn_errormsg](#ibm_dbconn_errormsg)
* [ibm_db.connect](#ibm_dbconnect)
* [ibm_db.createdb](#ibm_dbcreatedb)
* [ibm_db.createdbNX](#ibm_dbcreatedbNX)
* [ibm_db.cursor_type](#ibm_dbcursor_type)
* [ibm_db.dropdb](#ibm_dbdropdb)
* [ibm_db.exec_immediate](#ibm_dbexec_immediate)
* [ibm_db.execute](#ibm_dbexecute)
* [ibm_db.execute_many](#ibm_dbexecute_many)
* [ibm_db.fetch_tuple](#ibm_dbfetch_tuple)
* [ibm_db.fetch_assoc](#ibm_dbfetch_assoc)
* [ibm_db.fetch_both](#ibm_dbfetch_both)
* [ibm_db.fetch_row](#ibm_dbfetch_row)
* [ibm_db.field_display_size](#ibm_dbfield_display_size)
* [ibm_db.field_name](#ibm_dbfield_name)
* [ibm_db.field_num](#ibm_dbfield_num)
* [ibm_db.field_precision](#ibm_dbfield_precision)
* [ibm_db.field_scale](#ibm_dbfield_scale)
* [ibm_db.field_type](#ibm_dbfield_type)
* [ibm_db.field_width](#ibm_dbfield_width)
* [ibm_db.foreign_keys](#ibm_dbforeign_keys)
* [ibm_db.free_result](#ibm_dbfree_result)
* [ibm_db.free_stmt](#ibm_dbfree_stmt)
* [ibm_db.get_option](#ibm_dbget_option)
* [ibm_db.next_result](#ibm_dbnext_result)
* [ibm_db.num_fields](#ibm_dbnum_fields)
* [ibm_db.num_rows](#ibm_dbnum_rows)
* [ibm_db.pconnect](#ibm_dbpconnect)
* [ibm_db.prepare](#ibm_dbprepare)
* [ibm_db.primary_keys](#ibm_dbprimary_keys)
* [ibm_db.procedure_columns](#ibm_dbprocedure_columns)
* [ibm_db.procedures](#ibm_dbprocedures)
* [ibm_db.recreatedb](#ibm_dbrecreatedb)
* [ibm_db.result](#ibm_dbresult)
* [ibm_db.rollback](#ibm_dbrollback)
* [ibm_db.server_info](#ibm_dbserver_info)
* [ibm_db.set_option](#ibm_dbset_option)
* [ibm_db.special_columns](#ibm_dbspecial_columns)
* [ibm_db.statistics](#ibm_dbstatistics)
* [ibm_db.stmt_error](#ibm_dbstmt_error)
* [ibm_db.stmt_errormsg](#ibm_dbstmt_errormsg)
* [ibm_db.table_privileges](#ibm_dbtable_privileges)
* [ibm_db.tables](#ibm_dbtables)
* Context manager support with connection object

### ibm_db.active ###
`bool ibm_db.active(IBM_DBConnection connection)`

**Description**

Checks if the specified IBM_DBConnection is active.

**Parameters**
* connection - A valid IBM_DBConnection

**Return Values**
* `True` - the resource is active
* `False` - the resource is not active

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')
connState = ibm_db.active(conn)
print(connState)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-active.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_116_ConnActive.py)

### ibm_db.autocommit ###
`mixed ibm_db.autocommit ( IBM_DBConnection connection [, bool value] )`

**Description**

Returns and sets the AUTOCOMMIT behavior of the specified IBM_DBConnection.

**Parameters**
* connection - A valid IBM_DBConnection
* value - One of the following constants:
    * `SQL_AUTOCOMMIT_OFF`
    * `SQL_AUTOCOMMIT_ON`

**Return Values**
* When `value` is not passed:
    * `0` - AUTOCOMMIT is off
    * `1` - AUTOCOMMIT is on
* When `value` is passed:
    * `True` - AUTOCOMMIT was set to `value` successfully
    * `False` - AUTOCOMMIT was not set to `value` successfully

**Example**
```python
import ibm_db
options = { ibm_db.SQL_ATTR_AUTOCOMMIT:  ibm_db.SQL_AUTOCOMMIT_ON }
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','', options)
autocommitstatus = ibm_db.autocommit(conn)
print(autocommitstatus)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-autocommit.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_051_SetAutocommit_01.py)

### ibm_db.bind_param ###
`bool ibm_db.bind_param (IBM_DBStatement stmt, int parameter-number, string variable [, int parameter-type [, int data-type [, int precision [, int scale [, int size]]]]] )`

**Description**

Binds a Python variable to an SQL statement parameter in an IBM_DBStatement returned by ibm_db.prepare().
This function gives you more control over the parameter type, data type,
precision, and scale for the parameter than simply passing the variable as
part of the optional input tuple to ibm_db.execute().

**Parameters**
* stmt - A prepared statement returned from ibm_db.prepare()
* parameter-number - The 1-indexed position of the parameter in the prepared statement
* variable - A Python variable to bind to the parameter specified by parameter-number
* parameter-type - A constant specifying the parameter input/output type:
    * `SQL_PARAM_INPUT` - an input-only parameter
    * `SQL_PARAM_OUTPUT` - an output-only parameter
    * `SQL_PARAM_INPUT_OUTPUT` - the parameter is used for both input and output
    * `PARAM_FILE` - The data is stored in the file name specified in `variable` instead of in `variable` itself. This can be used to avoid storing lots of LOB data in memory.
* data-type - A constant specifying the SQL data type that the Python variable should be bound as:
    * `SQL_BINARY`
    * `DB2_CHAR`
    * `DB2_DOUBLE`
    * `DB2_LONG`
* precision - The precision of the variable
* scale - The scale of the variable

**Return Values**
* `True` - the bind succeeded
* `None` - the bind failed

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')
stmt=ibm_db.prepare(conn, "select * from tabmany where id=?")
id=1
ibm_db.bind_param(stmt, 1,id)
ibm_db.execute(stmt)
row=ibm_db.fetch_tuple(stmt)
print(row)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-bind_param.py),
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_140_BindParamSelectStmt.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_141_BindParamSelectStmtMultipleParams_01.py),
[Example4](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_142_BindParamSelectStmtMultipleParams_02.py),
[Example5](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_144_BindParamInsertStmtPARAM_FILE.py),
[Example6](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_145_BindRetrieveNoneEmptyString.py)

### ibm_db.callproc ###
`( IBM_DBStatement [, ...] ) ibm_db.callproc( IBM_DBConnection connection, string procname [, parameters] )`

**Description**

Calls a stored procedure with the given name. The parameters tuple must contain one entry for each argument (IN/OUT/INOUT) that the procedure expects. Returns an IBM_DBStatement containing result sets and modified copy of the input parameters. IN parameters are left untouched whereas INOUT/OUT parameters are possibly replaced by new values.

A call to a stored procedure may return zero or more result sets. You can retrieve a row as a tuple/dict from the IBM_DBStatement using ibm_db.fetch_assoc(), ibm_db.fetch_both(), or ibm_db.fetch_tuple(). Alternatively, you can use ibm_db.fetch_row() to move the result set pointer to next row and fetch a column at a time with ibm_db.result().

Samples for the API usage can be referred from test_146_CallSPINAndOUTParams.py, test_148_CallSPDiffBindPattern_01.py or test_52949_TestSPIntVarcharXml.py.

**Parameters**
* connection - A valid IBM_DBConnection
* procname - A valid strored procedure name
* parameters - A tuple containing as many parameters as required by the stored procedure.


**Return Values**
* On success, 
    * A tuple containing an IBM_DBStatement object followed by the parameters passed to the procedure, if any. 
    * Or an IBM_DBStatement object if there are no parameters passed to procedure
* On failure, the value `None`

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql="""create or replace procedure proc(OUT out1 integer) dynamic result sets 1 begin  select id into out1 from tabmany where id=1; end"""
ibm_db.exec_immediate(conn, sql)
out1 = 0
stmt, out1=ibm_db.callproc(conn,'proc',(out1,))
print(out1)

result = ibm_db.exec_immediate(conn, """CREATE PROCEDURE out_blob(IN P1 BLOB(100),OUT P2 BLOB(100)) LANGUAGE SQL DYNAMIC RESULT SETS 0 BEGIN SET P2 = P1; END""")
stmt, blob1, blob2 = ibm_db.callproc(conn, 'out_blob', (b'1234',b'0'))

if stmt is not None:
    print("Values of bound parameters _after_ CALL:")
    print("  1: %s\t 2: %s \n" % (blob1, blob2))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-callproc.py),
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_148_CallSPDiffBindPattern_01.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_146_CallSPINAndOUTParams.py),
[Example4](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_SPInOutBlob.py),
[Example5](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_bool_callproc.py)

### ibm_db.client_info ###
`object ibm_db.client_info ( IBM_DBConnection connection )`

**Description**

Returns a read-only object with information about the database client.

**Parameters**
* connection - A valid IBM_DBConnection returned from ibm_db.connect() or ibm_db.pconnect()

**Return Values**
* On success, an object with the following fields:
    * APPL_CODEPAGE - The application code page
    * CONN_CODEPAGE - The code page for the current connection
    * DATA_SOURCE_NAME - The data source name (DSN) used to create the current connection to the database
    * DRIVER_NAME - The name of the library that implements the Call Level Interface (CLI) specification
    * DRIVER_ODBC_VER - The version of ODBC that the IBM Data Server client supports. This returns a string "MM.mm" where MM is the major version and mm is the minor version. The IBM Data Server client always returns "03.51"
    * DRIVER_VER - The version of the client, in the form of a string "MM.mm.uuuu" where MM is the major version, mm is the minor version, and uuuu is the update. For example, "08.02.0001" represents major version 8, minor version 2, update 1.
    * ODBC_SQL_CONFORMANCE - There are three levels of ODBC SQL grammar supported by the client:
        * MINIMAL - Supports the minimum ODBC SQL grammar
        * CORE - Supports the core ODBC SQL grammar
        * EXTENDED - Supports extended ODBC SQL grammar
    * ODBC_VER - The version of ODBC that the ODBC driver manager supports. This returns a string "MM.mm.rrrr" where MM is the major version, mm is the minor version, and rrrr is the release. The client always returns "03.01.0000"
* On failure, `False`

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')
clientinfo = ibm_db.client_info(conn)
if client:
    print("DRIVER_NAME: string(%d) \"%s\"" % (len(client.DRIVER_NAME), client.DRIVER_NAME))
    print("DRIVER_VER: string(%d) \"%s\"" % (len(client.DRIVER_VER), client.DRIVER_VER))
    print("DATA_SOURCE_NAME: string(%d) \"%s\"" % (len(client.DATA_SOURCE_NAME), client.DATA_SOURCE_NAME))
    print("DRIVER_ODBC_VER: string(%d) \"%s\"" % (len(client.DRIVER_ODBC_VER), client.DRIVER_ODBC_VER))
    print("ODBC_VER: string(%d) \"%s\"" % (len(client.ODBC_VER), client.ODBC_VER))
    print("ODBC_SQL_CONFORMANCE: string(%d) \"%s\"" % (len(client.ODBC_SQL_CONFORMANCE), client.ODBC_SQL_CONFORMANCE))
    print("APPL_CODEPAGE: int(%s)" % client.APPL_CODEPAGE)
    print("CONN_CODEPAGE: int(%s)" % client.CONN_CODEPAGE)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-client_info.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/IBM_DB/ibm_db/ibm_db_tests/test_310_ClientInfo.py)

### ibm_db.close ###
`bool ibm_db.close ( IBM_DBConnection connection )`

**Description**

Closes a DB2 client connection and returns the corresponding resources to the database server.

If you attempt to close a persistent DB2 client connection created with
ibm_db.pconnect(), the connection is returned to the pool for the next caller of ibm_db.pconnect() to use.

**Parameters**
* connection - A valid IBM_DBConnection

**Return Values**

Returns `True` on success or `False` on failure.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

rc = ibm_db.close(conn)
print(rc)
```
Other Examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-close.py),
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_070_Close.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_071_CloseSuccess.py)


### ibm_db.column_privileges ###
`IBM_DBStatement ibm_db.column_privileges ( IBM_DBConnection connection [, string qualifier [, string schema [, string table-name [, string column-name]]]] )`

**Description**

Returns a result set listing the columns and associated privileges for a table.

**Parameters**
* connection - A valid IBM_DBConnection
* qualifier - A qualifier for DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* schema - The schema which contains the tables. To match all schemas, pass `None` or an empty string.
* table-name - The name of the table or view. To match all tables in the database, pass `None` or an empty string.
* column-name - The name of the column. To match all columns in the table, pass `None` or an empty string.

**Return Values**

An IBM_DBStatement with a result set containing rows with the following columns:
* TABLE_CAT - Name of the catalog. The value is `None` if the database does not have catalogs.
* TABLE_SCHEM - Name of the schema.
* TABLE_NAME - Name of the table or view.
* COLUMN_NAME - Name of the column.
* GRANTOR - Authorization ID of the user who granted the privilege.
* GRANTEE - Authorization ID of the user to whom the privilege was granted.
* PRIVILEGE - The privilege for the column.
* IS_GRANTABLE - Whether the GRANTEE is permitted to grant this privilege to other users.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

# ANIMAL is the table name
stmt = ibm_db.column_privileges(conn, None, None, 'ANIMALS')
row = ibm_db.fetch_tuple(stmt)
if row:
    print(row[0])
    print(row[1])
    print(row[2])
    print(row[3])
    print(row[4])
    print(row[5])
    print(row[6])
    print(row[7])

ibm_db.close(conn)
```

**Example**
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-column_privileges.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_023_ColumnPrivileges.py)

### ibm_db.columns ###
`IBM_DBStatement ibm_db.columns ( IBM_DBConnection connection [, string qualifier [, string schema [, string table-name [, string column-name]]]] )`

**Description**

Returns a result set listing the columns and associated metadata for a table.

**Parameters**

* connection - A valid IBM_DBConnection
* qualifier - A qualifier for DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* schema - The schema which contains the tables. To match all schemas, pass '%'.
* table-name - The name of the table or view. To match all tables in the database, pass `None` or an empty string.
* column-name - The name of the column. To match all columns in the table, pass `None` or an empty string.

**Return Values**

An IBM_DBStatement with a result set containing rows containing the following columns:
* TABLE_CAT - Name of the catalog. The value is `None` if this table does not have catalogs.
* TABLE_SCHEM - Name of the schema.
* TABLE_NAME - Name of the table or view.
* COLUMN_NAME - Name of the column.
* DATA_TYPE - The SQL data type for the column represented as an integer value.
* TYPE_NAME - A string representing the data type for the column.
* COLUMN_SIZE - An integer value representing the size of the column.
* BUFFER_LENGTH - Maximum number of bytes necessary to store data from this column.
* DECIMAL_DIGITS - The scale of the column, or `None` where scale is not applicable.
* NUM_PREC_RADIX - An integer value of either 10 (representing an exact numeric data type), 2 (representing an approximate numeric data type), or `None` (representing a data type for which radix is not applicable).
* NULLABLE - An integer value representing whether the column is nullable or not.
* REMARKS - Description of the column.
* COLUMN_DEF - Default value for the column.
* SQL_DATA_TYPE - The SQL data type of the column.
* SQL_DATETIME_SUB - An integer value representing a datetime subtype code, or `None` for SQL data types to which this does not apply.
* CHAR_OCTET_LENGTH -   Maximum length in octets for a character data type column, which matches COLUMN_SIZE for single-byte character set data, or `None` for non-character data types.
* ORDINAL_POSITION - The 1-indexed position of the column in the table.
* IS_NULLABLE - A string value where 'YES' means that the column is nullable and 'NO' means that the column is not nullable.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

# TABMANY is table name
result = ibm_db.columns(conn,None,None,"TABMANY")
row = ibm_db.fetch_both(result)
if row:
    table_name=row['TABLE_NAME']
    column_name=row['COLUMN_NAME']
print("Table name               : {}" .format(table_name))
print("column name              : {}" .format(column_name))
```

Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-columns.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_008_ColumnInfo.py)

### ibm_db.commit ###
`bool ibm_db.commit ( IBM_DBConnection connection )`

**Description**

Commits an in-progress transaction on the specified IBM_DBConnection and begins a new transaction.

Python applications normally default to AUTOCOMMIT mode, so ibm_db.commit() is not necessary unless AUTOCOMMIT has been turned off for the IBM_DBConnection.

Note: If the specified IBM_DBConnection is a persistent connection, all transactions in progress for all applications using that persistent
connection will be committed. For this reason, persistent connections are not recommended for use in applications that require transactions.

**Parameters**
* connection - A valid IBM_DBConnection

**Return Values**

Returns `True` on success or `False` on failure.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

#set autocommit off
rc = ibm_db.autocommit(conn, ibm_db.SQL_AUTOCOMMIT_OFF)
#insert a row 
stmt = ibm_db.exec_immediate(conn, "insert into tabmany values(2, 'commit test')")
#commit the transaction explicitly as autocommit is off
rc = ibm_db.commit(conn)
#validate that row is inserted
sql_stmt = ibm_db.exec_immediate(conn, "select * from tabmany")
row = ibm_db.fetch_tuple(sql_stmt)
if row:
    print(str(row[0]) + "\n" + row[1])

#close the connection
ibm_db.close(conn)
```
Other Examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-commit.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_021_CommitDelete.py)

### ibm_db.conn_error ###
`string ibm_db.conn_error ( [IBM_DBConnection connection] )`

**Description**

When not passed any parameters, returns the SQLSTATE representing the reason the last database connection attempt failed.

When passed a valid IBM_DBConnection returned by ibm_db.connect(), returns the SQLSTATE representing the reason the
last operation using a IBM_DBConnection failed.

**Parameters**
* connection - A valid IBM_DBConnection

**Return Values**

Returns a string containing the SQLSTATE value or an empty string if there was no error.

**Example**
```python
import ibm_db
#try connecting with an invalid user name
try:
    conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=invalidusername;PWD=password",'','')
except:
    print("Error in connection, sqlstate = ")
    errorState = ibm_db.conn_error()
    print(errorState)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-conn_error.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_081_ConnWrongUser.py)

### ibm_db.conn_errormsg ###
`string ibm_db.conn_errormsg ( [IBM_DBConnection connection] )`

**Description**

When not passed any parameters, returns a string containing the SQLCODE and error message representing the reason the last database connection attempt failed.

When passed a valid IBM_DBConnection returned by ibm_db.connect(), returns  a string containing the SQLCODE and error message representing the reason the
last operation using a IBM_DBConnection failed.

**Parameters**
* connection - A valid IBM_DBConnection

**Return Values**

Returns a string containing the SQLCODE and error message or an empty string if there was no error.

**Example**
```python
import ibm_db
#try connecting with an invalid user name
try:
    conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=invalidusername;PWD=password",'','')
except:
    print("Error in connection, sqlstate = ")
    errorMsg = ibm_db.conn_errormsg()
    print(errorMsg)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-conn_errormsg.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_082_ConnWrongPwd.py)

### ibm_db.connect ###
`IBM_DBConnection ibm_db.connect(string database, string user, string password , [dict options [, constant replace_quoted_literal]])`

**Description**

Creates a new connection to an IBM DB2 Universal Database, IBM Cloudscape, or Apache Derby database.

**Parameters**
* database
    * For a cataloged connection to a database, this parameter represents the database alias in the DB2 client catalog. For an uncataloged connection to a database, database represents a complete connection string in the following format:
DRIVER={IBM DB2 ODBC DRIVER};DATABASE=database;HOSTNAME=hostname;PORT=port;
PROTOCOL=TCPIP;UID=username;PWD=password;
where the parameters represent the following values:
        * hostname - The hostname or IP address of the database server.
        * port - The TCP/IP port on which the database is listening for requests.
        * username - The username with which you are connecting to the database.
        * password - The password with which you are connecting to the database.  
    * In case of JWT access Token based LUW server, supported from Db2 Version 11.5 Mod Pack 4 (db2_v115m4fp0) and above, database represents a complete connection string in the following format:
DRIVER={IBM DB2 ODBC DRIVER};DATABASE=database;HOSTNAME=hostname;PORT=port;accesstoken=complete_access_token;authentication=token;accesstokentype=jwt;
where the parameter represents the following values:
        * hostname - The hostname or IP address of the JWT configured database server.
        * port - The TCP/IP port on which the database is listening for requests.
        * accesstoken - The access token generated on the server for JWT (Json Web Token) configuration.
        * authentication - For connection using JWT access token the authentication has to be set as token.
        * accesstokentype - For connection using JWT access token the parameter accesstokentype has be set as jwt.
* user - The username with which you are connecting to the database. For uncataloged connections, you must pass an empty string.
* password - The password with which you are connecting to the database. For uncataloged connections, you must pass an empty string.
* **options** - A dict of connection options that affect the behavior of the connection:
    * `SQL_ATTR_AUTOCOMMIT`
        * `SQL_AUTOCOMMIT_ON` - AUTOCOMMIT is on
        * `SQL_AUTOCOMMIT_OFF` - AUTOCOMMIT is off
       Refer [ibm_db.autocommit](#ibm_dbautocommit) for example.
    * `ATTR_CASE` ([Example](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_008_ColumnInfo.py))
        * `CASE_NATURAL` - column names are returned in natural case.
        * `CASE_LOWER` - column names are returned in lower case.
        * `CASE_UPPER` - column names are returned in upper case.
    * `SQL_ATTR_CURSOR_TYPE` ([Example](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_cursortype.py))
        * `SQL_CURSOR_FORWARD_ONLY` - uses a forward-only cursor is created, which is the default and is supported on all database servers.
        * `SQL_CURSOR_KEYSET_DRIVEN` - uses a keyset-driven cursor, which is scrollable and allows random access in the result set but is currently only supported by IBM DB2 Universal Database.
        * `SQL_CURSOR_DYNAMIC` - uses a dynamic cursor
        * `SQL_CURSOR_STATIC` - uses a static cursor
    * `SQL_ATTR_INFO_PROGRAMNAME` ([Example](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_setgetOption.py)) - A null-terminated user-defined character string, up to 20 bytes in length, used to specify the name of the application running on the client.
    * `SQL_ATTR_USE_TRUSTED_CONTEXT` ([Example](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_trusted_context_connect.py)) - When connecting to a Db2 database server that supports trusted contexts, set this attribute if you want the connection you are creating to be a trusted connection.
    * `SQL_ATTR_TRUSTED_CONTEXT_USERID` ([Example](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_trusted_context_connect.py)) - A user defined string containing a user ID. Use this on existing trusted connections to switch users. Do not use it when creating a trusted connection.
    * `SQL_ATTR_TRUSTED_CONTEXT_PASSWORD` ([Example](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_trusted_context_connect.py)) - A user defined string containing a password. Use this attribute if the database server requires a password when switching users on a trusted connection. Set this attribute after setting the attribute SQL_ATTR_TRUSTED_CONTEXT_USERID and before executing any SQL statements that access the database server.
    * `SQL_ATTR_CURRENT_SCHEMA` - A null-terminated character string containing the name of the schema to be used by CLI for the SQLColumns() call if the szSchemaName pointer is set to null. Refer to [ibm_db.columns](#ibm_dbcolumns) for example.
    * `SQL_ATTR_INFO_USERID ` ([Example](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_053_AttrThruConn.py)) - The SQL_ATTR_INFO_USERID attribute is used to set the client user ID (accounting user ID) that is sent to a database. The SQL_ATTR_INFO_USERID attribute is for identification purposes only and is not used for any authentication. Do not confuse the SQL_ATTR_INFO_USERID attribute with the authentication user ID. The CLI driver has limit of 255 characters for the SQL_ATTR_INFO_USERID attribute.
    * `SQL_ATTR_INFO_WRKSTNNAME` ([Example](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_053_AttrThruConn.py)) - The SQL_ATTR_INFO_WRKSTNNAME attribute is used to set the client workstation name that is sent to a database.  The CLI driver has limit of 255 characters for the SQL_ATTR_INFO_WRKSTNNAME attribute.
    * `SQL_ATTR_INFO_ACCTSTR` ([Example](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_053_AttrThruConn.py)) - The SQL_ATTR_INFO_ACCTSTR attribute is used to set the client accounting string that is sent to a database. The CLI driver has limit of 255 characters for the SQL_ATTR_INFO_ACCTSTR attribute.
    * `SQL_ATTR_INFO_APPLNAME` ([Example](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_053_AttrThruConn.py)) - The SQL_ATTR_INFO_APPLNAME attribute is used to set the client application name that is sent to a database. The CLI driver has limit of 255 characters for the SQL_ATTR_INFO_APPLNAME attribute.

For more information on these keywords, please refer [IBM data server driver configuration keywords](https://www.ibm.com/support/knowledgecenter/en/SSEPGG_11.1.0/com.ibm.swg.im.dbclient.config.doc/doc/c0054698.html).

* replace_quoted_literal - Indicates if the CLI Connection attribute SQL_ATTR_REPLACE_QUOTED_LITERAL is to be set or not
    * `QUOTED_LITERAL_REPLACEMENT_ON` - Sets the attribute on (default)
    * `QUOTED_LITERAL_REPLACEMENT_OFF` - Sets the attribute off
    

**Return Values**
* On success, an IBM_DBConnection connection object
* On failure, `None`

**Example**
```python
import ibm_db
#use connection string
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

#use connection string with JWT access token
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;accesstoken=complete_access_token;authentication=token;accesstokentype=jwt;",'','')

#use options
options = { ibm_db.SQL_ATTR_INFO_PROGRAMNAME : 'TestProgram', ibm_db.SQL_ATTR_CURRENT_SCHEMA : 'MYSCHEMA' }
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','', options)

Note: Local cataloged database implicit connection
i) If database parameter specified is a local database alias name with blank userid and password
then connect/pconnect API will use current logged in user's userid for implicit connection
eg: **conn = ibm_db.connect('sample', '', '')**

ii) If database parameter is a connection string with value "DSN=database_name" then
connect/pconnect API will use current logged in user's userid for implicit connection
eg: **conn = ibm_db.connect('DSN=sampledb', '', '')**
If you are using DSN in connection string as in above example, then you must specify other necessary connection details like hostname, userid, password via supported keywords in db2dsdriver.cfg configuration file located under site-packages/clidriver/cfg or under the cfg folder as per the path you have set IBM_DB_HOME to. You can refer to the sample file below.
For more information, please refer [IBM data server driver configuration keywords](https://www.ibm.com/support/knowledgecenter/en/SSEPGG_11.1.0/com.ibm.swg.im.dbclient.config.doc/doc/c0054698.html).
```

**Sample configuration in db2dsdriver.cfg:**
```xml
<configuration>
   <dsncollection>
      <dsn alias="sampledb" name="sample" host="x.y.z.com" port="50000">
      </dsn>
   </dsncollection>
   <databases>
      <database name="sample" host="x.y.z.com" port="50000">
	  <parameter name="userid" value="username"/>
	  <parameter name="password" value="xxxxxx"/>
       </database>
   </databases>
</configuration>
```

### ibm_db.createdb ###
`bool ibm_db.createdb ( IBM_DBConnection connection, string dbName [, codeSet, mode] )`

**Description**

Creates a database by using the specified database name, code set and mode

**Parameters**

* connection - A valid IBM_DBConnection as returned from ibm_db.connect() by specifying the ATTACH keyword
* dbName - Name of the database that is to be created.
* codeSet - Database code set information. Note: If the value of the codeSet argument not specified, the database is created in the Unicode code page for DB2 data servers and in the UTF-8 code page for IDS data servers.
* mode - Database logging mode. Note: This value is applicable only to IDS data servers.

**Return Value**

Returns `True` on successful creation of database else return `None`.

**Example**
```python
import ibm_db
conn_str_attach = "attach=true;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password"
database='test123'
conn_attach = ibm_db.connect(conn_str_attach, '', '')
rc = ibm_db.createdb(conn_attach, database)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-createdb_REMOTE.py),
[Example2](https://github.com/IBM/db2-python/blob/master/Jupyter_Notebooks/ibm_db-createdb.ipynb),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_createDropDB.py)

### ibm_db.createdbNX ###
`bool ibm_db.createdbNX ( IBM_DBConnection connection, string dbName [, codeSet, mode] )`

**Description**

Creates the database if it does not exist by using the specified database name, code set and mode.

**Parameters**

* connection - A valid IBM_DBConnection as returned from ibm_db.connect() by specifying the ATTACH keyword
* dbName Name of the database that is to be created.
* codeSet - Database code set information. Note: If the value of the codeSet argument not specified, the database is created in the Unicode code page for DB2 data servers and in the UTF-8 code page for IDS data servers.
* mode - Database logging mode. Note: This value is applicable only to IDS data servers.

**Return Value**

Returns `True` if database already exists or created successfully else return `None`

**Example**
```python
import ibm_db
conn_str_attach = "ATTACH=true;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password"
database='test123'
conn_attach = ibm_db.connect(conn_str_attach, '', '')
rc = ibm_db.createdbNX(conn_attach, database)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Jupyter_Notebooks/ibm_db-createdbNX.ipynb)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/IBM_DB/ibm_db/ibm_db_tests/test_createdbNX.py)

### ibm_db.cursor_type ###
`int ibm_db.cursor_type ( IBM_DBStatement stmt )`

**Description**

Returns the cursor type used by an IBM_DBStatement. Use this to determine
if you are working with a forward-only cursor or scrollable cursor.

**Parameters**

* stmt - A valid IBM_DBStatement.

**Return Values**

One of the following values: `SQL_CURSOR_FORWARD_ONLY`, `SQL_CURSOR_KEYSET_DRIVEN`, `SQL_CURSOR_DYNAMIC`, or `SQL_CURSOR_STATIC`

**Example**
```python
import ibm_db
conn = ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

stmtOption = {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_FORWARD_ONLY}
sqlStatement = "SELECT * FROM tabmany"
resultSet = ibm_db.exec_immediate(conn, sqlStatement, stmtOption)

#get the cursor type
cursorType = ibm_db.cursor_type(resultSet)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Jupyter_Notebooks/ibm_db-cursor_type.ipynb)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/IBM_DB/ibm_db/ibm_db_tests/test_cursortype.py)

### ibm_db.dropdb ###
`bool ibm_db.dropdb ( IBM_DBConnection connection, string dbName )`

**Description**

Drops the specified database

**Parameters**

* connection - A valid IBM_DBConnection as returned from ibm_db.connect() by specifying the ATTACH keyword
* dbName - Name of the database that is to be dropped.

**Return Value**

Returns `True` if specified database dropped successfully else `None`.

**Example**
```python
import ibm_db
conn = ibm_db.connect("ATTACH=true;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

dbName = "MY_DB"
rc = ibm_db.dropdb(conn, dbName)
```
Othe examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-dropdb_LOCAL.py),
[Example2](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-dropdb_REMOTE.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_createDropDB.py)

### ibm_db.exec_immediate ###
`stmt_handle ibm_db.exec_immediate( IBM_DBConnection connection, string statement [, dict options] )`

**Description**

Prepares and executes an SQL statement.

If you plan to repeatedly issue the same SQL statement with different
parameters, consider calling ibm_db.prepare() and ibm_db.execute() to
enable the database server to reuse its access plan and increase the
efficiency of your database access.

If you plan to interpolate Python variables into the SQL statement,
understand that this is one of the more common security exposures.
Consider calling ibm_db.prepare() to prepare an SQL statement with
parameter markers for input values. Then you can call ibm_db.execute()
to pass in the input values and avoid SQL injection attacks.

**Parameters**

* connection - A valid IBM_DBConnection
* statement - An SQL statement. The statement cannot contain any parameter markers.
* options - A dict containing statement options.
    * `SQL_ATTR_CURSOR_TYPE` - Set the cursor type to one of the following (not supported on all databases):
        * `SQL_CURSOR_FORWARD_ONLY`
        * `SQL_CURSOR_KEYSET_DRIVEN`
        * `SQL_CURSOR_DYNAMIC`
        * `SQL_CURSOR_STATIC`

**Return Values**

Returns a stmt_handle resource if the SQL statement was issued
successfully, or `False` if the database failed to execute the SQL statement.

**Example**
```python
import ibm_db
import pandas as pd
import ibm_db_dbi as dbi
conn = ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql_stmt =  "select * from tabmany"
result = ibm_db.exec_immediate(conn, sql_stmt)
if stmt is not None:
    row = ibm_db.fetch_tuple(result)
    while(row):
        print("{}\t{}\n".format(row[0],row[1])
        row = ibm_db.fetch_tuple(result)

# use pandas dataframe
conn1 = dbi.connect('DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password')
df = pd.read_sql("select * from tabmany", conn1)
print(df)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-exec_immediate.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_113_DateTest.py)

### ibm_db.execute ###
`bool ibm_db.execute ( IBM_DBStatement stmt [, tuple parameters] )`

**Description**

ibm_db.execute() executes an SQL statement that was prepared by ibm_db.prepare(). If the SQL statement returns a result set, for example, a SELECT statement that returns one or more result sets, you can retrieve a row as an tuple/dict from the stmt resource using ibm_db.fetch_assoc(), ibm_db.fetch_both(), or ibm_db.fetch_tuple(). Alternatively, you can use ibm_db.fetch_row() to move the result set pointer to the next row and fetch a column at a time from that row with ibm_db.result(). Refer to ibm_db.prepare() for a brief discussion of the advantages of using ibm_db.prepare() and ibm_db.execute() rather than ibm_db.exec_immediate(). To execute stored procedure refer ibm_db.callproc()

**Parameters**
* stmt - A prepared statement returned from ibm_db.prepare().
* parameters - An tuple of input parameters matching any parameter markers contained in the prepared statement.

**Return Values**

Returns `True` on success or `False` on failure.

**Example**
```python
import ibm_db
conn = ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql_stmt = "insert into tabmany values(?,?)"
stmt = ibm_db.prepare(conn, sql_stmt)
id = 3
name = "Sam"
ibm_db.bind_param(stmt, 1, id)
ibm_db.bind_param(stmt, 2, name)
try:
    ibm_db.execute(stmt)
except:
    print(ibm_db.stmt_errormsg())
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-execute.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_265_NoAffectedRows.py)

### ibm_db.execute_many ###
`mixed ibm_db.execute_many( IBM_DBStatement stmt, tuple seq_of_parameters )`

**Description**

Executes an SQL statement prepared by ibm_db.prepare() against all parameter sequences or mappings found in the sequence seq_of_parameters.
Use this function for bulk insert/update/delete operations. It uses ArrayInputChaining feature of DB2 CLI to ensure minimum roundtrips to the server.

**Parameters**
* stmt - A prepared statement returned from ibm_db.prepare().
* seq_of_parameters - A tuple of tuples, with each tuple containing input parameters matching parameter markers contained in the prepared statement.

**Return Values**
* On success, returns the number of inserted/updated/deleted rows
* On failure, returns `None`. Use ibm_db.num_rows() to find out the inserted/updated/deleted row count.

**Example**
```python
import ibm_db
import ibm_db_dbi as dbi
import pandas as pd
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

ibm_db.exec_immediate(conn,"CREATE table tabmany( id SMALLINT , name VARCHAR(32))")
insert = "insert into tabmany values(?,?)"
values=(1,'sample')
params=tuple(tuple (x+i if type(x)==int else x+str(i) for x in values) for i in range(3))
stmt_insert = ibm_db.prepare(conn, insert)
ibm_db.execute_many(stmt_insert,params)
row_count = ibm_db.num_rows(stmt_insert)
print("inserted {} rows".format(row_count))

# use data frame, requires ibm_db_dbi connection
conn1 = dbi.connect('DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password')

data={'ID':[11,22,33,44],'NAME':['val1','val2','val3','val4']}
df1=pd.DataFrame(data)
tuple_of_tuples = tuple([tuple(x) for x in df1.values])
sql="insert into testmany values(?,?)"

stmt=ibm_db.prepare(conn,sql)
ibm_db.execute_many(stmt,tuple_of_tuples)

df2=pd.read_sql("select * from test",conn1) 
print(df2)

subset = df2[['ID','NAME','RATING']]
tuple_of_tuples1 = tuple([tuple(x) for x in subset.values])
ibm_db.execute_many(stmt,tuple_of_tuples1)

df3=pd.read_sql("select * from test", conn1)
print(df3)
```
Other examples:
[Example1](http://htmlpreview.github.io/?https://github.com/IBM/db2-python/blob/master/HTML_Documentation/ibm_db-execute_many.html)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_execute_many.py)

### ibm_db.fetch_tuple ###
`tuple ibm_db.fetch_tuple ( IBM_DBStatement stmt [, int row_number] )`

**Description**

Returns a tuple, indexed by column position, representing a row in a result set.

**Parameters**
* stmt - A valid stmt resource containing a result set.
* row_number - Requests a specific 1-indexed row from the result set. Passing this parameter results in a warning if the result set uses a forward-only cursor.

**Return Values**
* Returns a tuple containing all the column values in the result set for the selected row or the next row if row_number was not specified
* Returns `False` if there are no rows left in the result set, or if the row requested by row_number does not exist in the result set.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "select id, name from tabmany"
stmt = ibm_db.exec_immediate(conn, sql)

row = ibm_db.fetch_tuple(stmt)
while ( row ):
    for i in row:
         print(i)
    row = ibm_db.fetch_tuple(stmt)
ibm_db.close(conn)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-fetch_tuple.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_154_AllFetches.py)

### ibm_db.fetch_assoc ###
`dict ibm_db.fetch_assoc ( IBM_DBStatement stmt [, int row_number] )`

**Description**

Returns a dict, indexed by column name, representing a row in a result set.

**Parameters**
* stmt - A valid stmt resource containing a result set.
* row_number - Requests a specific 1-indexed row from the result set. Passing this parameter results in a warning if the result set uses a forward-only cursor.

**Return Values**
* Returns a dict containing all the column values indexed by column name for the selected row or the next row if row number was not specified.
* Returns `False` if there are no rows left in the result set, or if the row requested by row_number does not exist in the result set.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "select id, name from tabmany"
stmt = ibm_db.prepare(conn, sql,{ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_KEYSET_DRIVEN})
result = ibm_db.execute(stmt)
#fetch every alternate row starting from 2nd 
i = 2
row = ibm_db.fetch_assoc(stmt, i)
while ( row ):
    print("%-5d %-16s " % (row['ID'], row['NAME']))
    i = i + 2
    row = ibm_db.fetch_assoc(stmt, i)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-fetch_assoc.py),
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_151_FetchAssocSelect_02.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_153_FetchAssocSelect_04.py),
[Example4](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_158_FetchAssocNestedSelects_02.py)

### ibm_db.fetch_both ###
`dict ibm_db.fetch_both ( IBM_DBStatement stmt [, int row_number] )`

**Description**

Returns a dict, indexed by column name and position, representing a row in a result set.

**Parameters**
* stmt - A valid stmt resource containing a result set.
* row_number - Requests a specific 1-indexed row from the result set. Passing this parameter results in a warning if the result set uses a forward-only cursor.

**Return Values**
* Returns a dict containing all the column values indexed by column name and by 0-indexed column number for the selected row or the next row if row number was not specified.
* Returns `False` if there are no rows left in the result set, or if the row requested by row_number does not exist in the result set.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "select id, name from tabmany"
stmt = ibm_db.prepare(conn, sql,)
result = ibm_db.execute(stmt)
row = ibm_db.fetch_both(stmt)
while ( row ):
    print("%-5d %-5d " % (row['ID'], row[0]))
    print("%-16s %-16s " % (row['NAME'], row[1]))
    row = ibm_db.fetch_both(stmt)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-fetch_both.py),
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_161_FetchBothNestedSelects_01.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_162_FetchBothNestedSelects_02.py)

### ibm_db.fetch_row ###
`bool ibm_db.fetch_row ( IBM_DBStatement stmt [, int row_number] )`

**Description**

Sets the result set pointer to the next row or requested row.

Use ibm_db.fetch_row() to iterate through a result set, or to point to a
specific row in a result set if you requested a scrollable cursor.

To retrieve individual fields from the result set, call the ibm_db.result()
function. Rather than calling ibm_db.fetch_row() and ibm_db.result(), most
applications will call one of ibm_db.fetch_assoc(), ibm_db.fetch_both(), or
ibm_db.fetch_tuple() to advance the result set pointer and return a complete
row.

**Parameters**
* stmt - A valid stmt resource.
* row_number - Requests a specific 1-indexed row from the result set. Passing this parameter results in a warning if the result set uses a forward-only cursor.

**Return Values**

Returns `True` if the requested row exists in the result set. Returns `False` if
the requested row does not exist in the result set.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "select id, name from tabmany"
stmt = ibm_db.prepare(conn, sql,)
result = ibm_db.execute(stmt)
row = ibm_db.fetch_row(stmt)
while ( row ):
    print(row)
    row = ibm_db.fetch_row(stmt)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-fetch_row.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_036_FetchRow_02.py)

### ibm_db.field_display_size ###
`int ibm_db.field_display_size ( IBM_DBStatement stmt, mixed column )`

**Description**

Returns the maximum number of bytes required to display a column in a result set.

**Parameters**
* stmt - Specifies an IBM_DBStatement containing a result set.
* column - Specifies the column in the result set. This can either be an integer representing the 0-indexed position of the column or a string containing the name of the column.

**Return Values**

Returns an integer value with the maximum number of bytes required to display
the specified column or `False` if the column does not exist.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "select id, name from tabmany"
stmt = ibm_db.prepare(conn, sql,)
result = ibm_db.execute(stmt)
cols = ibm_db.num_fields(stmt)
for i in range(0, cols):
    size = ibm_db.field_display_size(stmt,i)
    print("col:%d and size: %d" % (i, size))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-field_display_size.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_213_FieldDisplaySize_04.py)

### ibm_db.field_name ###
`string ibm_db.field_name ( IBM_DBStatement stmt, mixed column )`

**Description**

Returns the name of the specified column in the result set.

**Parameters**
* stmt - Specifies an IBM_DBStatement containing a result set.
* column - Specifies the column in the result set. This can either be an integer representing the 0-indexed position of the column or a string containing the name of the column.

**Return Values**

Returns a string containing the name of the specified column or `False` if the column does not exist.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "select id, name from tabmany"
field_name=[]
stmt = ibm_db.prepare(conn, sql,)
result = ibm_db.execute(stmt)
cols = ibm_db.num_fields(stmt)
for i in range(0, cols):
    field_name.append(ibm_db.field_name(stmt,i))
print(field_name)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-field_name.py),
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_231_FieldTypeName.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_240_FieldWidthPosName_01.py)

### ibm_db.field_num ###
`int ibm_db.field_num ( IBM_DBStatement stmt, mixed column )`

**Description**

Returns the position of the named column in a result set.

**Parameters**
* stmt - Specifies an IBM_DBStatement containing a result set.
* column - Specifies the column in the result set. This can either be an integer representing the 0-indexed position of the column or a string containing the name of the column.

**Return Values**

Returns an integer containing the 0-indexed position of the specified column or `False` if the column does not exist.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "select id, name from tabmany"
field_num=[]
field_name=[]
stmt = ibm_db.prepare(conn, sql,)
result = ibm_db.execute(stmt)
cols = ibm_db.num_fields(stmt)

# index by column number
for i in range(0, cols):
    field_name.append(ibm_db.field_name(stmt,i))
    field_num.append(ibm_db.field_num(stmt,field_name[i]))
print(field_num)

# index by column name
field_num=[]
field_num.append(ibm_db.field_num(stmt, 'ID'))
field_num.append(ibm_db.field_num(stmt, 'NAME'))
print(field_num)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-field_num.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_111_FieldNumAddCol.py)

### ibm_db.field_precision ###
`int ibm_db.field_precision ( IBM_DBStatement stmt, mixed column )`

**Description**

Returns the precision of the indicated column in a result set.

**Parameters**
* stmt - Specifies an IBM_DBStatement containing a result set.
* column - Specifies the column in the result set. This can either be an integer representing the 0-indexed position of the column or a string containing the name of the column.

**Return Values**

Returns an integer containing the precision of the specified column or `False` if the column does not exist.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "select id, name from tabmany"
field_precision=[]
stmt = ibm_db.prepare(conn, sql,)
result = ibm_db.execute(stmt)
cols = ibm_db.num_fields(stmt)
for i in range(0, cols):
    field_precision.append(ibm_db.field_precision(stmt,i))
print(field_precision)

row = ibm_db.fetch_tuple(stmt)
# use the precision to format the data display
print("{:<{prec}}\t{:>{char_prec}}".format(row[0],row[1],prec=field_precision[0],char_prec=field_precision[1]))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-field_precision.py)

### ibm_db.field_scale ###
`int ibm_db.field_scale ( IBM_DBStatement stmt, mixed column )`

**Description**

Returns the scale of the indicated column in a result set.

**Parameters**
* stmt - Specifies an IBM_DBStatement containing a result set.
* column - Specifies the column in the result set. This can either be an integer representing the 0-indexed position of the column or a string containing the name of the column.

**Return Values**

Returns an integer containing the scale of the specified column or `False` if the column does not exist.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

insert = "insert into scale_test values(25280.00, 17600.00)"
ibm_db.exec_immediate(conn, insert)

sql = "select salary, bonus from scale_test"
field_scale=[]
stmt = ibm_db.prepare(conn, sql)
result = ibm_db.execute(stmt)
cols = ibm_db.num_fields(stmt)
for i in range(0, cols):
    field_scale.append(ibm_db.field_scale(stmt,i))
print(field_scale)
row = ibm_db.fetch_tuple(stmt)
print("{:<{scale1}}\t{:>{scale2}}".format(row[0],row[1],scale1=field_scale[0],scale2=field_scale[1]))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-field_scale.py)

### ibm_db.field_type ###
`string ibm_db.field_type ( IBM_DBStatement stmt, mixed column )`

**Description**

Returns the data type of the indicated column in a result set.

**Parameters**
* stmt - Specifies an IBM_DBStatement containing a result set.
* column - Specifies the column in the result set. This can either be an integer representing the 0-indexed position of the column or a string containing the name of the column.

**Return Values**

Returns a string containing the defined data type of the specified column or `False` if the column does not exist.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

result = ibm_db.exec_immediate(conn, "select * from tabmany")
for i in range(0, ibm_db.num_fields(result) ):
    print(str(i) + ":" + str(ibm_db.field_type(result,i)))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-field_type.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_230_FieldTypePos.py)

### ibm_db.field_width ###
`int ibm_db.field_width ( IBM_DBStatement stmt, mixed column )`

**Description**

Returns the width of the current value of the indicated column in a result
set. This is the maximum width of the column for a fixed-length data type, or
the actual width of the column for a variable-length data type.

**Parameters**
* stmt - Specifies an IBM_DBStatement containing a result set.
* column - Specifies the column in the result set. This can either be an integer representing the 0-indexed position of the column or a string containing the name of the column.

**Return Values**

Returns an integer containing the width of the specified character or binary column; or `False` if the column does not exist.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

result = ibm_db.exec_immediate(conn, "select * from tabmany")
for i in range(0, ibm_db.num_fields(result) ):
    col_width = ibm_db.field_width(result, i)
    col_name = ibm_db.field_name(result,i)
    #print(col_name,col_width)
    print("{:<{width}}".format(col_name, width=col_width),end=" ")
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-field_width.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_240_FieldWidthPosName_01.py)

### ibm_db.foreign_keys ###
`IBM_DBStatement ibm_db.foreign_keys ( IBM_DBConnection connection, string pk_qualifier, string pk_schema, string pk_table-name, string fk_qualifier, string fk_schema, string fk_table-name )`

**Description**

Returns a result set listing the foreign keys for a table.

**Parameters**

* connection - A valid IBM_DBConnection
* pk_qualifier - A qualifier for the pk_table-name argument for the DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* pk_schema - The schema for the pk_table-name argument which contains the tables. If schema is `None`, the current schema for the connection is used instead.
* pk_table-name - The name of the table which contains the primary key.
* fk_qualifier - A qualifier for the fk_table-name argument for the DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* fk_schema - The schema for the fk_table-name argument which contains the tables. If schema is `None`, the current schema for the connection is used instead.
* fk_table-name - The name of the table which contains the foreign key.

**Return Values**

Returns an IBM_DBStatement with a result set containing the following columns:
* PKTABLE_CAT - Name of the catalog for the table containing the primary key. The value is `None` if this table does not have catalogs.
* PKTABLE_SCHEM - Name of the schema for the table containing the primary key.
* PKTABLE_NAME - Name of the table containing the primary key.
* PKCOLUMN_NAME - Name of the column containing the primary key.
* FKTABLE_CAT - Name of the catalog for the table containing the foreign key. The value is `None` if this table does not have catalogs.
* FKTABLE_SCHEM - Name of the schema for the table containing the foreign key.
* FKTABLE_NAME - Name of the table containing the foreign key.
* FKCOLUMN_NAME - Name of the column containing the foreign key.
* KEY_SEQ - 1-indexed position of the column in the key.
* UPDATE_RULE - Integer value representing the action applied to the foreign key when the SQL operation is UPDATE.
* DELETE_RULE - Integer value representing the action applied to the foreign key when the SQL operation is DELETE.
* FK_NAME - The name of the foreign key.
* PK_NAME - The name of the primary key.
* DEFERRABILITY - An integer value representing whether the foreign key deferrability is SQL_INITIALLY_DEFERRED, SQL_INITIALLY_IMMEDIATE, or SQL_NOT_DEFERRABLE.

If pk_table-name contains a table name, and fk_table-name is an empty string, the ibm_db.foreign_keys() function returns a result set that contains the primary key of the specified table and all of the foreign keys (in other tables) that refer to it.

If fk_table-name contains a table name, and pk_table-name is an empty string, the ibm_db.foreign_keys() function returns a result set that contains all of the foreign keys in the specified table and the primary keys (in other tables) to which they refer.

If both pk_table-name and fk_table-name contain table names, the ibm_db.foreign_keys() function returns the foreign keys in the table that are specified in fk_table-name, which refer to the primary key of the table that is specified in pk_table-name. There should be one key at the most.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

tkey = "create table test_key(name VARCHAR(30) NOT NULL, idf INTEGER NOT NULL)"
try:
    result = ibm_db.exec_immediate(conn, tkey)
except:
    pass
	
fktable = "create table foreign_key(namef VARCHAR(30) NOT NULL, id INTEGER NOT NULL, FOREIGN KEY(namef) REFERENCES test_keys(name))"
try:
    result = ibm_db.exec_immediate(conn, fktable)
except:
    pass

stmt = ibm_db.foreign_keys(conn, None, None, None, None, None,'FOREIGN_KEY')
row = ibm_db.fetch_tuple(stmt)
print(row[7],"is a foreign key in", row[6], "referencing", row[3], "in table", row[2])
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-foreign_keys.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_024_ForeignKeys.py)

### ibm_db.free_result ###
`bool ibm_db.free_result ( IBM_DBStatement stmt )`

**Description**

Frees the system and IBM_DBConnections that are associated with a result
set. These resources are freed implicitly when a script finishes, but you
can call ibm_db.free_result() to explicitly free the result set resources
before the end of the script.

**Parameters**
* stmt - A valid IBM_DBStatement.

**Return Values**

Returns `True` on success or `False` on failure.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

result = ibm_db.exec_immediate(conn, "select * from tabmany")
row = ibm_db.fetch_both(result)
while row:
    print(row)
    row = ibm_db.fetch_both(result)
	
ibm_db.free_result(result)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-free_result.py),
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_250_FreeResult_01.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_251_FreeResult_02.py)

### ibm_db.free_stmt ###
`bool ibm_db.free_stmt ( IBM_DBStatement stmt )` **(DEPRECATED)**

**Description**

Frees the system and IBM_DBConnections that are associated with a statement
resource. These resources are freed implicitly when a script finishes, but
you can call ibm_db.free_stmt() to explicitly free the statement resources
before the end of the script.

This API is deprecated. Applications should use ibm_db.free_result instead.

**Parameters**
* stmt - A valid IBM_DBStatement.

**Return Values**

Returns `True` on success or `False` on failure.

### ibm_db.get_option ###
`mixed ibm_db.get_option ( mixed resc, int options, int type )`

**Description**

Returns a value that is the current setting of a connection or statement
attribute.

**Parameters**
* resc - A valid IBM_DBConnection or IBM_DBStatement containing a result set.
* options - The options to be retrieved
* type - The type of resc
    * `0` - IBM_DBStatement
    * `1` - IBM_DBConnection

**Return Values**

Returns the current setting of the resource attribute provided.

You may refer to [Supported Options](#SupportedOptions) section for the list of options that can be set at connection and statement level.

```python
import ibm_db

# Connection options
conn_options = { ibm_db.SQL_ATTR_INFO_PROGRAMNAME : 'TestProgram'}
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','', conn_options)

value=ibm_db.get_option(conn, ibm_db.SQL_ATTR_INFO_PROGRAMNAME, 1)
print("Connection options:\nSQL_ATTR_INFO_PROGRAMNAME = {}".format(value), end="\n")
returncode=ibm_db.set_option(conn, {ibm_db.SQL_ATTR_AUTOCOMMIT:0},1)
value=ibm_db.get_option(conn, ibm_db.SQL_ATTR_AUTOCOMMIT, 1)
print("SQL_ATTR_AUTOCOMMIT = {}".format(str(value)), end="\n")

# statement options
stmt = ibm_db.prepare(conn, "select * from tabmany")
returnCode = ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_QUERY_TIMEOUT : 20}, 0)
value = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_QUERY_TIMEOUT, 0)
print("Statement options:\nSQL_ATTR_QUERY_TIMEOUT = {}".format(str(value)), end="\n")
result = ibm_db.execute(stmt)

if result:
    ibm_db.free_result(stmt)
else:
    print(ibm_db..stmt_errormsg())
ibm_db.rollback(conn)
ibm_db.close(conn)
```
Other example:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-get_option_STATEMENT.py),
[Example2](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-get_option_CONNECTION.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_setgetOption.py)

### ibm_db.next_result ###
`IBM_DBStatement ibm_db.next_result ( IBM_DBStatement stmt )`

**Description**

Requests the next result set from a stored procedure.
A stored procedure can return zero or more result sets. While you handle the
first result set in exactly the same way you would handle the results
returned by a simple SELECT statement, to fetch the second and subsequent
result sets from a stored procedure you must call the ibm_db.next_result()
function and return the result to a uniquely named Python variable.

**Parameters**
* stmt - A prepared statement returned from ibm_db.exec_immediate() or ibm_db.execute().

**Return Values**

Returns a new IBM_DBStatement containing the next result set if the stored
procedure returned another result set. Returns `False` if the stored procedure
did not return another result set.


**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

create_proc = """create procedure multi_results() 
result sets 3
language sql
Begin
DECLARE c1 CURSOR WITH RETURN FOR 
select name, id from tabmany;

DECLARE c2 CURSOR WITH RETURN FOR
select name, id from tabmany where id < 40;

DECLARE c3 CURSOR WITH RETURN FOR
select name, id from tabmany where id > 40;

OPEN c1;
OPEN c2;
OPEN c3;
END """

try:
    rc = ibm_db.exec_immediate(conn, create_proc)
except:
    pass

# retrieve first result set
resultSet_1 = None
try:
    resultSet_1 = ibm_db.callproc(conn, 'multi_results')
except:
    print("stored procedure invocation\n")
    print(ibm_db.stmt_errormsg())
    pass


if resultSet_1:
    row = ibm_db.fetch_tuple(resultSet_1)
    while row:
        for i in row:
            print(i)
        row = ibm_db.fetch_tuple(resultSet_1)

# retrieve second result set
resultSet_2 = None
try:
    resultSet_2 = ibm_db.next_result(resultSet_1)
except Exception:
    pass	

if resultSet_2:
    row = ibm_db.fetch_tuple(resultSet_2)
    while row:
        for i in row:
            print(i)
        row = ibm_db.fetch_tuple(resultSet_2)

# retrieve third result set		
resultSet_3 = None
try:
    resultSet_3 = ibm_db.next_result(resultSet_1)
except Exception:
    pass

if resultSet_3:
    row = ibm_db.fetch_tuple(resultSet_3)
    while row:
        for i in row:
            print(i)
        row = ibm_db.fetch_tuple(resultSet_3)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-next_result.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_200_MultipleRsltsetsUniformColDefs.py)

### ibm_db.num_fields ###
`int ibm_db.num_fields ( IBM_DBStatement stmt )`

**Description**

Returns the number of fields contained in a result set. This is most useful
for handling the result sets returned by dynamically generated queries, or
for result sets returned by stored procedures, where your application cannot
otherwise know how to retrieve and use the results.

**Parameters**
* stmt - A valid IBM_DBStatement containing a result set.

**Return Values**

Returns an integer value representing the number of fields in the result set
associated with the specified IBM_DBStatement. Returns `False` if stmt is not
a valid IBM_DBStatement object.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "select id, name from tabmany"
stmt = ibm_db.prepare(conn, sql,)
result = ibm_db.execute(stmt)
cols = ibm_db.num_fields(stmt)
print(cols)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-num_fields.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_102_NumFieldsSelect_01.py)

### ibm_db.num_rows ###
`int ibm_db.num_rows ( IBM_DBStatement stmt )`

**Description**

Returns the number of rows deleted, inserted, or updated by an SQL statement.

To determine the number of rows that will be returned by a SELECT statement,
issue `SELECT COUNT(*)` with the same predicates as your intended SELECT
statement and retrieve the value. If your application logic checks the number
of rows returned by a SELECT statement and branches if the number of rows is
0, consider modifying your application to attempt to return the first row
with one of ibm_db.fetch_assoc(), ibm_db.fetch_both(), ibm_db.fetch_tuple(),
or ibm_db.fetch_row(), and branch if the fetch function returns `False`.
Note: If you issue a SELECT statement using a scrollable cursor,
ibm_db.num_rows() returns the number of rows returned by the SELECT
statement. However, the overhead associated with scrollable cursors
significantly degrades the performance of your application, so if this is the
only reason you are considering using scrollable cursors, you should use a
forward-only cursor and either call `SELECT COUNT(*)` or rely on the boolean
return value of the fetch functions to achieve the equivalent functionality
with much better performance.

**Parameters**
* stmt - A valid stmt resource containing a result set.

**Return Values**

Returns the number of rows affected by the last SQL statement issued by the
specified statement handle.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "update tabmany set id=15 where id < 40"
res = ibm_db.exec_immediate(conn, sql)
print ("Number of affected rows: %d" % ibm_db.num_rows(res))
ibm_db.rollback(conn)
ibm_db.close(conn)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-num_rows.py),
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_265_NoAffectedRows.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_011_DeleteRowCount.py),
[Example4](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_017_selectRowcountPrefetchSTMTOpt.py)

### ibm_db.pconnect ###
`IBM_DBStatement ibm_db.pconnect ( string database, string username, string password [, dict options] )`

**Description**

Returns a persistent connection to an IBM DB2 Universal Database,
IBM Cloudscape, Apache Derby or Informix. Persistent connections
are not closed when ibm_db.close is called on them. Instead, they
are returned to a process-wide connection pool. The next time
ibm_db.pconnect is called, the connection pool is searched for a
matching connection. If one is found, it is returned to the application
instead of attempting a new connection.

For more information on parameters and return values, see [ibm_db.connect](#ibm_dbconnect).

**Example**
```python
import ibm_db

# Open normal connection
conn1=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')
print("Normal connection 1 = {}".format(conn1))
# Open persistent connections
pconn1 = ibm_db.pconnect('DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password','','')
print("Persistent connection 1 = {}".format(pconn1))
# pconn2 is same as pconn1
pconn2 = ibm_db.pconnect('DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password','','')
print("Persistent connection 2 = {}".format(pconn2))

# closing normal connection
ibm_db.close(conn1)
print("Normal connection 1 = {} closed".format(conn1))
# closing persistent connection will not shut off the db connection
ibm_db.close(pconn1)
print("Persistent connection 1 = {} closed".format(pconn1))

# select from the persistent connection
sql = "select * from tabmany"
stmt = ibm_db.exec_immediate(pconn2,sql)

# fetching data from a closed connection results in error
try:
    sql = "select * from tabmany"
    stmt = ibm_db.exec_immediate(conn1,sql)
except:
    print("Connection is closed, Hence can't execute {} on conn1".format(sql))
    pass
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-pconnect_DB.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_trusted_context_pconnect.py)

### ibm_db.prepare ###
`IBMDB_Statement ibm_db.prepare ( IBM_DBConnection connection, string statement [, dict options] )`

**Description**

Creates a prepared SQL statement which can include 0 or more parameter markers
(? characters) representing parameters for input,output, or input/output.
You can pass parameters to the prepared statement using ibm_db.bind_param(),
or for input values only, as a tuple passed to ibm_db.execute().

There are two main advantages to using prepared statements in your application:
* Performance: when you prepare a statement, the database server
    creates an optimized access plan for retrieving data with that
    statement. Subsequently issuing the prepared statement with
    ibm_db.execute() enables the statements to reuse that access plan
    and avoids the overhead of dynamically creating a new access plan
    for every statement you issue.
* Security: when you prepare a statement, you can include parameter
    markers for input values. When you execute a prepared statement
    with input values for placeholders, the database server checks each
    input value to ensure that the type matches the column definition or
    parameter definition.

**Parameters**
* connection - A valid IBM_DBConnection
* statement - An SQL statement, optionally containing one or more parameter markers.
* options - A dict containing statement options.
    * `SQL_ATTR_CURSOR_TYPE` - Set the cursor type to one of the following (not supported on all databases):
        * `SQL_CURSOR_FORWARD_ONLY`
        * `SQL_CURSOR_KEYSET_DRIVEN`
        * `SQL_CURSOR_DYNAMIC`
        * `SQL_CURSOR_STATIC`

**Return Values**

Returns a IBM_DBStatement object if the SQL statement was successfully
parsed and prepared by the database server or `False` if the database
server returned an error.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')
stmt=ibm_db.prepare(conn, "select * from tabmany where id=?", {ibm_db.SQL_ATTR_CURSOR_TYPE: ibm_db.SQL_CURSOR_STATIC})
id=1
ibm_db.bind_param(stmt, 1,id)
ibm_db.execute(stmt)
row=ibm_db.fetch_tuple(stmt)
print(row)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-prepare.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_000_PrepareDb.py)

### ibm_db.primary_keys ###
`IBM_DBStatement ibm_db.primary_keys ( IBM_DBConnection connection, string qualifier, string schema, string table-name )`

**Description**

Returns a result set listing the primary keys for a table.

**Parameters**

* connection - A valid IBM_DBConnection
* qualifier - A qualifier for DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* schema - The schema which contains the tables. If schema is `None`, the current schema for the connection is used instead.
* table-name - The name of the table.

**Return Values**

Returns an IBM_DBStatement with a result set containing the following columns:
* TABLE_CAT - Name of the catalog for the table containing the primary key. The value is `None` if this table does not have catalogs.
* TABLE_SCHEM - Name of the schema for the table containing the primary key.
* TABLE_NAME - Name of the table containing the primary key.
* COLUMN_NAME - Name of the column containing the primary key.
* KEY_SEQ - 1-indexed position of the column in the key.
* PK_NAME - The name of the primary key.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

stmt = ibm_db.exec_immediate(conn,"drop table test_primary_keys")
statement = 'CREATE TABLE test_primary_keys (id INTEGER NOT NULL, PRIMARY KEY(id))'
result = ibm_db.exec_immediate(conn, statement)
stmt = ibm_db.primary_keys(conn, None, None, 'TEST_PRIMARY_KEYS')
row = ibm_db.fetch_tuple(stmt)
print("{} is primary key in table {} with index position {} in the key".format(row[3],row[2],row[4]))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-primary_keys.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_025_PrimaryKeys.py)

### ibm_db.procedure_columns ###
`IBM_DBStatement ibm_db.procedure_columns ( IBM_DBConnection connection, string qualifier, string schema, string procedure, string parameter )`

**Description**

Returns a result set listing the parameters for one or more stored procedures

**Parameters**

* connection - A valid IBM_DBConnection
* qualifier - A qualifier for DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* schema - The schema which contains the procedures. This parameter accepts a search pattern containing _and % as wildcards.
* procedure - The name of the procedure. This parameter accepts a search pattern containing_ and % as wildcards.
* parameter - The name of the parameter. This parameter accepts a search pattern containing _and % as wildcards. If this parameter is `None`, all parameters for the specified stored procedures are returned.

**Return Values**

Returns an IBM_DBStatement with a result set containing the following columns:
* PROCEDURE_CAT - The catalog that contains the procedure. The value is `None` if this table does not have catalogs.
* PROCEDURE_SCHEM - Name of the schema that contains the stored procedure.
* PROCEDURE_NAME - Name of the procedure.
* COLUMN_NAME - Name of the parameter.
* COLUMN_TYPE - An integer value representing the type of the parameter:
    * 1 (`SQL_PARAM_INPUT`) - Input (IN) parameter.
    * 2 (`SQL_PARAM_INPUT`_OUTPUT) - Input/output (INOUT) parameter.
    * 3 (`SQL_PARAM_OUTPUT`) - Output (OUT) parameter.
* DATA_TYPE - The SQL data type for the parameter represented as an integer value.
* TYPE_NAME - A string representing the data type for the parameter.
* COLUMN_SIZE - An integer value representing the size of the parameter.
* BUFFER_LENGTH - Maximum number of bytes necessary to store data for this parameter.
* DECIMAL_DIGITS - The scale of the parameter, or `None` where scale is not applicable.
* NUM_PREC_RADIX - An integer value of either 10 (representing an exact numeric data type), 2 (representing anapproximate numeric data type), or `None` (representing a data type for which radix is not applicable).
* NULLABLE - An integer value representing whether the parameter is nullable or not.
* REMARKS - Description of the parameter.
* COLUMN_DEF - Default value for the parameter.
* SQL_DATA_TYPE - An integer value representing the size of the parameter.
* SQL_DATETIME_SUB - Returns an integer value representing a datetime subtype code, or `None` for SQL data types to which this does not apply.
* CHAR_OCTET_LENGTH - Maximum length in octets for a character data type parameter, which matches COLUMN_SIZE for single-byte character set data, or `None` for non-character data types.
* ORDINAL_POSITION - The 1-indexed position of the parameter in the CALL statement.
* IS_NULLABLE - A string value where 'YES' means that the parameter accepts or returns `None` values and 'NO' means that the parameter does not accept or return `None` values.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql="""create or replace procedure proc(OUT out1 integer) dynamic result sets 1 begin  select id into out1 from tabmany where id=1; end"""
ibm_db.exec_immediate(conn, sql)
# note the procedure name upper case
resultSet = ibm_db.procedure_columns(conn, None, '', 'PROC', None)
#print(resultSet)
row = ibm_db.fetch_assoc(resultSet)
while row:
    print(row)
    print("Procedure {} is having one output parameter with name {}\n".format(row['PROCEDURE_NAME'], row['COLUMN_NAME']))
    row = ibm_db.fetch_assoc(resultSet)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-procedure_columns.py)

### ibm_db.procedures ###

**Description**

resource ibm_db.procedures ( IBM_DBConnection connection, string qualifier,
string schema, string procedure )
Returns a result set listing the stored procedures registered in a database.

**Parameters**

* connection - A valid IBM_DBConnection
* qualifier - A qualifier for DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* schema - The schema which contains the procedures. This parameter accepts a search pattern containing _and % as wildcards.
* procedure - The name of the procedure. This parameter accepts a search pattern containing_ and % as wildcards.

**Return Values**

Returns an IBM_DBStatement with a result set containing the following columns:
* PROCEDURE_CAT - The catalog that contains the procedure. The value is `None` if this table does not have catalogs.
* PROCEDURE_SCHEM - Name of the schema that contains the stored procedure.
* PROCEDURE_NAME - Name of the procedure.
* NUM_INPUT_PARAMS - Number of input (IN) parameters for the stored procedure.
* NUM_OUTPUT_PARAMS - Number of output (OUT) parameters for the stored procedure.
* NUM_RESULT_SETS - Number of result sets returned by the stored procedure.
* REMARKS - Any comments about the stored procedure.
* PROCEDURE_TYPE - Always returns 1, indicating that the stored procedure does not return a return value.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

schemaName = 'DB2ADMIN'
resultSet = ibm_db.procedures(conn, None, schemaName, 'PROC')
row = ibm_db.fetch_assoc(resultSet)
while row:
    print(row)
    row = ibm_db.fetch_assoc(resultSet)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-procedures.py)

### ibm_db.recreatedb ###
`bool ibm_db.recreatedb ( IBM_DBConnection connection, string dbName [, codeSet, mode] )`

**Description**

Drop and then recreates a database by using the specified database name, code set, and mode

**Parameters**

* connection - A valid IBM_DBConnection as returned from ibm_db.connect() by specifying the ATTACH keyword
* dbName - Name of the database that is to be created.
* codeSet - Database code set information. Note: If the value of the codeSet argument not specified, the database is created in the Unicode code page for DB2 data servers and in the UTF-8 code page for IDS data servers.
* mode - Database logging mode. Note: This value is applicable only to IDS data servers.

**Return Value**

Returns `True` if specified database created successfully else return `None`.

**Example**
```python
import ibm_db
conn_str_attach = "attach=true;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password"
database='test123'
conn_attach = ibm_db.connect(conn_str_attach, '', '')

rc = ibm_db.recreatedb(conn_attach, database)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-recreatedb_REMOTE.py),
[Example2](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-recreatedb_LOCAL.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_recreateDB.py)

### ibm_db.result ###
`mixed ibm_db.result ( IBM_DBStatement stmt, mixed column )`

**Description**

Returns a single column from a row in the result set
Use ibm_db.result() to return the value of a specified column in the current  **row of a result set. You must call ibm_db.fetch_row() before calling
ibm_db.result() to set the location of the result set pointer.

**Parameters**

* stmt - A valid stmt resource.
* column - Either an integer mapping to the 0-indexed field in the result set, or a string matching the name of the column.

**Return Values**

Returns the value of the requested field if the field exists in the result
set. Returns `None` if the field does not exist, and issues a warning.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

sql = "select id, name from tabmany"
stmt = ibm_db.exec_immediate(conn, sql)
while (ibm_db.fetch_row(stmt)):
    id = ibm_db.result(stmt, "ID")
    name = ibm_db.result(stmt, "NAME")
    print("col1 = {}, col2 = {}".format(id, name))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-result.py),
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_03a_ResultNonExistCol.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_031_ResultIndexPosition.py)

### ibm_db.rollback ###

**Description**

bool ibm_db.rollback ( IBM_DBConnection connection )
Rolls back an in-progress transaction on the specified IBM_DBConnection
and begins a new transaction. Python applications normally default to
AUTOCOMMIT mode, so ibm_db.rollback() normally has no effect unless
AUTOCOMMIT has been turned off for the IBM_DBConnection.
Note: If the specified IBM_DBConnection is a persistent connection, all
transactions in progress for all applications using that persistent
connection will be rolled back. For this reason, persistent connections are
not recommended for use in applications that require transactions.

**Parameters**

* connection - A valid IBM_DBConnection

**Return Values**

Returns `True` on success or `False` on failure.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','',{ibm_db.SQL_ATTR_AUTOCOMMIT:  ibm_db.SQL_AUTOCOMMIT_OFF})

sql = "insert into tabmany values(100, 'Testrollback')"
stmt = ibm_db.exec_immediate(conn, sql)
sql = "select name from tabmany where id=100"
stmt = ibm_db.exec_immediate(conn, sql)
res = ibm_db.fetch_tuple(stmt)
print(res)

# rollback
rc = ibm_db.rollback(conn)

# again fetch the data, should see empty row
stmt1 = ibm_db.exec_immediate(conn, sql)
res1 = ibm_db.fetch_tuple(stmt1)
print(res1)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-rollback.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_021_CommitDelete.py)

### ibm_db.server_info ###
`IBM_DBServerInfo ibm_db.server_info ( IBM_DBConnection connection )`

**Description**

Returns a read-only object with information about the IBM DB2 or Informix server.

**Parameters**
* connection - A valid IBM_DBConnection

**Return Values**
* On success, an object with the following fields:
    * DBMS_NAME - The name of the database server to which you are connected. For DB2 servers this is a combination of DB2 followed by the operating system on which the database server is running. (string)
    * DBMS_VER - The version of the database server, in the form of a string "MM.mm.uuuu" where MM is the major version, mm is the minor version, and uuuu is the update. For example, "08.02.0001" represents major version 8, minor version 2, update 1. (string)
    * DB_CODEPAGE - The code page of the database to which you are connected. (int)
    * DB_NAME - The name of the database to which you are connected. (string)
    * DFT_ISOLATION - The default transaction isolation level supported by the server: (string)
        * UR - Uncommitted read: changes are immediately visible by all concurrent transactions.
        * CS - Cursor stability: a row read by one transaction can be altered and committed by a second concurrent transaction.
        * RS - Read stability: a transaction can add or remove rows matching a search condition or a pending transaction.
        * RR - Repeatable read: data affected by pending transaction is not available to other transactions.
        * NC - No commit: any changes are visible at the end of a successful operation. Explicit commits and rollbacks are not allowed.
    * IDENTIFIER_QUOTE_CHAR - The character used to delimit an identifier. (string)
    * INST_NAME - The instance on the database server that contains the database. (string)
    * ISOLATION_OPTION - A tuple of the isolation options supported by the database server. The isolation options are described in the DFT_ISOLATION property. (tuple)
    * KEYWORDS - A tuple of the keywords reserved by the database server. (tuple)
    * LIKE_ESCAPE_CLAUSE - `True` if the database server supports the use of % and _wildcard characters. `False` if the database server does not support these wildcard characters. (bool)
    * MAX_COL_NAME_LEN - Maximum length of a column name supported by the database server, expressed in bytes. (int)
    * MAX_IDENTIFIER_LEN - Maximum length of an SQL identifier supported by the database server, expressed in characters. (int)
    * MAX_INDEX_SIZE - Maximum size of columns combined in an index supported by the database server, expressed in bytes. (int)
    * MAX_PROC_NAME_LEN - Maximum length of a procedure name supported by the database server, expressed in bytes. (int)
    * MAX_ROW_SIZE - Maximum length of a row in a base table supported by the database server, expressed in bytes. (int)
    * MAX_SCHEMA_NAME_LEN - Maximum length of a schema name supported by the database server, expressed in bytes. (int)
    * MAX_STATEMENT_LEN - Maximum length of an SQL statement supported by the database server, expressed in bytes. (int)
    * MAX_TABLE_NAME_LEN - Maximum length of a table name supported by the database server, expressed in bytes. (bool)
    * NON_NULLABLE_COLUMNS - `True` if the database server supports columns that can be defined as NOT NULL, `False` if the database server does not support columns defined as NOT NULL. (bool)
    * PROCEDURES - `True` if the database server supports the use of the CALL statement to call stored procedures, `False` if the database server does not support the CALL statement. (bool)
    * SPECIAL_CHARS - A string containing all of the characters other than A-Z, 0-9, and underscore that can be used in an identifier name. (string)
    * SQL_CONFORMANCE - The level of conformance to the ANSI/ISO SQL-92 specification offered by the database server: (string)
        * ENTRY - Entry-level SQL-92 compliance.
        * FIPS127 - FIPS-127-2 transitional compliance.
        * FULL - Full level SQL-92 compliance.
        * INTERMEDIATE - Intermediate level SQL-92 compliance.
* On failure, `False`

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

serverInfo = ibm_db.server_info(conn)
print("Db2 database server name                 : {}" .format(serverInfo.DBMS_NAME))
print("Database name                            : {}" .format(serverInfo.DB_NAME))
print("Db2 instance name                        : {}" .format(serverInfo.INST_NAME))
print("Database codepage used                   : {}" .format(serverInfo.DB_CODEPAGE))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-server_info.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_300_ServerInfo.py)

### ibm_db.set_option ###
`bool ibm_db.set_option ( mixed resc, dict options, int type )`

**Description**

Sets options for a IBM_DBConnection or IBM_DBStatement. You cannot set options for result set resources.

**Parameters**
* resc - A valid IBM_DBConnection or IBM_DBStatement.
* options - The options to be set
* type - A field that specifies the type of resc
    * 0 - IBM_DBStatement
    * 1 - IBM_DBConnection

**Return Values**

Returns `True` on success or `False` on failure

**Example**
```python
import ibm_db
conn_options = { ibm_db.SQL_ATTR_INFO_PROGRAMNAME : 'TestProgram'}
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','', conn_options)

value=ibm_db.get_option(conn, ibm_db.SQL_ATTR_INFO_PROGRAMNAME, 1)
print("Connection options:\nSQL_ATTR_INFO_PROGRAMNAME = {}".format(value), end="\n")
returncode=ibm_db.set_option(conn, {ibm_db.SQL_ATTR_AUTOCOMMIT:0},1)
value=ibm_db.get_option(conn, ibm_db.SQL_ATTR_AUTOCOMMIT, 1)
print("SQL_ATTR_AUTOCOMMIT = {}".format(str(value)), end="\n")

# statement options
stmt = ibm_db.prepare(conn, "select * from tabmany")
returnCode = ibm_db.set_option(stmt, {ibm_db.SQL_ATTR_QUERY_TIMEOUT : 20}, 0)
value = ibm_db.get_option(stmt, ibm_db.SQL_ATTR_QUERY_TIMEOUT, 0)
print("Statement options:\nSQL_ATTR_QUERY_TIMEOUT = {}".format(str(value)), end="\n")
result = ibm_db.execute(stmt)

if result:
    ibm_db.free_result(stmt)
else:
    print(ibm_db..stmt_errormsg())
ibm_db.rollback(conn)
ibm_db.close(conn)
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-set_option_CONNECTION.py),
[Example2](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-set_option_STATEMENT.py),
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_setgetOption.py)

### ibm_db.special_columns ###
`IBM_DBStatement ibm_db.special_columns ( IBM_DBConnection connection, string qualifier, string schema, string table_name, int scope )`

**Description**

Returns a result set listing the unique row identifier columns for a table.

**Parameters**
* connection - A valid IBM_DBConnection
* qualifier - A qualifier for DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* schema - The schema which contains the tables.
* table_name - The name of the table.
* scope - Integer value representing the minimum duration for which the unique row identifier is valid. This can be one of the following values:
    * 0 - Row identifier is valid only while the cursor is positioned on the row. (SQL_SCOPE_CURROW)
    * 1 - Row identifier is valid for the duration of the transaction. (SQL_SCOPE_TRANSACTION)
    * 2 - Row identifier is valid for the duration of the connection. (SQL_SCOPE_SESSION)

**Return Values**

Returns an IBM_DBStatement with a result set containing the following columns:
* SCOPE - Integer value representing the minimum duration for which the unique row identifier is valid.
    * 0 (SQL_SCOPE_CURROW) - Row identifier is valid only while the cursor is positioned on the row.
    * 1 (SQL_SCOPE_TRANSACTION) - Row identifier is valid for the duration of the transaction.
    * 2 (SQL_SCOPE_SESSION) - Row identifier is valid for the duration of the connection.
* COLUMN_NAME - Name of the unique column.
* DATA_TYPE - SQL data type for the column.
* TYPE_NAME - Character string representation of the SQL data type for thecolumn.
* COLUMN_SIZE - An integer value representing the size of the column.
* BUFFER_LENGTH - Maximum number of bytes necessary to store data from thiscolumn.
* DECIMAL_DIGITS - The scale of the column, or `None` where scale is notapplicable.
* NUM_PREC_RADIX - An integer value of either 10 (representing an exact numeric data type), 2 (representing an approximate numeric data type), or `None` (representing a data type for which radix is not applicable).
* PSEUDO_COLUMN - Always returns 1.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

schemaName = "DB2ADMIN"
tableName = "TABMANY"
resultSet = ibm_db.special_columns(conn, None, schemaName, tableName, 0)
dataRecord = ibm_db.fetch_assoc(resultSet)
while dataRecord:
    print("Column name            : {}" .format(dataRecord['COLUMN_NAME']))
    print("Data type              : {}" .format(dataRecord['TYPE_NAME']))
    print("Column size            : {}" .format(dataRecord['COLUMN_SIZE']))	
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-special_columns.py)

### ibm_db.statistics ###
`IBM_DBStatement ibm_db.statistics ( IBM_DBConnection connection, string qualifier, string schema, string table-name, bool unique )`

**Description**

Returns a result set listing the index and statistics for a table.

**Parameters**
* connection - A valid IBM_DBConnection
* qualifier - A qualifier for DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* schema - The schema that contains the table. If this parameter is `None`, the statistics and indexes are returned for the schema of the current user.
* table_name The name of the table.
* unique A boolean value representing the type of index information to return.
    * `False` -  Return only the information for unique indexes on the table.
    * `True` - Return the information for all indexes on the table.

**Return Values**

Returns an IBM_DBStatement with a result set containing the following columns:
* TABLE_CAT - The catalog that contains the table. The value is `None` if this table does not have catalogs.
* TABLE_SCHEM - Name of the schema that contains the table.
* TABLE_NAME - Name of the table.
* NON_UNIQUE - An integer value representing whether the index prohibits unique values, or whether the row represents statistics on the table itself:
    * 0 (SQL_FALSE) - The index allows duplicate values.
    * 1 (SQL_TRUE) - The index values must be unique.
    * None - This row is statistics information for the table itself.
* INDEX_QUALIFIER - A string value representing the qualifier that would have to be prepended to INDEX_NAME to fully qualify the index.
* INDEX_NAME - A string representing the name of the index.
* TYPE - An integer value representing the type of information contained in this row of the result set:
    * 0 (SQL_TABLE_STAT) - The row contains statistics about the table itself.
    * 1 (SQL_INDEX_CLUSTERED) - The row contains information about a clustered index.
    * 2 (SQL_INDEX_HASH) - The row contains information about a hashed index.
    * 3 (SQL_INDEX_OTHER) - The row contains information about a type of index that is neither clustered nor hashed.
* ORDINAL_POSITION - The 1-indexed position of the column in the index. `None` if the row contains statistics information about the table itself.
* COLUMN_NAME - The name of the column in the index. `None` if the row contains statistics information about the table itself.
* ASC_OR_DESC - A if the column is sorted in ascending order, D if the column is sorted in descending order, `None` if the row contains statistics information about the table itself.
* CARDINALITY - If the row contains information about an index, this column contains an integer value representing the number of unique values in the index. If the row contains information about the table itself, this column contains an integer value representing the number of rows in the table.
* PAGES - If the row contains information about an index, this column contains an integer value representing the number of pages used to store the index. If the row contains information about the table itself, this column contains an integer value representing the number of pages used to store the table.
* FILTER_CONDITION - Always returns `None`.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

create_table = "create table index_test(id int, data VARCHAR(50))"
rc = ibm_db.exec_immediate(conn, create_table)
create_index = "CREATE UNIQUE INDEX index1 ON index_test (id)"
rc = ibm_db.exec_immediate(conn, create_index)

schemaName = "DB2ADMIN"
tableName = "INDEX_TEST"
resultSet = ibm_db.statistics(conn, None, schemaName, tableName, True)
dataRecord = ibm_db.fetch_assoc(resultSet)
while dataRecord['INDEX_NAME'] is not None:
    print("Table Schema            : {}" .format(dataRecord['TABLE_SCHEM']))
    print("Table name              : {}" .format(dataRecord['TABLE_NAME']))
    print("Index qualifier            : {}" .format(dataRecord['INDEX_QUALIFIER']))
    print("Index name                       : {}" .format(dataRecord['INDEX_NAME']))
    print("Column name                      : {}" .format(dataRecord['COLUMN_NAME']))
    print("Column position in index         : {}" .format(dataRecord['ORDINAL_POSITION']))
    dataRecord = ibm_db.fetch_assoc(resultSet)	
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-statistics.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_197_StatisticsIndexes.py)

### ibm_db.stmt_error ###
`string ibm_db.stmt_error ( [IBM_DBStatement stmt] )`

**Description**

When not passed any parameters, returns the SQLSTATE representing the reason
the last attempt to return an IBM_DBStatement via ibm_db.prepare(),
ibm_db.exec_immediate(), or ibm_db.callproc() failed.

When passed a valid IBM_DBStatement, returns the SQLSTATE representing the
reason the last operation using the resource failed.

**Parameters**
* stmt - A valid IBM_DBStatement.

**Return Values**

Returns a string containing the SQLSTATE value or an empty string if there was no error.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

create_table = "create table index_test(id int, data VARCHAR(50)"
try:
    rc = ibm_db.exec_immediate(conn, create_table)
except:
    print("Query ' {} ' failed with ".format(create_table))
    print("SQLSTATE = {}".format(ibm_db.stmt_error()))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-stmt_error.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_6561_InsertNULLValues.py)

### ibm_db.stmt_errormsg ###
`string ibm_db.stmt_errormsg ( [IBM_DBStatement stmt] )`

**Description**


When not passed any parameters, returns a string containing
the SQLCODE and error message representing the reason
the last attempt to return an IBM_DBStatement via ibm_db.prepare(),
ibm_db.exec_immediate(), or ibm_db.callproc() failed.

When passed a valid IBM_DBStatement, returns a string containing
the SQLCODE and error message representing the reason the last
operation using the resource failed.

**Parameters**
* stmt - A valid IBM_DBStatement.

**Return Values**

Returns a string containing the SQLCODE and error message or an empty string if there was no error.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

create_table = "create table index_test(id int, data VARCHAR(50)"
try:
    rc = ibm_db.exec_immediate(conn, create_table)
except:
    print("Query ' {} ' failed with ".format(create_table))
    print("Error : {}".format(ibm_db.stmt_errormsg()))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-stmt_errormsg.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_180_StmtErrMsg.py)

### ibm_db.table_privileges ###
`IBM_DBStatement ibm_db.table_privileges ( IBM_DBConnection connection [, string qualifier [, string schema [, string table_name]]] )`

**Description**

Returns a result set listing the tables and associated privileges in a database.

**Parameters**
* connection - A valid IBM_DBConnection
* qualifier - A qualifier for DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* schema - The schema which contains the tables. This parameter accepts a search pattern containing _and % as wildcards.
* table_name - The name of the table. This parameter accepts a search pattern containing_ and % as wildcards.

**Return Values**

Returns an IBM_DBStatement with a result set containing following columns:
* TABLE_CAT - The catalog that contains the table. The value is `None` if this table does not have catalogs.
* TABLE_SCHEM - Name of the schema that contains the table.
* TABLE_NAME - Name of the table.
* GRANTOR - Authorization ID of the user who granted the privilege.
* GRANTEE - Authorization ID of the user to whom the privilege was granted.
* PRIVILEGE - The privilege that has been granted. This can be one of ALTER, CONTROL, DELETE, INDEX, INSERT, REFERENCES, SELECT, or UPDATE.
* IS_GRANTABLE - A string value of "YES" or "NO" indicating whether the grantee can grant the privilege to other users.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

schemaName = "DB2ADMIN"
tableName = "TABMANY"
resultSet = ibm_db.table_privileges(conn, None, schemaName, tableName)
dataRecord = ibm_db.fetch_assoc(resultSet)
print("Schema name            : {}" .format(dataRecord['TABLE_SCHEM']))
print("Table name             : {}" .format(dataRecord['TABLE_NAME']))
print("Privilege grantor      : {}" .format(dataRecord['GRANTOR']))
print("Privilege recipient    : {}" .format(dataRecord['GRANTEE']))
print("Privilege              : {}" .format(dataRecord['PRIVILEGE']))
print("Privilege is grantable : {}" .format(dataRecord['IS_GRANTABLE']))
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-table_privileges.py)

### ibm_db.tables ###
`IBM_DBStatement ibm_db.tables ( IBM_DBConnection connection [, string qualifier [, string schema [, string table-name [, string table-type]]]] )`

**Description**

Returns a result set listing the tables and associated metadata in a database

**Parameters**

* connection - A valid IBM_DBConnection
* qualifier - A qualifier for DB2 databases running on OS/390 or z/OS servers. For other databases, pass `None` or an empty string.
* schema - The schema which contains the tables. This parameter accepts a search pattern containing _and % as wildcards.
* table-name - The name of the table. This parameter accepts a search pattern containing_ and % as wildcards.
* table-type - A list of comma-delimited table type identifiers. To match all table types, pass `None` or an empty string.
    * ALIAS
    * HIERARCHY TABLE
    * INOPERATIVE VIEW
    * NICKNAME
    * MATERIALIZED QUERY TABLE
    * SYSTEM TABLE
    * TABLE
    * TYPED TABLE
    * TYPED VIEW
    * VIEW

**Return Values**

Returns an IBM_DBStatement with a result set containing the following columns:
* TABLE_CAT - The catalog that contains the table. The value is `None` if this table does not have catalogs.
* TABLE_SCHEMA - Name of the schema that contains the table.
* TABLE_NAME - Name of the table.
* TABLE_TYPE - Table type identifier for the table.
* REMARKS - Description of the table.

**Example**
```python
import ibm_db
conn=ibm_db.connect("DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password",'','')

schemaName = "DB2ADMIN"
resultSet = ibm_db.tables(conn, None, schemaName, 'TAB%', 'TABLE')
dataRecord = ibm_db.fetch_assoc(resultSet)
while dataRecord:
    print("Table schema  : {}" .format(dataRecord['TABLE_SCHEM']))
    print("Table name    : {}" .format(dataRecord['TABLE_NAME']))
    print("Table type    : {}" .format(dataRecord['TABLE_TYPE']))
    print("Description   : {}" .format(dataRecord['REMARKS']))
    dataRecord = ibm_db.fetch_assoc(resultSet)
    print("------------------------------------------------------")	
```
Other examples:
[Example1](https://github.com/IBM/db2-python/blob/master/Python_Examples/ibm_db/ibm_db-tables.py)

### Context manager with connection object ###

Using a context manager with a connection object is a great way to ensure that resources are properly managed and cleaned up, especially in scenarios such as database connections where it's crucial to handle connections properly.
Context manager can be achieved using python with statement.
The Python with statement creates a runtime context that allows  to run a group of statements under the control of a context manager. 

Below is an example of context manager for managing the ibm_db connection: 

```
import ibm_db
import ibm_db_ctx

conn_str = "DATABASE=database;HOSTNAME=hostname;PORT=port;PROTOCOL=TCPIP;UID=username;PWD=password"
with ibm_db_ctx.Db2connect(conn_str, '','') as conn:
    stmt = ibm_db.exec_immediate(conn, "SELECT * FROM my_table")
    while ibm_db.fetch_row(stmt):
        row = ibm_db.fetch_tuple(stmt)
        print(row)
```


Creates an instance of Db2connect with 'conn_str'.Inside with' block, 'conn' represents the active database connection object.
And perfomrs the database operations such as executing query (ibm_db.exec_immediate) and fetching results (ibm_db.fetch_row and ibm_db.fetch_tuple).
The connection object is active only within with block.
The connection gets automatically closed once the with block execution completed.

Other examples:
[Example1](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_context_ConnDb.py)
[Example2](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_context_ConnDbUncatalogedConn.py)
[Example3](https://github.com/ibmdb/python-ibmdb/blob/master/ibm_db_tests/test_context_ConnActive.py)


### Supported Options ###
Python ibm_db driver supports only a subset of Db2 ODBC and CLI Driver's connection and statement level attributes. However, you can set other supported configuration keywords through db2dsdriver.cfg file. Refer to [db2dsdriver.cfg configuration keywords](https://www.ibm.com/support/knowledgecenter/en/SSEPGG_11.1.0/com.ibm.swg.im.dbclient.config.doc/doc/c0054698.html) for more details.

Connection Options:
* SQL_ATTR_AUTOCOMMIT
* SQL_ATTR_CURSOR_TYPE
* SQL_ATTR_INFO_PROGRAMNAME
* SQL_ATTR_USE_TRUSTED_CONTEXT
* SQL_ATTR_TRUSTED_CONTEXT_USERID
* SQL_ATTR_TRUSTED_CONTEXT_PASSWORD
* SQL_ATTR_CURRENT_SCHEMA
* SQL_ATTR_INFO_USERID
* SQL_ATTR_INFO_WRKSTNNAME
* SQL_ATTR_INFO_ACCTSTR
* SQL_ATTR_INFO_APPLNAME


Statement Options:
* SQL_ATTR_ROWCOUNT_PREFETCH
* SQL_ATTR_QUERY_TIMEOUT