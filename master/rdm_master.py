#!/usr/bin/env python
import sqlite3


#uncomment this stuff to generate new db
#conn = sqlite3.connect('rdm.sqlite3')
#cur = conn.cursor()
#cur.execute('CREATE TABLE Devices (timestamp TEXT, device_name TEXT, cpu FLOAT, mem FLOAT, net_sent INTEGER, net_recv INTEGER, version TEXT, citrix TEXT)')
#cur.execute('INSERT INTO Devices (timestamp, device_name, cpu, mem, net_sent, net_recv, version, citrix) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', ('today', 'TX-rPi3-acasper', 'a lot', 'a little', 'some', 'some more', 'outdated','who knows'))
#conn.commit()
#cur.close()
#conn.close()

import re
import time
import os
import psutil
import socket
import subprocess

network = 'localhost'
port = 6667
CHAN0 = "#eastern"
CHAN1 = "#central"
CHAN2 = "#mountain"
CHAN3 = "#pacific"
CHAN4 = "#offshore"
CHAN5 = "#console"

master_host = socket.gethostname()
master_nickname = "rdm_master"
master_ver = "0.1_9"
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 4096 )
irc.send ( 'NICK %s\r\n' % master_nickname )
irc.send ( 'USER rdm_master rdm_master rdm_master :Python RDM\r\n' )
#don't spam-join, it's a bad idea, work out a delay if you want to 
#use more than one channel
irc.send ( 'JOIN %s\r\n' % CHAN5)
while True:
    data = irc.recv ( 4096 )
    if data.find ( 'PING' ) != -1:
        irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
    if data.find ( 'agent_status' ) != -1:
	stuffbuffer = data
	csv_data = stuffbuffer.split("agent_status",1)[1]
	irc.send ( 'PRIVMSG %s :%s\r\n' %(CHAN5, csv_data))
	conn = sqlite3.connect('rdm.sqlite3')
	cur = conn.cursor()
	age_ts = str(csv_data.split(",")[0])
	device_name = str(csv_data.split(",")[1])
	cpu = csv_data.split(",")[2]
	mem = csv_data.split(",")[3]
	net_sent = csv_data.split(",")[4]
	net_recv = csv_data.split(",")[5]
	version = str(csv_data.split(",")[6])
	citrix = str(csv_data.split(",")[7])
	table_name = str(device_name)
	cur.execute("CREATE TABLE IF NOT EXISTS '" + table_name + "' (timestamp TEXT, device_name TEXT, cpu FLOAT, mem FLOAT, net_sent INTEGER, net_recv INTEGER, version TEXT, citrix TEXT)")
	cur.execute("INSERT INTO '" + table_name + "' (timestamp, device_name, cpu, mem, net_sent, net_recv, version, citrix) VALUES (?,?,?,?,?,?,?,?)", (age_ts, device_name, cpu, mem, net_sent, net_recv,version,citrix))
	irc.send ( 'PRIVMSG %s : %s\r\n' %(CHAN5,age_ts))
	conn.commit()
	cur.close()
	conn.close()
    if data.find ( 'JOIN' ) != -1:
	agentid=data[data.find(":")+1:data.find("!")]
        irc.send ( 'PRIVMSG %s :!status\r\n' % (agentid))
    if data.find ( '!help' ) != -1:
	irc.send ( 'PRIVMSG %s :All commands should be sent to agents, not groups!\r\n' % CHAN5)
	time.sleep(2)
	irc.send ( 'PRIVMSG %s :All commands are preceeded by "!"\r\n' % CHAN5)
	time.sleep(2)
        irc.send ( 'PRIVMSG %s :agentver - print agent version\r\n' % CHAN5)
	time.sleep(1)
        irc.send ( 'PRIVMSG %s :status - generate/print status\r\n' % CHAN5)
	time.sleep(1)
	irc.send ( 'PRIVMSG %s :tunnel - Initiate SSH tunnel\r\n' % CHAN5)
	time.sleep(1)
	irc.send ( 'PRIVMSG %s :rebootdevice - Reboot target device\r\n' % CHAN5)
	time.sleep(1)
	irc.send ( 'PRIVMSG %s :agentrestart - Kill/Restart agent\r\n' % CHAN5)    
    print data
