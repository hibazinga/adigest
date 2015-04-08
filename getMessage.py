import contextio as c

CONSUMER_KEY = 'x8k6sokj'
CONSUMER_SECRET = 'VSHVN2f4Praml16A'
context_io = c.ContextIO(
  consumer_key=CONSUMER_KEY, 
  consumer_secret=CONSUMER_SECRET,  
)

account = c.Account(context_io, {'id': '55201e008e079da4338b4569'})
m = account.get_messages(limit=1)[0]



wh = account.get_webhooks()


