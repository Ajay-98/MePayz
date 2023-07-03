from sqlalchemy import Column, String, Date, Float, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
URI = 'mssql+pyodbc://DESKTOP-M0S2O65/blop?driver=SQL+Server'

class stmt_info(Base):
    __tablename__ = "STMT_Info"

    date_ = Column("dated_on", Date, primary_key = True)
    paid_to = Column("paid_to", String)
    stmt_desc = Column("Stmt_desc", String)
    balance_amt = Column("balance_amt", Float)

    def __int__(self, date, paid_to, stmt_desc, balance_amt):
        date_ = self.date
        paid_to = self.paid_to
        stmt_desc = self.stmt_desc
        balance_amt = self.balance_amt

# Initialize MSSQL DB connection.
engine_ = create_engine(URI, echo = True)
Base.metadata.create_all(bind=engine_)

Session = sessionmaker(bind=engine_)
session = Session()

# get all balance amunts
get_all = session.query(stmt_info).all()

# Get grouped balance mat, for each dates.
get_grouped = session.query(stmt_info).select_from(stmt_info.date_).group_by(stmt_info.date_).all()
for i in get_grouped:
    print(i.date_)

session.close_all()