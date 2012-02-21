import sys
import socket
import string

HOST="irc.freenode.net"
PORT=6667
NICK="mk_socket__"
IDENT="mk_socket_"
REALNAME="Matt's Crazy Socket"
CHANNEL="#mk_temp"
readbuffer=""

s=socket.socket()
s.connect((HOST,PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT,HOST,REALNAME))
s.send("JOIN %s\r\n" % CHANNEL)
s.send("PRIVMSG mkenny :whaddup, ho!!\r\n")
s.send("PRIVMSG sudobangbang :whaddup, ho!!\r\n")
s.send("QUIT Bye!\r\n")
try:
    while 1:
        readbuffer=readbuffer+s.recv(1024)
        temp=string.split(readbuffer, "\n")
        readbuffer=temp.pop()
        print temp
        for line in temp:
            line=string.rstrip(line)
            line=string.split(line)

            if(line[0]=="PING"):
                s.send("PONG %s\r\n" % line[1])
except:
    s.send("QUIT Bye!\r\n")
    s.close()
