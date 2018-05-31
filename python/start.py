#!/usr/bin/python
#########
# This is going to be the start script for the fib server.
# It should be the single interface to start all the scripts needed to work.
##########
import logging
import json
import redis
import threading
import configparser

import updatecache
import os

# Get config info

print "Loading Config"

config =  configparser.ConfigParser()
config.sections()
config.read('/localDir/conf/fib.conf')
log_file=str(config['DEFAULT']['logging_dir'])+str(config['DEFAULT']['log_file'])
print "log_file",str(log_file)
logging.basicConfig(filename=log_file,level=logging.DEBUG)

max_redis=int(config['DEFAULT']['max_redis'])
print "Config loaded"


print "Starting local cache file"
## Start the local cache file_updater
update_cache_thread = threading.Thread(target=updatecache.check_needed, args="")
update_cache_thread.daemon = True
update_cache_thread.start()

print "Starting Service"
# Now we need to start the gunicor service.
cmd ="gunicorn -b 0.0.0.0 -w 1 --keep-alive 10 webservice:app"
return_value = os.system(cmd)
print ('return_value:', return_value)
