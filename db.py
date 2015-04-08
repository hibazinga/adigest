import sqlite3
import settings
import os
import time

def record(string):
    f=open(settings._DB_LOG,'a+')
    try:
        f.write(string.encode("UTF-8"))
    except:
        pass
    f.close()

def log_time():
    now = int(time.time()) #get current time
    timeArray = time.localtime(now)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    record("TIME : "+otherStyleTime+"\n")


def insert_user(cur, uid, email, first_name, last_name, token, preference, timestamp):
    log_time()
    record("QUERY: select email from user where email = %s\n" % (email))
    cur.execute("select email from user where email = ? " , (email,))
    record("FOR  : check dup in user table\n\n")
    data = cur.fetchall()
    if len(data) != 0:
        #update user set preference=? where email=?
        cur.execute("update user set uid=?, first_name=?, last_name=?, token=?, preference=?, timestamp=? where email=?", (uid, first_name, last_name, token, preference, timestamp, email,))
        update_lastdigest(cur,email,140000000)
        return settings._SUCCESS
    log_time()
    record("QUERY: insert into user (uid, email, first_name, last_name, token, preference, timestamp) values (%s, %s, %s, %s, %s, %d, %d);\n" % (uid, email, first_name, last_name, token, preference, timestamp))
    cur.execute("insert into user (uid, email, first_name, last_name, token, preference, timestamp) values (?, ?, ?, ?, ?, ?, ?);", (uid, email, first_name, last_name, token, preference, timestamp,))
    record("FOR  : insert into user table\n\n")
    cur.execute("insert into whitelist values (?,?);", (email, "adigest@gmail.com"))
    update_lastdigest(cur,email,140000000)
    
    return settings._SUCCESS


def delete_user(cur, email):
    cur.execute("select email from user where email = ? " , (email,))
    log_time()
    record("QUERY: select email from user where email = %s\n" % (email))
    record("FOR  : check available in user table\n\n")
    data = cur.fetchall()
    if len(data) == 0:
        return settings._FAILURE
    
    cur.execute("delete from user where email = ?;" , (email,))
    log_time()
    record("QUERY: delete from user where email = %s ; \n" % (email))
    record("FOR  : delete user from user table\n\n")

    cur.execute("delete from lastdigest where email = ?;", (email,))
    log_time()
    record("QUERY: delete from lastdigest where email = %s ; \n" % (email))
    record("FOR  : delete email from lastdigest table\n\n")

    cur.execute("delete from email where email = ?;", (email,))
    log_time()
    record("QUERY: delete from email where email = %s ; \n" % (email))
    record("FOR  : delete email from email table\n\n")

    return settings._SUCCESS

def insert_whitelist(cur, email, sender):
    cur.execute("select * from whitelist where email=? and sender=?" , (email, sender,))
    log_time()
    record("QUERY: select * from whitelist where email = %s and sender = %s;\n" % (email, sender))
    record("FOR  : check table whitelist insertion dups\n\n")
    
    data = cur.fetchall()
    if len(data) !=0:
        
        return settings._FAILURE
    cur.execute("insert into whitelist (email, sender) values (?, ?);" , (email, sender,))
    log_time()
    record("QUERY: insert into whitelist (email, sender) values (%s, %s);\n" % (email, sender))
    record("FOR  : table whitelist insertion\n\n")
    
    return settings._SUCCESS


def insert_email(cur, email_addr, email_id, gmail_message_id, sender_email, sender_name, timestamp,  unsub_url, pic_url, subject, category=0):
    log_time()
    record("QUERY: insert into email (email_addr, email_id, gmail_message_id, sender_email, sender_name, timestamp,  unsub_url, pic_url, subject, category) values (%s,%s,%s,%s,%s,%d,%s,%s,%s,%d);\n" % (email_addr, email_id, gmail_message_id, sender_email, sender_name, timestamp,  unsub_url, pic_url, subject, category))
    cur.execute("insert into email (email_addr, email_id, gmail_message_id, sender_email, sender_name, timestamp,  unsub_url, pic_url, subject, category) values (?,?,?,?,?,?,?,?,?,?);" , (email_addr, email_id, gmail_message_id, sender_email, sender_name, timestamp,  unsub_url, pic_url, subject, category,))
    record("FOR  : table email insertion\n\n")
    
    return settings._SUCCESS



def update_user_preference(cur, email, preference):
    cur.execute("update user set preference=? where email=?;" , (preference, email,))
    log_time()
    record("QUERY: update user set preference=%d where email=%s;\n" % (preference, email))
    record("FOR  : update user preference\n\n")
    
    return settings._SUCCESS

