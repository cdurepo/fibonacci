# fibonacci
** Web Service to return numbers in order in the Fibonacci sequence **

## Summary
This is a service that will work as a RestAPI to deliver the Fibonacci numbers to the requested depth.  
It uses a reds server to store the numbers and a local file to cache what is needed.  You are able to scale the
redis and web servers as you need to deliver to your requirements. The redis servers are in a cluster that is monitored by sentinel.  If a redis server goes down a a new one will be started and added to the cluster.   

Redis cluster provided by:
https://github.com/mustafaileri/redis-cluster-with-sentinel



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
Name                     command                State     Ports
--------------------------------------------------------------------
docker_master_1     docker-entrypoint.sh redis ...   Up      6379/tcp
```
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
Verify the web service is running.
The first command will give results via the cache file
The second will connect to redis, update the cache file, and then return results.
```
curl http://websrvr:8000/?fib=10
curl http://websrvr:8000/?fib=20
```
