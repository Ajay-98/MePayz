# Dev by AJM
# Extracting the Raw data from Bank Statement and store it in my SQL and also data processing the data, Followed by Storing the processed data and mailing it.
import re

import PyPDF2
import regex
import Connectors.SQL_Connectors as sql_conn
# Converting the Raw data from PDF to TXT.
PDF_Obj = open('C:\\Users\\Acer\\PycharmProjects\\Automation_Scripts\\Src.pdf', 'rb')
Src_txt = open('C:\\Users\\Acer\\PycharmProjects\\Automation_Scripts\\extract.txt', 'w')
ext_flag = False
tw_ln_marker = [False, False]  # Line Marking Indicator
a_ln_string = ''  # to build a proper line in a statement

date_re = regex.compile(r"(\d{2}\-\d{2}\-\d{4})")  # Regex engine for matching date pattern
Match_grp_re = regex.compile(r"(\d{2}\-\d{2}\-\d{4}).*(\d{3})$")
# money_re = regex.compile(r"(\d+\.\d+)")
# Balance_re = regex.compile(r"(\d{3})")           # Regex engine for matching for Init BR

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
                    sql_conn.store_in_DB(a_ln_string)
                    a_ln_string = ''
                a_ln_string = a_ln_string + line.strip()
            tw_ln_marker[0] = tw_ln_marker[1]
            tw_ln_marker[1] = False


# txt_extract()
# Start the DB processing
row_data_lt = sql_conn.ext_from_DB()
for row in row_data_lt:
    str_ = row[0]
    print('*********')
    try:
        stripped_lst = [x.strip() for x in str_.split(" ") if x != '']
        lst_len = len(stripped_lst)
        Date_ = date_re.match(stripped_lst[0]).group(1)  #Extract the date
        print(lst_len)
        info_ = date_re.sub(stripped_lst[0], "")
        print(Date_ + " -- " + info_ + " " + stripped_lst[lst_len-2])
    except Exception as e:
        print(str_)

sql_conn.close()