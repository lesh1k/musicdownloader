from cooker import SoupCooker
from bs4 import BeautifulSoup
from mmGUIv2 import mmGUI
import unicodedata
import logging
import os

class MusicManager:
	def __init__(self, query):
		self.query = query
		self.dl_link_base = 'http://89.248.172.6/dvv.php?q='
		#configure logging
		current_path = '/'.join(__file__.split('/')[:-1])
		path = os.path.join(current_path, "Logs")
		if not os.path.exists(path):
			os.mkdir(path)
		path = os.path.join(path, 'debug.log')
		if not os.path.isfile(path):
			fHandle = open(path, 'w')
			fHandle.write('')
			fHandle.close()
		logging.basicConfig(
								filename=path, filemode='a', level=logging.DEBUG,
								format='[%(levelname)s] - [%(asctime)s]: %(message)s',
								datefmt='%d-%m-%Y at %H:%M:%S'
								)
		self.logger = logging.getLogger('debug')
		self.logger.setLevel(logging.DEBUG)

	def sanitizeQuery(self):
		self.logger.debug('Query sanitizing')
		pass

	def normalizeUnicode(self, data):
		#returns normalized and encoded to ascii_letters data
		if type(data) is unicode:
			self.logger.debug('Unicode normalization')
			data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
		return data

	def searchResults(self, count=5):
		self.logger.debug('Building search query')
		self.query = 'http://myfreemp3.eu/music/' + self.query.replace(' ', '+')
		print self.query
		self.logger.debug('Cooking soup')
		self.search_soup = SoupCooker(self.query).getSoup()
		self.logger.debug('Looking for results')
		self.results = self.search_soup.find_all('li', {'class':'track'})
		if len(self.results) > count:
			self.logger.debug('Selecting '+str(count)+' results')
			self.results = self.results[:count]

	def parseResults(self):
		self.logger.debug('parse results function start')
		if not hasattr(self,'results'):
			self.logger.debug('no parsed results. going to get some.')
			self.getSearchResults()
		self.parsed_results = {}
		self.logger.debug('Building results dictionary')
		for item in self.results:
			data = item.find(class_='info')
			self.parsed_results[int(item['id'])] = {
				'title' : self.normalizeUnicode(data.text),
				'duration' : str(int(data['data-duration'])/60)+':'+str("%02d" %(int(data['data-duration'])%60)),
				'dl_id' : self.normalizeUnicode(data['data-aid']),
				'dl_link' : self.dl_link_base+self.normalizeUnicode(data['data-aid'])
			}

	def getSearchResults(self,count=17):
		self.logger.debug('Getting search results')
		if hasattr(self,'results'):
			return self.results
		else:
			self.searchResults(count)
			return self.results

	def getParsedResults(self):
		if hasattr(self,'parsed_results'):
			return self.parsed_results
		else:
			self.parseResults()
			return self.parsed_results

	def printResults(self):
		self.logger.debug('Printing search results')
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
		self.logger.debug('Building GUI')
		mmGUI_instance = mmGUI(0, self.parsed_results)
		mmGUI_instance.MainLoop()