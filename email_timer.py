import sys
import db
#sys.path.insert(0, "/var/www/FlaskApp/FlaskApp/newsletter-email-template")
import gen_digest_html
import sqlite3
import send_email
import settings
from lib.sender_handler import match

"""
data format:
    email_id, gmail_message_id, sender_email, sender_name, unsub_url, pic_url, subject, category, email_addr, first_name
"""

def process_emails(emails):
    data = []
    first_name = ""
    for entry in emails:
        sender_email = entry[2]
        sender_name = entry[3]
        first_name = entry[9]
        email_addr = entry[8]
        subject = entry[6] 
        pic_url = match(sender_email)
        unsub_url = entry[4]
        email_url = "mail.google.com/mail/u/0/#inbox/"+entry[1]
        entry_dict = { "email_addr": email_addr, "sender_email": sender_email, "title": sender_name, "content": subject, "email_url": email_url, "pic_url": pic_url, "unsub_url": unsub_url}
        data.append(entry_dict)
    print data
    return data, first_name

def main():
    conn = sqlite3.connect(settings._DB)
    cur = conn.cursor()
    user_list = db.get_email_list(cur)
    print user_list

    for user in user_list:
        emails = db.get_digest_list(cur, user[0])
        raw_data, first_name = process_emails(emails)
        if len(raw_data) > 0:
            html_data = gen_digest_html.gen_html(raw_data, first_name)
            send_email.send_mail(user[0], html_data)
            #send_email.send_mail("zjuxie@gmail.com", html_data)
            #send_email.send_mail("jieyu.120@gmail.com", html_data)
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
