from flask import Flask, g, request, send_file, render_template, url_for, redirect, session
import oauth123
import sqlite3
import sys
import db
import settings
import threading
from lib.body_handler import *
import send_email
import email_timer
import gen_digest_html

app = Flask(__name__)


def connect_db():
    return sqlite3.connect(settings._DB)

def manage_db(con, cur, fn, *args):
    code = fn(cur, *args)
    if code == settings._SUCCESS:
        con.commit()
    return code

def gen_digest(uid):
    conn = connect_db()
    cur = conn.cursor()
    f = open("/tmp/test_gen_digest.txt", "a")
    """email_addr, sender_email, sender_name, email_id, gmail_message_id, timestamp, subject, s"""
    f.write(uid+"\n")
    emails = oauth123.get_last100_emails(uid)
    f.write("get 100 emails\n")
    f.write(str(emails))
    f.write('\n')
    f.write(str(len(emails)))
    email_addr = ""
    if len(emails) == 0:
        return
    i = 0
    for email in emails:
        i += 1
        f.write(str(i)+"\n")
        email_addr = email[0]
        sender_email = email[1]
        sender_name = email[2]
        email_id = email[3]
        gmail_message_id = email[4]
        timestamp = email[5]
        subject = email[6]
        content = email[7]
        parse_res = detect_promotion(content)
        if parse_res['is_promotion']:
            f.write("email_addr\n")
            f.write(email_addr)
            db.insert_email(cur, email_addr, email_id, gmail_message_id, sender_email, sender_name, int(timestamp), parse_res['unsubscribe_url'], "", subject)
            f.write("tryt insrteafeasd\n")
            conn.commit()
    f.write('asfdsadfsad\n')
    f.write(email_addr)
    digest_emails = db.get_digest_list(cur, email_addr)
    f.write('finish get digest list\n')
    print digest_emails
    conn.commit()
    raw_data, first_name = email_timer.process_emails(digest_emails)
    f.write('--------------------\n')
    f.write(str(raw_data)+'\n')
    f.write(str(first_name)+'\n')
    if len(raw_data) > 0:
        f.write('get in here!!!\n')
        html_data = gen_digest_html.gen_html(raw_data, first_name)
        #f.write(str(html_data))
        #f.write('\n')
        send_email.send_mail(email_addr, html_data)
        f.write('----------ok here too---------\n')
    f.close()
    cur.close()
    conn.close()

@app.before_request
def before_request():
    g.db = connect_db()
    g.cur = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'cur'):
        g.cur.close()
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def redirect_index():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    #db.insert_user(g.cur, '123','123@gmail.com', 'Jie', 'Yu', '123456', 2)
    #g.db.commit()
    return render_template('index.html')

@app.route('/image/<image_id>')
def get_image(image_id):
    filename = image_id + ".png"
    return send_file(filename, mimetype='image/png')

@app.route('/oauth_success')
def oauth_success():
    f = open("/tmp/test_email.txt", "a")
    token = request.args.get('contextio_token')
    #uid, email, first_name, last_name, token, preference, timestamp = oauth123.get_userinfo_from_token(token)
    args = oauth123.get_userinfo_from_token(token)
    code = manage_db(g.db, g.cur, db.insert_user, *args)
    session['email_addr'] = args[1]
    """
    uid, email, first_name, last_name, token, preference, timestamp = oauth123.get_userinfo_from_token(token)
    code = db.insert_user(g.cur, uid, email, first_name, last_name, token, preference, timestamp)
    """
    f.write('go into \n')
    if code == settings._SUCCESS:
        uid = args[0]
        f.write('success\n')
        f.write(uid + "\n")
        t = threading.Thread(target=gen_digest, args=(uid, ))
        t.start()
        f.close()
        return redirect(url_for('get_preference'))
    else:
        f.write('fail\n')
        f.close()
        return redirect(url_for('get_preference'))
    
    #store this data here
    #return str(uid)+"\n"+ str(email)+"\n"+str(first_name)+"\n"+str(last_name) +"\n"+str(token)+ "\n"+str(preference) + "\n" + str(timestamp)
    
@app.route('/oauth')
def oauth():
    url = oauth123.get_browser_redirect_url()
    return redirect(url)

@app.route('/preference', methods = ['GET','POST'])
def get_preference():
    if request.method == 'GET':
        return render_template('preference.html', frequency = "1")
    else :
        data = request.form['frequency']
        frequency = int(data)
        code = manage_db(g.db, g.cur, db.update_user_preference, session['email_addr'], frequency)
        return render_template('success.html')


@app.route('/move_to_whitelist', methods = ['GET'])
def add_to_whitelist():
    code = manage_db(g.db, g.cur, db.insert_whitelist, request.args.get('email'), request.args.get('sender_email'))
    return render_template('success.html')


@app.route('/webhook', methods = ['POST'])
def webhook_callback():
    f = open('/tmp/log123.txt','a')
    f.write("------------------------\n")
    f.write("Webhook Called!\n")
    f.write("Open file!\n")
    import json
    data = json.loads(request.data)
    uid = data['account_id']
    mid = data['message_data']['message_id']
    f.write(uid)
    f.write('\n')
    f.write(mid)
    f.write('\n')
#parse_res = {'is_promotion':Bool, 'unsubscribe_url':string, 'img_url_list':string}
    email_addr, sender_email, sender_name, email_id, gmail_message_id, timestamp, subject, content = oauth123.get_message(uid, mid)

    #f.write('Finish fetch data\n')
    #f.write(content)
    parse_res = detect_promotion(content)
    f.write(str(parse_res))
    f.write('\n')
    f.write("------------------------\n")
    if parse_res['is_promotion']:
        oauth123.mark_read(uid, mid)
        db.insert_email(g.cur, email_addr, email_id, gmail_message_id, sender_email, sender_name, timestamp,  parse_res["unsubscribe_url"], "http://pic.com", subject) 
        g.db.commit()
    f.close()
    return content


if __name__ == '__main__':
    app.run(debug=True)
