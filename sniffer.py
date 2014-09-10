#!/usr/bin/python2.7

import socket, sys
import re
from struct import *
import string
import subprocess




#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

fnicks = open("/home/rayenok/software/python/alertWoW/nicks.lst","r")
fwords = open("/home/rayenok/software/python/alertWoW/words.lst","r")

list_words = []
list_nicks = []

for line in fnicks:
    list_nicks += [line.strip('\n')]

for line in fwords:
    list_words += [line.strip('\n')]

# print "list nicks: "+str(list_nicks)
# print "list words: "+str(list_words)

lheader = 40

# receive a packet
while True:
    packet = s.recvfrom(8997)
    packet = packet[0]
    headers = packet[0:lheader]
    # print "Header:"+str(headers)
    dataHex = ''.join([hex(ord(x))[2:].zfill(2) for x in packet[lheader:]])
    # print "DataHex: "+dataHex

    # mGuild = re.search('\w{8}0300000000\w{16}\w{8}(\w*)0000',dataHex)
    mGuild = re.search('\w{8}0300000000\w{6}0{10}\w{2}0{6}(\w*?)0000',dataHex)
    mOnline = re.search('\w{8}0c01(\w*?)00\w{6}0{10}',dataHex)
    mOffline = re.search('\w{8}0d01(\w*?)00\w{6}0{10}',dataHex)

    if mGuild:
        try:
            msg = mGuild.group(1).decode('hex')
            if all(c in string.printable for c in msg) and \
                        not all(c in string.hexdigits for c in msg):
                print "[Guild]: "+msg
                for word in list_words:
                        if word in msg.lower():
                                print "[Alerta][Guild] "+msg
                                subprocess.Popen(['notify-send',msg,'-t','0'])
        except Exception, e:
            pass

    elif mOnline:
        try:
            msg = mOnline.group(1).decode('hex')
            if all(c in string.printable for c in msg) and \
                        not all(c in string.hexdigits for c in msg):
                
                print msg + ' just connected'
                for nick in list_nicks:
                        if nick in msg.lower():
                                print "[Alerta] "+msg+' just connected'
                                subprocess.Popen(['notify-send', \
                                                msg+'has come online', \
                                                '-t','0'])
        except Exception, e:
            pass

    elif mOffline:
        try:
            msg = mOffline.group(1).decode('hex')
            if all(c in string.printable for c in msg) and \
                        not all(c in string.hexdigits for c in msg):
                print msg + ' just disconnected'
                for nick in list_nicks:
                        if nick in msg.lower():
                                print "[Alerta] "+msg+' just disconnected'
                                subprocess.Popen(['notify-send', \
                                                msg+'has gone offline', \
                                                '-t','0'])
        except Exception, e:
            pass
