# fibonacci
This is a service that will work as a RestAPI to deliver the Fibonacci numbers to the requested depth.  
It uses a reds server to store the numbers and a local file to cache what is needed.  You are able to scale the
redis and web servers as you need to deliver to your requirements. The redis servers are in a cluster that is monitoed by sentinal.  If a redis server goes down a a new one will be started and added to the cluster.   
