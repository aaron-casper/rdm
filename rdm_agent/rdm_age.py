#this code is rough, you might not get it to work.
#but, if you have a IRCD and webserver at your disposal
#you just might.
#
#enjoy,
#aaron casper
#
#!/usr/bin/env python
import datetime
import subprocess
import time
import os
import psutil
import socket
import random
#search and replace 'network.here.please'
network = 'network.here.please'
port = 6667
CHAN = "#console"
citrix_running = ""
agent_host = socket.gethostname()
agent_nickname = "rdm_dev_001"
agent_ver = "0.1_9"

time.sleep(random.uniform(0.0,60.0))

irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
irc.send ( 'NICK %s\r\n' % agent_host )
irc.send ( 'USER %s %s %s :Python RDM\r\n'% (str(agent_host), str(agent_host), str(agent_host)))
irc.send ( 'JOIN %s\r\n' % CHAN)
irc.send ( 'PRIVMSG #console : version %s on host %s\r\n' % (agent_ver, agent_host))
while True:
    data = irc.recv ( 4096 )
    if data.find ( 'PING' ) != -1:
	irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
    if data.find ( '!agentver' ) != -1:
  	irc.send ( 'PRIVMSG %s :version %s\r\n' % (CHAN, agent_ver))
    if data.find ( '!status' ) != -1:
	procs = os.popen("ps -A | grep wfica")
	#check if citrix is running
	currentprocs = procs.read()
	if currentprocs.find('wfica') == -1:
	    citrix_running = "Not Running"
	else:    
	    citrix_running = "Running"
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M.%S')
	cpu=psutil.cpu_percent(interval=1)
	mem=psutil.virtual_memory()
	net=psutil.net_io_counters()
	stuffbuffer = ("agent_status " + str(st) + "," + str(agent_host) + "," + str(cpu) + "," + str(mem.percent) + "," + str(net.bytes_sent) + "," + str(net.bytes_recv) +  "," + str(agent_ver) + "," + str(citrix_running))
	irc.send ( 'PRIVMSG rdm_master : %s \r\n' % stuffbuffer)
    if data.find ( '!tunnel' ) != -1:
	irc.send ( 'PRIVMSG %s : digging a tunnel...\r\n' % CHAN)
	#initiate a reverse SSH tunnel to the master server
        #tunneler = str(subprocess.check_output(["sh ./tunnel.sh"]))
        os.popen ( "sh ./AutoDiag/tunnel.sh" )
#    if data.find ( '!cavein' ) != -1:
#	irc.send ( 'PRIVMSG %s : caving in that tunnel...\r\n' % CHAN)
#	os.popen ( "sh ./AutoDiag/collapse")
    if data.find ( '!reboot' ) != -1:
	#reboot the thing
	irc.send ( 'PRIVMSG %s : reboot instruction detected, standby...\r\n' % CHAN)
	os.popen ( "sh ./AutoDiag/reboot")
    if data.find ( '!agentrestart' ) != -1:
	#restart the RDM agent
        irc.send ( 'QUIT\r\n' )
        exit()
    if data.find ( '!package' ) != -1:
	packagename = data.split( )
	#fix the server address before running
	irc.send ( 'PRIVMSG %s :Attempting to connect\r\n' % CHAN)
	os.popen ( "wget network.here.please/rdm_hub/packages/%s\n" % packagename[4])
	irc.send ( 'PRIVMSG %s :package delivery "%s" failed\r\n' % (CHAN, packagename[4]))
    if data.find ( '!sim_error' ) != -1:
	#queuing for errors, not yet finished
        irc.send ( 'JOIN #ATTENTION\r\n' )
        irc.send ( 'PRIVMSG #ATTENTION : I need help, something is wrong!\r\n')
	irc.send ( 'PRIVMSG %s : Joining #ATTENTION queue.\r\n' % CHAN)
    print data
