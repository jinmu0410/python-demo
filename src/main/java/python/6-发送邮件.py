import smtplib
from email.mime.text import MIMEText
from email.header import Header

##发送方邮箱设置
mail_host = "smtp.163.com"
mail_user = "hmlnzn@163.com"
mail_pass = "BHEOPXAMGBWIJTDO"

send_mail = "hmlnzn@163.com"
receive_mail = "hujb@hsmap.com"
subject = 'Python SMTP 邮件测试'


def send(email_content):
    ##内容
    message = MIMEText(email_content, 'plain', 'utf-8')
    message['From'] = Header("菜鸟教程", 'utf-8')
    message['To'] =  Header("测试", 'utf-8')

    ##主题
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(send_mail, receive_mail, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")



if __name__ == '__main__':
   send('测试发送邮件')