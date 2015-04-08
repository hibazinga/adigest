'''
detects if the email body is a promotion email.
detect_promotion(email_body)  returns true/false

returns:
unsubscribe url
picture url
'''

#import re
import sys
from HTMLParser import HTMLParser

#url_pattern = '^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
newTagFlag = False
key_word = 'unsubscribe'
kw_pos = {'in_url':'', 'in_cur_tag':'', 'in_near_tag':''}
is_promotion = False
cur_attrs = []
next_url_unsubscribe = False
img_url_list = []

def prune_url(url):
#do nothing
    return url

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global newTagFlag
        global is_promotion
        global next_url_unsubscribe
        global img_url_list
        global cur_attrs
        newTagFlag = True

        for attr_pair in attrs:
            if len(attr_pair) < 2:
                continue
            if 'img' in tag and 'src' in attr_pair[0]:
                url = attr_pair[1]
                url = prune_url(url)
                img_url_list.append(url)
        if kw_pos['in_url'] == '':
            cur_attrs = attrs
            for attr_pair in attrs:
                if attr_pair[1] is None:
                    continue
                if len(attr_pair) < 2 or len(attr_pair[1]) < 5:
                    continue
                attr = prune_url(attr_pair[1]) # \"www\" ==> www

                if attr_pair[0] == 'href':
                    if key_word in attr.lower():
                        kw_pos['in_url'] = attr
                        is_promotion = True
                        next_url_unsubscribe = False
                    else:
                        if next_url_unsubscribe == True:
                            if kw_pos['in_url'] == '' and kw_pos['in_cur_tag'] == '':
                                kw_pos['in_near_tag'] = attr
                                next_url_unsubscribe = False
                                is_promotion = True
                    
    def handle_endtag(self, tag):
        global newTagFlag
        newTagFlag = False
        pass
    
    def handle_data(self, data):
        global is_promotion
        global cur_attrs
        global newTagFlag
        global next_url_unsubscribe

        if kw_pos['in_url'] == '':
            if key_word in data.lower():
                if newTagFlag:
                    for attr_pair in cur_attrs:
                        attr = attr_pair[1]
                        if attr_pair[0] == 'href':
                        #2nd unsubscribe pattern
                            kw_pos['in_cur_tag'] = prune_url(attr)
                            is_promotion = True
                else:
                    if kw_pos['in_cur_tag'] == '':
                    #3rd unsubscribe pattern
                        next_url_unsubscribe = True

#body: email body
def detect_promotion(body):
    parser = MyHTMLParser()
    parser.feed(body)
 
    unsub_url = ''
    if kw_pos['in_url'] != '':
        unsub_url = kw_pos['in_url']

    elif kw_pos['in_cur_tag'] != '':
        unsub_url = kw_pos['in_cur_tag']
    
    elif kw_pos['in_near_tag'] != '':
        unsub_url = kw_pos['in_near_tag']
    
    if len(img_url_list) == 0:
        img_url_list.append('http://i.huffpost.com/gen/964776/images/o-CATS-KILL-BILLIONS-facebook.jpg')
    return {
            'is_promotion' : is_promotion,
            'unsubscribe_url' : unsub_url,
            'img_url_list': img_url_list[0]
            }

#for DEBUG 
if __name__ == '__main__':
    if len(sys.argv)>1:
        f = open(sys.argv[1], 'r')
        body = f.read()
    else:
        body = ''
    print detect_promotion(body)
