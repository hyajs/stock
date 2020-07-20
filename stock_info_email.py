import smtplib,schedule,time,os
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


account = '@qq.com'
password = 'qq邮箱设置上有'
receiver = '@qq.com'
filename = 'aa.csv'
def send_email():
    qqmail = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
    qqmail.login(account,password)

    msg = MIMEMultipart()  # 创建一个带附件的实例
    subject = Header('今日股票信息', 'utf-8').encode()
    msg["Subject"] = subject  # 指定邮件主题
    msg["From"] = account  # 邮件发送人
    msg["To"] = '自己改'
    msg.attach(MIMEText('附件今日股票信息，请查收!', _subtype='html', _charset='utf-8'))
    part = MIMEApplication(open(filename, 'rb').read())
    part.add_header('Content-Disposition', 'attachment',filename=filename)
    msg.attach(part)
    try:
        qqmail.sendmail(account, receiver, msg.as_string())
        print ('邮件发送成功')
        os.remove("aa.csv")
    except:
        print ('邮件发送失败')
    qqmail.quit()

def job():
    print('开始一次任务')
    send_email()
    print('任务完成')


schedule.every().day.at("06:30").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)

# 每天早上630自动运行该代码，接入qq代码发送邮件。初级服务器运行 ：D