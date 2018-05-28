#!/usr/bin/python
#######################
# this is going to be the web service that will recive and respond to, the
# reqeust for a numbeer of fib
# Created by Chris Durepo May 22 2018
#######################
import json
import redis
import threading
import os
from flask import Flask
from flask import request
from flask import jsonify
from rediscluster import StrictRedisCluster


max_redis=2000
#Connect to redis

rdb = redis.Redis(
   host='master',
   port="6379"
)

#print "testing rdb"
#rdb.set('test', 'pass')
#value = rdb.get('test')
#print "Value:",value
#value = rdb.get(1001)
#print "1001:",value


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
