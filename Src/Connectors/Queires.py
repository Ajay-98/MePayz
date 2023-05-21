
import regex

str = "02-06-2022UPI/P2A/215363933688/THANGAMAY/StateBan/NA2137.0002-06-2022            27299.08 006"
stripped_lst = [x.strip() for x in str.split(" ") if x != '']
date_re = regex.compile(r"(\d{2}\-\d{2}\-\d{4})")
Date_ = date_re.split(stripped_lst[0])
print( Date_)
