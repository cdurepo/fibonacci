#!/usr/bin/python
#######################
# This is going to update the local file cache for the fib webservice
#
# Created by Chris Durepo May 22 2018
#######################
import json
import threading
import configparser
import time
import redis
import updatecache

config =  configparser.ConfigParser()
config.sections()
config.read('/localDir/conf/fib.conf')

file_name="/var/data/fib"
#os.remove(file_name)
fib_file=open(file_name, 'w')
fib_read=open(file_name, 'r')
file_index=0

### Setup
local_high=10
max_array=int(config['DEFAULT']['max_array'])
#Connect to redis

rdb = redis.Redis(
   host=config['DEFAULT']['redis_host'],
   port=config['DEFAULT']['redis_port']
)
print "set inital max_update"
rdb.set("max_update",int(local_high))


rdb.set('needed',0)
rdb.set('done',0)

# Function to fill array
def populate_fib_array ():
    # Changing to file
    print "Populating array to ",max_array
    count=1
    first=0
    second=1
    #Bootstrap sequence
    file_index=fib_file.write(str(first))
    rdb.set('index_'+str(count),fib_file.tell())
    file_index=fib_file.write(','+str(second))
    count+=1
    rdb.set('index_'+str(count),fib_file.tell())
    count+=1
    while count <= max_array:
        third=first+second
        current=fib_file.tell()
        fib_file.write((','+str(third)))
        rdb.set('index_'+str(count),fib_file.tell())
        rdb.set('redis_high',str(third))
        first=second
        second=third
        count+=1
    fib_file.flush()
    return

def check_needed():
    print "update running"
    global local_high
    #This is going to check to see if we need to update the local cache file
    running = 1
    while (running):
        needed=int(rdb.get("needed"))
        while (local_high < needed):
            fib_file.write((','+rdb.get(local_high+1)))
            rdb.set('index_'+str(local_high+1),fib_file.tell())
            rdb.set('done',local_high+1)
            local_high+=1
            fib_file.flush()
        time.sleep(2)



########### Main #################
print "starting service"
fib_array=populate_fib_array()
print "Done filling array"
