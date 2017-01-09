import pickle
import re
import sys
import time
import urllib2
from bs4 import BeautifulSoup


def process_url(base_url):
	'''
	Process and return different parts of the url.
	'''
	pass

def start(base_url):
	
	node_number = 1
	queue = [base_url]
	visited_urls = {base_url : node_number}
	
	start_index = base_url.index('www.') + len('www.')
	end_index = base_url.index('.org')
	edge_f = file(base_url[start_index : end_index] + '_graph_structure', 'w')
	urls_f = file(base_url[start_index : end_index] + '_url_structure', 'w')
	

	while len(queue) > 0:
		current_url = queue.pop(0)
		try:
			print "Sending Request:\t", current_url
			page = urllib2.urlopen(current_url)
			print "Received Response at time :\t", time.asctime()
			soup = BeautifulSoup(page)
			website_urls = soup.findAll('a', attrs = {'href' : re.compile(base_url)})
			
			for url in website_urls:
				if url['href'] not in visited_urls:
					node_number += 1
					visited_urls[url['href']] = node_number
					queue.append(url['href'])
					print >>edge_f, visited_urls[current_url], visited_urls[url['href']]
					print visited_urls[current_url], visited_urls[url['href']]
					#time.sleep(2)
				else:
					print >>edge_f, visited_urls[current_url], visited_urls[url['href']]
			print "-" * 20
			print "Queue length:\t", len(queue)
			print "Visited urls:\t", len(visited_urls)
			print "-" * 20
			print "Politely sleeping:\t 1 sec", time.sleep(1)
				
		except Exception as e:
			print "Exception", e
			continue
			#sys.exit(1)

	edge_f.close()
	pickle.dump(visited_urls, urls_f)
	urls_f.close()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		base_url = sys.argv[1]
		start(base_url)
	else:
		print '\n\nUsage: Enter seed url to begin\n\n'
		sys.exit(1)

