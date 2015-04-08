import contextio as c
import time
import unicodedata

CONSUMER_KEY = 'x8k6sokj'
CONSUMER_SECRET = 'VSHVN2f4Praml16A'
context_io = c.ContextIO(
	consumer_key=CONSUMER_KEY, 
	consumer_secret=CONSUMER_SECRET,  
)

callbackurl = 'http://ec2-52-5-42-106.compute-1.amazonaws.com/oauth_success'

def get_browser_redirect_url():
	d = context_io.post_connect_token(callback_url = callbackurl)
	url = d["browser_redirect_url"]
	return str(url)

def get_userinfo_from_token(t):
	d = context_io.get_connect_tokens(token = t)
	uid = d['account']['id']
	first_name = d['account']['first_name']
	last_name = d['account']['last_name']
	email = d['account']['email_addresses'][0]
	token = t
	preference = 2
	timestamp = d['account']['created']
	#create_webhook(uid)
	return uid, email, first_name, last_name, token, preference, timestamp

def create_webhook(uid):
	account = c.Account(context_io, {'id': uid})
	webhook_callback_url = "http://ec2-52-5-42-106.compute-1.amazonaws.com/webhook"
	fail_url = "http://ec2-52-5-42-106.compute-1.amazonaws.com/webhook_fail"	
	webhook = account.post_webhook(callback_url=webhook_callback_url, failure_notif_url=fail_url)

def get_message(uid, mid):
	account = c.Account(context_io, {'id': uid})
	m = c.Message(account,{'message_id':mid})
	m.get()
	email_addr = m.addresses["to"][0]["email"]
	sender_email = m.addresses["from"]["email"]
	sender_name  = m.addresses["from"]["name"]
	email_id = m.message_id
	gmail_message_id = m.gmail_message_id
	timestamp = m.date
	subject = m.subject
	body = m.get_body()
	s = ''
	for b in body:
		s += b["content"]

	return email_addr, sender_email, sender_name, email_id, gmail_message_id, timestamp, subject, s

def mark_read(uid, mid):
	account = c.Account(context_io, {'id': uid})
	m = c.Message(account,{'message_id':mid})
	m.get()
	m.post_flag(seen=1)	
	return 1

def get1(uid,mid):
	account = c.Account(context_io, {'id': uid})
	m = c.Message(account,{'message_id':mid})
	m.get(include_body=1)
	return m
	body = m.get_body()
	s = ''
	for b in body:
		s += b["content"]
	return s

def send_email(uid):
	account = c.Account(context_io, {'id': uid})
	account.post_message('0','0')

def get_last100_emails(uid):
	f = open("/tmp/get_email.txt", "a")
	f.write('id:---' + str(uid) +'-----\n')
	# uid = '55210e7d8e079d8c528b4568'
	account = c.Account(context_io, {'id': uid})
	account.get()
	time.sleep(10)
	f.write(str(account))
	m_list = account.get_messages(limit = 30)
	emails = []
	i = 0
	#return m_list
	f.write(str(len(m_list)))
	f.write(str(m_list))
	for m in m_list:
		i += 1
		try:
			f.write(str(i) + "\n")
			email_addr = m.addresses["to"][0]["email"]
			if email_addr != account.email_addresses[0]:
				f.write('ignore')
				continue
			sender_email = m.addresses["from"]["email"]
			sender_name  = m.addresses["from"]["name"]
			email_id = m.message_id
			gmail_message_id = m.gmail_message_id
			timestamp = m.date
			subject = m.subject
			body = m.get_body()
			s = ''
			for b in body:
				s += b["content"]		
			emails.append([email_addr, sender_email, sender_name, email_id, gmail_message_id, timestamp, subject, s])		
		except:
			pass
	f.write('----------------------------\n')
	f.close()
	return emails

	#print o.get1('5520ddb70fd20baa4d8b457c','5520ddb92b9ffd8f478b45c7')
	# print get_browser_redirect_url()
	# get_id_from_token(1231)
