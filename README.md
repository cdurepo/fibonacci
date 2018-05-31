# fibonacci
** Web Service to return numbers in order in the Fibonacci sequence **

## Summary
This is a service that will work as a RestAPI to deliver the Fibonacci numbers to the requested depth.  
It uses a reds server to store the numbers and a local file to cache what is needed.  You are able to scale the
redis and web servers as you need to deliver to your requirements. The redis servers are in a cluster that is monitored by sentinel.  If a redis server goes down a a new one will be started and added to the cluster.

Redis cluster provided by:
https://github.com/mustafaileri/redis-cluster-with-sentinel

## Design
The web service uses a local cache file to serve the sequence of numbers.  A small initial file is created.  At the same time another server is doing calculations to populate the redis array with a much larger series of numbers.  When a call is made to the web service it looks to see if if the value needed is in the local cache, if it is not it looks to see if redis has the requests value.  If redis has the value the local cache is updated and the response is sent back with the request.

These are the parts of the service

* Redis Cluster: with sentinel monitoring and management
* Redis populator service: to fill the redis array
* Updater service: to keep he local cache up-to-date as needed
* Web Service: Rest API to receive and respond to requests.


## Installation

Build and start services
From inside the repo run
```
docker build docker -f docker/Dockerfile.redispop --rm -t redispop/devel
```
```
docker build docker -f docker/Dockerfile.websrvr --rm -t websrvr/devel
```
```
docker build docker -f docker/Dockerfile.python --rm -t python/devel
```
```
cd docker
```
```
docker-compose up --build
```
Leave that running and in a new tab verify the servers are up.
Again from inside the docker directory run
```
docker-compose ps
```
You should see
```
Name                     Command               State    Ports  
---------------------------------------------------------------------
docker_master_1     docker-entrypoint.sh redis ...   Up      6379/tcp
docker_python_1     /bin/bash                        Up              
docker_redispop_1   /bin/bash                        Up              
docker_sentinel_1   entrypoint.sh                    Up      6379/tcp
docker_slave_1      docker-entrypoint.sh redis ...   Up      6379/tcp
docker_websrvr_1    ./run.sh                         Up  
```
This is the minimum number of servers needed to work, we will add servers later.
List the running images
```
docker container ls
```
Attach to the "python" server to access RestAPI
Use the container ID for the image named docker_python_1
```
docker exec -it <container id> /bin/bash
```
## Testing
Verify the web service is running.
The first command will give results via the cache file
The second will connect to redis, update the cache file, and then return results.
```
curl http://websrvr:8000/?fib=10
curl http://websrvr:8000/?fib=20
curl http://websrvr:8000/?fib=3000
```
If you run these commands you should errors
```
curl http://websrvr:8000/?fib=b
curl http://websrvr:8000/?fib=0
```
If you run these commands you should get a warning
```
curl http://websrvr:8000/?fib=0
curl http://websrvr:8000/?fib=10001
```
If you want to increase the number of servers you can running
```
docker-compose scale sentinel=3
docker-compose scale slave=3
docker-compose scale websrvr=3
```
This will raise the number of each by 3 giving you nice redundancy.
The web servers are balanced via DNS but a more load balancer could be use.  
You can also scale down the number of servers. The value you give is the total number of servers of that kind so Docker will start or stop the number of servers need to reach it.

When you are done you can just run this to shut everything down
```
docker-compose down
```
## Configuration
There is a file in the repo call fib.conf, this is used by a number of the servers to setup the environment.

* Max array -- The max local array on boot
* Max redis  -- The max redis will be populated
* Log Dir and Log file are only for the web server
* Redis host and port  -- hostname or address of the redis server
* Workers -- number of threads for each web server

## Limits
I have tested this on my older laptop to over 40,000 places.  However after that it starts to have issues.  The only real limit on it should be hardware.  Python can handle the large integers without issue, redis will be fine as long as you keep adding servers.  Basically once you decide what your requirements are, as long as you can supply enough hardware it should work.

The docker process has only been tested on a Mac as that is the only server I have to test with.  I assume it would work with other types but I have no way of verifyting.

## Troubleshooting
* Web Server not responding.  
  Reboot the web server.  Because of the way the cache file is created it is just best to take the host down and replace it with another one.
* Redis host went down
  Sentinal will redeploy a redis host if one dies.  
* Redis Pop server went down.
  Check the max_redis value on redis, if it is where you want it, just leave the server down.  If you restart it, it will rebuild the DB from 0 so it is not worth it unless you really need to increase the count.

## Future progress
* Make redispop recover and continue where it left off
* Test with other hardware
* Make rpm's and eggs for people that don't want to deploy with docker
* Improve logging and logging options
