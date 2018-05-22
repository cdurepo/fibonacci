#!/usr/bin/python
import json
#######################
# this is going to be the web service that will recive and respond to, the
# reqeust for a numbeer of fib
# Created by Chris Durepo May 22 2018
#######################


# Function to fill array
def populate_fib_array ():
    print "Populating array"
    count=2
    fib_array=[1,1]
    while count < 10000:
        fib_array.append(fib_array[count-2]+fib_array[count-1])
        #print "fib array count is:",fib_array[count]
        count+=1
    return fib_array
def create_output (length, fib_array):
    #This is the function that will walk the array and return the array
    #for the given position
    output=fib_array[0:length]
    print "output",output
    print "json",json.dumps(output, separators=(',',':'))
    return

print "starting service"
fib_array=populate_fib_array()
print "Done filling array"
print "10:",create_output(10000, fib_array)
