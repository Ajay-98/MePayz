import os
import pymysql
from sqlalchemy import text, create_engine, engine, Table
import sqlalchemy as db


#URI = "mysql+pymysql://localhost:3306/blop"
URL = 'mssql+pyodbc://DESKTOP-M0S2O65/blop?driver=SQL+Server'
engine_ = db.create_engine(URL)
metadata = db.MetaData()
conn = engine_.connect()
blob_T = Table('blop',metadata, autoload_with=engine)
print(blob_T.columns.keys)
conn.close()