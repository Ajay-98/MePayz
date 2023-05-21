import pyodbc
import pandas

cnxn = pyodbc.connect(Driver='{SQL Server}',
                      Server='DESKTOP-M0S2O65',
                      Database='Blop',
                      Trusted_Connection='tcon')

def store_in_DB(row_insert):
    sql = "INSERT into STMT_Data (STMT_Lines) values ( ? )"
    val = (row_insert)
    cnxn.execute(sql, val)
    cnxn.commit()

def ext_from_DB():
    sql = " Select STMT_Lines from STMT_Data"
    all_rows = cnxn.execute(sql).fetchall()
    return all_rows
def close():
    cnxn.close()
