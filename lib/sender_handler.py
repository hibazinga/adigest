'''
usage: 
from lib.sender_handler import match
match(email)
'''

import os
import sys
from inspect import getsourcefile
from os.path import abspath

link_prefix = 'http://famouslogos.net/images/'
code_path = abspath(getsourcefile(lambda:0)).split('sender_handler.py')[0]

def match(email, linkFile=code_path+'./link', nameFile=code_path+'./name'):
    at_pos = email.find("@")
    uid = email[:at_pos].lower()
    domain = email[at_pos+1:].split('.')[-2].lower()

    name_link = {}
    tmp = open(nameFile, 'r')
    for line in tmp.readlines():
        line = line[:-1]
        strs = line.lower().split(' ')
        name = strs[0]
        link = link_prefix + strs[0]
        for i in range(1,len(strs)):
            name += strs[i]
            link += '-'
            link += strs[i]
        name_link[name] = link + '-logo.jpg'
 
    #pick closest name
    closest_name = ""
    for name in name_link:
        if name == uid or name == domain:
            closest_name = name
            #print "closest_name:", closest_name
            break

#hard-coding for missing links
    if uid.lower() == "gmail" or domain.lower() == "gmail":
        return "http://img4.wikia.nocookie.net/__cb20101116142833/logopedia/images/0/0a/Gmail_logo.png"
    
    #print name_link,closest_name
    res_link = ""
    if closest_name == "":
        return "http://www.fdla.com/wp-content/uploads/2011/03/shadowIcon.jpg"

    tmp = open(linkFile, 'r')
    for link in tmp.readlines():
        #print '====%s****%s'%(name_link[name],link)
        if name_link[name] in link.lower():
            res_link = name_link[name]
            break

    
    return res_link

if __name__ == '__main__':
    email = ''
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = "zjuwangk@Ford.com"
    print match(email)
