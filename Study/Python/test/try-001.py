import ssl,smtplib
from email.mime.text import MIMEText
from email.header import Header

smtp = smtplib.SMTP()

smtp.connect("smtp.163.com",25)
smtp.login(user="myjjack@163.com",password="myj520.")

message = MIMEText('ceshi','plain','utf-8')
message['From'] = Header('TouhoServer','utf-8')
message['To'] = Header('Touho','utf-8')
message['Subject'] = Header('ip','utf-8')
print(message)

smtp.sendmail(from_addr='myjjack@163.com',to_addrs="1603130558@qq.com",msg=message.as_string())