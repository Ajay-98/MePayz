
import regex

str = "29-08-2022UPI/P2M/224141587999/Naveen Ku/PaytmPay/UPI29-08-2022                 90.0029-08-2022               366.69 006"
tst_splt = "Ajay jebiagb Ajay jbguew"
stripped_lst = [x.strip() for x in str.split(" ") if x != '']
date_re = regex.compile(r"(\d{2}\-\d{2}\-\d{4})")
stmt_info_ = date_re.split(stripped_lst[0])[2]
print(stmt_info_ + "Ajay ")

