this is a very early version
it's a Remote Device Manager

you will need:

ircd
httpd
sshd
python
a fair amount of debugging time


go through the directory tree and read through the scripts

RDM works by using the ircd as a central communications hub for 'agents'
agents are linux computers with a python environment in the field
these agents connect to the hub on a traditional irc port and communicate 
with the traditional privmsg structure

different commands on the agent-end can be added easily with shell
scripts

check ./Autodiag in the agent tarball for a few examples
credit to whoever wrote the ookla speedtest script
i modified it to provide .csv data

the idea is to have any number of devices that a traditional irc net
could support

with regionally located ircds all connected together as a network
the scale is literally immense

in addition, the master service is light enough to run on a sbc like
the raspberry pi alongside existing linux services such as httpd and
ircd

that's what i developed it on

enjoy,
Aaron Casper
