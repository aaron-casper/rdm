killall -s 9 python
sleep 15s
rm /tmp/rdm_agent.pid
sleep 15s
python /home/wfh/rdm_agent/rdm_age.py &

