from cooker import SoupCooker
from bs4 import BeautifulSoup
from mmGUIv2 import mmGUI
import unicodedata

class MusicManager:
	def __init__(self, query):
		self.query = query
		self.dl_link_base = 'http://89.248.172.6/dvv.php?q='

	def sanitizeQuery(self):
		pass

	def normalizeUnicode(self, data):
		#returns normalized and encoded to ascii_letters data
		if type(data) is unicode:
			data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
		return data

	def searchResults(self, count=5):
		self.query = 'http://myfreemp3.eu/music/' + self.query.replace(' ', '+')
		print self.query
		self.search_soup = SoupCooker(self.query).getSoup()
		self.results = self.search_soup.find_all('li', {'class':'track'})
		if len(self.results) > count:
			self.results = self.results[:5]

	def parseResults(self):
		if not hasattr(self,'results'):
			self.getSearchResults()
		self.parsed_results = {}
		for item in self.results:
			data = item.find(class_='info')
			self.parsed_results[int(item['id'])] = {
				'title' : self.normalizeUnicode(data.text),
				'duration' : str(int(data['data-duration'])/60)+':'+str("%02d" %(int(data['data-duration'])%60)),
				'dl_id' : self.normalizeUnicode(data['data-aid']),
				'dl_link' : self.dl_link_base+self.normalizeUnicode(data['data-aid'])
			}

	def getSearchResults(self,count=5):
		if hasattr(self,'results'):
			return self.results
		else:
			self.searchResults()
			return self.results

	def getParsedResults(self):
		if hasattr(self,'parsed_results'):
			return self.parsed_results
		else:
			self.parseResults()
			return self.parsed_results

	def printResults(self):
		if hasattr(self,'parsed_results'):
			for key in self.parsed_results:
				output = str(key)+') '
				output += self.parsed_results[key]['title']
				output += '\t[Duration - ' + self.parsed_results[key]['duration'] +']'
				print(output)
		else:
			self.parseResults()
			self.printResults()

	def buildGUI(self):
		mmGUI_instance = mmGUI(0, self.parsed_results)
		mmGUI_instance.MainLoop()