import subprocess
import time
import ssl
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests

 
# 要执行的Linux命令
# command = "curl get http://whois.pconline.com.cn/ipJson.jsp?json=true"
# command = "curl get myip.opendns.com @resolver1.opendns.com"


try:
    # 执行命令并获取输出结果
    # result = subprocess.check_output(command, shell=True)

    url = "http://whois.pconline.com.cn/ipJson.jsp?json=true"
    response = requests.get(url)
    # data = {"key":"value"}
    # response = requests.get(url,data=data)
    
    print("命令执行成功！")
    # time.sleep(5)
    print("输出结果为:", response.text)

    smtp = smtplib.SMTP()

    smtp.connect("smtp.163.com",25)
    smtp.login(user="myjjack@163.com",password="IBAIUXFZHGDYAREB")

    message = MIMEText(response.text,'plain','utf-8')
    message['From'] = 'myjjack@163.com'
    message['To'] = 'Touho'
    message['Subject'] = 'ip'

    print(message)

    smtp.sendmail('myjjack@163.com',"1603130558@qq.com",message.as_string())


except subprocess.CalledProcessError as e:
    print("命令执行失败！错误信息为:\n", e.stderr.decode())