#!/usr/bin/python
#######################
# This is the process that will populate the redis array with the fibonacci
# sequence. 
# Created by Chris Durepo May 22 2018
#######################
import json
import redis
import threading
import configparser


config =  configparser.ConfigParser()
config.sections()
config.read('/localDir/conf/fib.conf')
max_redis=int(config['DEFAULT']['max_redis'])
#Connect to redis

rdb = redis.Redis(
   host=config['DEFAULT']['redis_host'],
   port=config['DEFAULT']['redis_port']
)

print "testing rdb"
rdb.set('test', 'pass')
value = rdb.get('test')

def populate_fib_redis ():
    print "Populating redis"
    count=1
    redis_high=0
    rdb.set(count,0)
    count+=1
    rdb.set(count,1)
    count+=1
    fib_one=0
    fib_two=1
    while count <= max_redis:
        value=fib_one+fib_two
        rdb.set(count,value)
        rdb.set('redis_high',count)
        count+=1

        fib_one=fib_two
        fib_two=value
    return


########### Main #################
print "starting service"
print "Start filling redis"
# Background redis population
populate_fib_redis()
#fill_redis_thread = thread = threading.Thread(target=populate_fib_redis)
#fill_redis_thread.start()
print "redis populated"
