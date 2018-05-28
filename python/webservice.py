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
import tornado.escape
import tornado.ioloop
import tornado.web
from flask import Flask
from flask import request
from flask import jsonify
from rediscluster import StrictRedisCluster



file_name="/var/data/fib"
#os.remove(file_name)
fib_file=open(file_name, 'w')
fib_read=open(file_name, 'r')
file_index=0

### Setup
local_high=10
max_array=10
max_redis=20
message="test"
#Connect to redis

rdb = redis.Redis(
   host='master',
   port="6379"
)

print "testing rdb"
rdb.set('test', 'pass')
value = rdb.get('test')
print "Value:",value
value = rdb.get(1001)
print "1001:",value


# Function to fill array
def populate_fib_array ():
    # Changing to file
    print "Populating array to ",max_array
    count=1
    first=0
    second=1
    #Bootstrap sequence
    file_index=fib_file.write(str(first))
    print "file_index:",file_index
    rdb.set('index_'+str(count),fib_file.tell())
    file_index=fib_file.write(','+str(second))
    count+=1
    rdb.set('index_'+str(count),fib_file.tell())
    count+=1
    while count <= max_array:
        third=first+second
        print "adding:",third
        current=fib_file.tell()
        fib_file.write((','+str(third)))
        rdb.set('index_'+str(count),fib_file.tell())
        rdb.set('redis_high',str(third))
        first=second
        second=third
        count+=1
    fib_file.flush()
    return


def create_output (length):
    #This is the function that will walk the array and return the array
    #for the given position
    global local_high
    print "local_high:",local_high
    if length <= local_high:
        fib_read.seek(0)
        fib_output=fib_read.read(int(rdb.get('index_'+str(length))))
    else:
        # If the length is more than we have in the cache file_name
        # We need to update the cache file and then return the whole thing.
        while (local_high < length):
            fib_file.write((','+rdb.get(local_high+1)))
            rdb.set('index_'+str(local_high+1),fib_file.tell())
            local_high+=1

        fib_file.flush()
        fib_read.seek(0)
        fib_output=fib_read.read(int(rdb.get('index_'+str(length))))
        #fib_output=fib_read.read()
        #fib_output.extend(rdb.mget(range(max_array+1,length+1,1)))
    message=fib_output
    return


########### Main #################
print "starting service"
fib_array=populate_fib_array()
print "Done filling array"

#Building the webservice app
# app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False
#
# @app.route("/")
def hello_world(length):
    try:
         length = int(length)
    except:
        return jsonify(response="error", message="invalid reqeust, reqeust must be an integer")

    if (length > 0):
        if ((length <= local_high) or ((length > local_high) and (rdb.exists(length)))):
            #print "current high",high
            return  jsonify(response="success",output=create_output(length))
        else:
            return jsonify(response="error", message="Not calculated yet please try again later")
    else:
            return jsonify(response="error",message="invalid reqeust")


class get_fib(tornado.web.RequestHandler):
    def get(self, id):
        hello_world(id)
        self.write(message)

application = tornado.web.Application([
    (r"/fib/([0-9]+)",get_fib)
])

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
