import mandrill

def send(from_email, to_email, reciper = 'Recipient Name', page):
    try:
        mandrill_client = mandrill.Mandrill('jBsJqXiN9MUbIMJVSSubow')
        message = {
            'from_email': from_email,
            'html': page,
            'subject': 'Adigest Daily',
            'to': [{
                 'email': to_email,
                 'name': 'Recipient Name',
                 'type': 'to'}],
        }
        result = mandrill_client.messages.send(message=message)
        print result
        '''
        [{'_id': 'abc123abc123abc123abc123abc123',
          'email': 'recipient.email@example.com',
          'reject_reason': 'hard-bounce',
          'status': 'sent'}]
        '''

def gen_digest():
    #for 

except mandrill.Error, e:
    # Mandrill errors are thrown as exceptions
    print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
    # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'    
    raise
