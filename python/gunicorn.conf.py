def on_starting(server):
	print "This should only print once"
	import redis
	rdb = redis.Redis(
	   host='master',
	   port="6379"
	)
	rdb.set('needed',0)
	rdb.set('done',0)
	# import threading
	# import updatecache
	# updatecache.populate_fib_array()
	# update_cache_thread = threading.Thread(target=updatecache.check_needed, args="")
	# update_cache_thread.daemon = True
	# update_cache_thread.start()
