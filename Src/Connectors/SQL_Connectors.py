import pyodbc
import pandas

cnxn = pyodbc.connect(Driver='{SQL Server}',
                      Server='DESKTOP-M0S2O65',
                      Database='Blop',
                      Trusted_Connection='tcon')

def store_in_DB(row_insert, table_name):
    print("IN Store func")
    if table_name == 'STMT_Data':
        sql = "INSERT into STMT_Data (STMT_Lines) values ( ? )"
        val = row_insert
        cnxn.execute(sql, val)
    elif table_name == 'Stmt_Info':
        sql = """INSERT INTO [dbo].[Stmt_Details]
           ([Date]
           ,[Paid_to]
           ,[Description]
           ,[Balance_amt])
     VALUES
           (?
           ,?
           ,?
           ,?)"""
        #print("INserting now " + (row_insert.date, row_insert.paid_to, row_insert.desc, row_insert.balance))
        cnxn.execute(sql,(row_insert.date, row_insert.paid_to, row_insert.desc, row_insert.balance) )
    cnxn.commit()

def ext_from_DB(query_action):
    select_all_data = " Select STMT_Lines from STMT_Data"
    select_all_details = " Select * from STMT_info"
    if query_action == 'select_all_data':
        all_rows = cnxn.execute(select_all_data).fetchall()
    elif query_action == 'select_all_details':
        all_rows = cnxn.execute(select_all_details).fetchall()
    return all_rows
def close():
    cnxn.close()
