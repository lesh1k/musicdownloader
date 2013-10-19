from mm import MusicManager
from mmGUI import mmGUI
import pprint

if __name__ == "__main__":
	USER_QUERY = raw_input('Your query: ')

	mm_instance = MusicManager(USER_QUERY)
	mm_instance.printResults()
	mm_instance.buildGUI()