import urllib2
from bs4 import BeautifulSoup

class SoupCooker:
	def __init__(self, url):
		#obtain the html code of the page
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36')
		cHandle = urllib2.urlopen(req)
		self.html = cHandle.read()
		cHandle.close()
		
		self.soup = BeautifulSoup(self.html)

	def getSoup(self):
		return self.soup