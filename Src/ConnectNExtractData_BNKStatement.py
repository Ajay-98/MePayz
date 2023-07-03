# Dev by AJM
# Extracting the Raw data from Bank Statement and store it in my SQL and also data processing the data, Followed by Storing the processed data and mailing it.
import datetime
import re

import matplotlib.pyplot as pypt
import PyPDF2
import regex
import Connectors.SQL_Connectors as sql_conn
# Converting the Raw data from PDF to TXT.
PDF_Obj = open('C:\\Users\\Acer\\PycharmProjects\\Automation_Scripts\\Src.pdf', 'rb')
Src_txt = open('C:\\Users\\Acer\\PycharmProjects\\Automation_Scripts\\extract.txt', 'w')
audit_file = open("Auditing_file.txt", 'w')
e_i = 0
ext_flag = False
tw_ln_marker = [False, False]  # Line Marking Indicator
a_ln_string = ''  # to build a proper line in a statement
class Row_entity:
    def __init__(self, date, balance, desc, paid_to, exp):
        self.date = datetime.datetime.strptime(date, '%d-%m-%Y')
        self.balance = balance
        self.desc = desc
        self.paid_to = paid_to
        self.exp = exp

date_re = regex.compile(r"(\d{2}\-\d{2}\-\d{4})")  # Regex engine for matching date pattern
Match_grp_re = regex.compile(r"(\d{2}\-\d{2}\-\d{4}).*(\d{3})$")

P_R = PyPDF2.PdfFileReader(PDF_Obj)  # PDF Reader

P_R.decrypt("AJAY890458587")
no_p = P_R.numPages

for i in range(no_p):
    page_txt_contents = P_R.getPage(i).extract_text()
    Src_txt.writelines(page_txt_contents)
    Src_txt.write('\n')

Src_txt.write('END OF LINE')

Src_txt.close()

def txt_extract():
    global ext_flag
    global a_ln_string
    with open(
            'C:\\Users\\Acer\\PycharmProjects\\Automation_Scripts\\extract.txt') as file:  # func to Extrac the RAW data to DB
        for line in file:
            # Processing the lines, with regex
            patt = 'OPENING BALANCE|CLOSING BALANCE'
            x = regex.match(patt, line)
            if x is not None:  # indicator flipper to turn off the extract processing
                print('FLAG flipped for kicking off Data EXT into DB')
                ext_flag = not ext_flag
            if ext_flag:  # if enabled, that line can be processed
                if date_re.search(line):
                    tw_ln_marker[1] = not tw_ln_marker[1]
                    sql_conn.store_in_DB(a_ln_string, "Stmt_Data")
                    a_ln_string = ''
                a_ln_string = a_ln_string + line.strip()
            tw_ln_marker[0] = tw_ln_marker[1]
            tw_ln_marker[1] = False


#txt_extract()
# Start the DB processing
row_data_lt = sql_conn.ext_from_DB("select_all_data")
prev_balance = 0.0
for row in row_data_lt:
    str_ = row[0]
    try:
        stripped_lst = [x.strip() for x in str_.split(" ") if x != '']
        lst_len = len(stripped_lst)
        Date_ = date_re.match(stripped_lst[0]).group(1)  #Extract the date
        str_0 = date_re.split(stripped_lst[0])[2]
        for i in range(1, lst_len-3):
            str_0 = str_0 + stripped_lst[i]
        print(stripped_lst[lst_len-2])
        exp = float(stripped_lst[lst_len-2]) - prev_balance # Expenditure is current Balance - Previous balance
        row_insert = Row_entity(Date_,stripped_lst[lst_len-2], "TBD", "TBD", exp)
        prev_balance = float(stripped_lst[lst_len-2])
        sql_conn.store_in_DB(row_insert, "Stmt_Info")
    except Exception as e:      #AttributeError
        audit_file.write(str(e_i) + ")"+"      " + stripped_lst[lst_len-2] +  'Thrown error, causing issue')
        e_i = e_i + 1
del row_data_lt
audit_file.close()
row_data_lt = sql_conn.ext_from_DB("select_all_details")


sql_conn.close()