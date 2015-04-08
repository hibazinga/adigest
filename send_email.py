import smtplib

from email.mime.text import MIMEText

# mailto_list=["zjuxie@gmail.com","renyb@qq.com"]
def send_mail(to_list, content, sub="Your AD Digest"):
    mail_host="smtp.gmail.com"
    mail_user="adigest2015"
    mail_pass="!qaz2Wsx3eDc"
    mail_postfix="gmail.com"
    """    
    file_object = open(html)
    try:
        content = file_object.read()
    finally:
        file_object.close()
    """
    
    me="ADigest"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='html',_charset='UTF-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_list

    try:
        s = smtplib.SMTP_SSL()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        print "Success!\n"
        return True

    except Exception, e:
        print str(e)
        print "Failed to send digest email!\n"
        return False

#send_mail("renyb@qq.com", "digest.html")

'''
if __name__ == '__main__':
    file_object = open('digest.html')
    try:
        all_the_text = file_object.read( )
    finally:
        file_object.close( )
    if send_mail(mailto_list,"Your AD Digest",all_the_text):
        print "success"
    else:
        print "failure"

'''
