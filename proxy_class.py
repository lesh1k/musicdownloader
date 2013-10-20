import time
from threading import Thread

class caching_proxy:
	def __init__(self):
		#prepare vars for proxy
		self.dl_requests = 0
		self.requests = []

	def addRequest(self, some_request):
		self.dl_requests += 1
		if self.dl_requests == 1:
			print "Gathering requests - 15 seconds."
			self.start_time = time.time()
			Thread(target=self.caching).start()

		self.requests.append(some_request)

	def caching(self):
		while True:
			if time.time()-self.start_time > 15:
				for some_thread in self.requests:
					some_thread.start()
				#reset vars
				self.dl_requests = 0
				self.requests = []
				break
			else:
				time.sleep(2)