def delete_whitelist(cur, email, sender):
    cur.execute("select * from whitelist where email=? and sender=?",(email, sender,))
    log_time()
    record("QUERY: select * from whitelist where email=%s and sender=%s" % (email, sender))
    record("FOR  : delete from white list\n\n")
    data = cur.fetchall()
    if len(data) ==0:
        
        return settings._FAILURE
    cur.execute("delete from whitelist where email=? and sender=?;" , (email, sender,))
    log_time()
    record("QUERY: delete from whitelist where email = %s and sender = %s;\n" % (email, sender))
    record("FOR  : delete whitelist\n\n")
    
    return settings._SUCCESS

def get_whitelist(cur, email):
    cur.execute("select sender from whitelist where email=?;" , (email,))
    log_time()
    record("QUERY: select sender from whitelist where email=%s;\n" % (email))
    record("FOR  : get whitelist\n\n")
    data = cur.fetchall()
    
    return data

def update_lastdigest(cur, email, timestamp):
    cur.execute("select email from lastdigest where email = ?;" , (email,))
    log_time()
    record("QUERY: select email from lastdigest where email = %s;\n" % (email))
    record("FOR  : insert or update last digest time\n\n")
    data = cur.fetchall()
    if len(data) == 0:
        cur.execute("insert into lastdigest (email, timestamp) values (?, ?)", (email, timestamp,))
        log_time()
        record("QUERY: insert into lastdigest (email, timestamp) values (%s, %d);\n" % (email, timestamp))
        record("FOR  : insert into last digest time\n\n")
    else:
        cur.execute("update lastdigest set timestamp=? where email=?", (timestamp, email,))
        log_time()
        record("QUERY: update lastdigest set timestamp = %d where email = %s;\n" % (timestamp,email))
        record("FOR  : update last digest time\n\n")
    
    return settings._SUCCESS


def get_email_list(cur):
    timestamp = int(time.time()) #get current time
    cur.execute("select lastdigest.email from lastdigest,user where lastdigest.timestamp+user.preference*12*3600>=? and lastdigest.email=user.email", (timestamp,))
    log_time()
    record("QUERY: select lastdigest.email from lastdigest,user where lastdigest.timestamp+user.preference*12*3600>=%d and lastdigest.email=user.email ;\n" % (timestamp))
    record("FOR  : get email list to send digest\n\n")

    data = cur.fetchall()
    
    return data



def get_digest_list(cur, email):
    timestamp = int(time.time()) #get current time
    
    cur.execute("select timestamp from lastdigest where email = ?", (email,))
    data = cur.fetchone()
    log_time()
    record("QUERY: select timestamp from lastdigest where email = %s\n" % (email))
    record("FOR  : get last digest time\n\n")
    lasttimestamp = 0
    lasttimestamp = data[0]
    #print lasttimestamp
    
    cur.execute("update lastdigest set timestamp=? where email=?", (timestamp, email,))
    log_time()
    record("QUERY: update lastdigest set timestamp = %d where email = %s;\n" % (timestamp, email))
    record("FOR  : update last digest time\n\n")
    
    #cur.execute("select email_id, gmail_message_id, sender_email, sender_name, unsub_url, pic_url, subject, category from email where email_addr=? and timestamp>=? and timestamp<=? and sender_email not in (select sender from whitelist where email=?) ;", (email, lasttimestamp, timestamp, email,))
    cur.execute("select email.email_id, email.gmail_message_id, email.sender_email, email.sender_name, email.unsub_url, email.pic_url, email.subject, email.category, email.email_addr, user.first_name from email,user where email.email_addr=? and email.timestamp >=? and email.timestamp<=? and user.email=? and email.sender_email not in (select whitelist.sender from whitelist where whitelist.email=?) ;", (email, lasttimestamp, timestamp, email, email,))
    
    log_time()
    record("QUERY: select email.email_id, email.gmail_message_id, email.sender_email, email.sender_name, email.unsub_url, email.pic_url, email.subject, email.category, email.email_addr, user.first_name from email,user where email.email_addr=%s  and email.timestamp<=%s and user.email=%s and email.sender_email not in (select sender from whitelist where email=%s);\n" % (email, timestamp, email, email))
    record("FOR  : get emails contents for email_addr = email\n\n")
    
    data = cur.fetchall()
    '''
    email_addr, email_id, gmail_message_id, sender_email, sender_name, timestamp,  unsub_url, pic_url, subject, category = []
    for i in data:
        email_addr.append(i[0])
        email_id.append(i[1])
        gmail_message_id.append(i[2])
        sender_email.append(i[3])
        sender_name.append(i[4])
        timestamp.append(i[5])
        unsub_url.append(i[6])
        pic_url.append(i[7])
        subject.append(i[8])
        category.append(i[9])
    '''
    return data
