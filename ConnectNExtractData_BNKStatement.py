import string
from PyPDF2 import PdfReader
import regex
import pandas as pd

pdf_1 = PdfReader("Src.pdf")
pdf_1.decrypt("AJAY890458587")
bal_ = list()
party_ = list()
#lt_ = regex.split(r'\d\d\-\d\d\-\d\d\d\d', pdf_1.pages[0].extractText(0))
lt_ = pdf_1.pages[0].extractText(0)
print(lt_)
with open('extract.txt','w') as f:
    for i in lt_[3:]:
        print(i)
        bal = regex.search(r'(\b\d+\.\d+\b)(?!.*(\b\d+\.\d+\b))', i).group()
        bal_.append(bal)

pd_ = pd.DataFrame(bal_, columns=['Balance'])
print(pd_)
f.close()
