#!/usr/bin/python
#######################
# this is going to be the web service that will recive and respond to, the
# reqeust for a numbeer of fib
# Created by Chris Durepo May 22 2018
#######################
import json
import redis
from flask import Flask
from flask import request
from flask import jsonify

### Setup
max_array=1000
max_redis=10000
#Connect to redis

rdb = redis.Redis(
    host='redis',
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
    print "Populating array"
    count=2
    fib_array=[0,1]
    while count < max_array:
        fib_array.append(fib_array[count-2]+fib_array[count-1])
        #print "fib array count is:",fib_array[count]
        count+=1
    return fib_array

def populate_fib_redis (fib_one, fib_two):
    print "Populating redis"
    count=max_array+1
    while count < max_redis:
        value=fib_one+fib_two
        rdb.set(count,value)
        count+=1
        fib_one=fib_two
        fib_two=value
    return

def create_output (length, fib_array):
    #This is the function that will walk the array and return the array
    #for the given position
    if length <= max_array:
        fib_output=fib_array[0:length]
    else:
        print "range",range(max_array+1,length+1,1)
        fib_output=fib_array
        fib_output.extend(rdb.mget(range(max_array+1,length+1,1)))
    return fib_output

print "starting service"
fib_array=populate_fib_array()
print "Done filling array"
#print "10:",create_output(10000, fib_array)
print "Start filling redis"
populate_fib_redis(fib_array[-2], fib_array[-1])
print "redis populated"

#Building the webservice app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def hello_world():
    try:
         length = int(request.args.get('fib'))
    except:
        return jsonify(response="error", message="invalid reqeust, reqeust must be an integer")

    if (length > 0):
        if ((length <= max_array) or ((length > max_array) and (rdb.exists(length)))):
            return  jsonify(response="success",output=create_output(length, fib_array))
        else:
                return jsonify(response="error", message="Not calculated yet please try again later")
    else:
            return jsonify(response="error",message="invalid reqeust")
