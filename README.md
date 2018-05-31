# fibonacci
** Web Service to return numbers in order in the Fibonacci sequence

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
Again from inside the docker directory running
```
docker-compose ps
```
You should see
Name                     Command               State    Ports  
---------------------------------------------------------------------
docker_master_1     docker-entrypoint.sh redis ...   Up      6379/tcp
docker_python_1     /bin/bash                        Up              
docker_redispop_1   /bin/bash                        Up              
docker_sentinel_1   entrypoint.sh                    Up      6379/tcp
docker_slave_1      docker-entrypoint.sh redis ...   Up      6379/tcp
docker_websrvr_1    ./run.sh                         Up  
