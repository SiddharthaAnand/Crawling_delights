import time
import urllib2
import logging
from Queue import Queue
from threading import Thread, active_count
from bs4 import BeautifulSoup


crawlable_urls = Queue(maxsize=0)
author_no = 0
authors = set()
fp = file("Edges.txt", "w")
	
def send_request(crawlable_urls, authors):
	author_no = 0
	while author_no < 1:
		author_no += 1
		url = crawlable_urls.get()
		try:
			print "Request sent to ", url
			page = urllib2.urlopen(url)
			print "Response received"
		except Exception as e:
			print "Exception Caught: ", e
		soup = BeautifulSoup(page)
		coauthor_tags = soup.findAll('div', attrs={'class' : 'person'})
		name_tag = soup.find('span', attrs={'itemprop' : 'name'})
		
		print name_tag.text
		for coauthors in coauthor_tags:
			if coauthors.a['href'] not in authors:
				authors.add(coauthors.a['href'])
				print "In queue", coauthors.a['href']				
				print coauthors.a.text.encode("utf-8")
				print >>fp, name_tag.text.encode("utf-8"), coauthors.a.text.encode("utf-8")
		crawlable_urls.task_done()
	
thread_count = 5
for i in range(thread_count):
	print "Thread", i
	worker = Thread(target=send_request, args=(crawlable_urls, authors))
	worker.setDaemon(True)
	worker.start()

seed = ["http://dblp.uni-trier.de/pers/hd/b/Basuchowdhuri:Partha", \
		"http://dblp.uni-trier.de/pers/hd/c/Chan:Jeffrey", \
		"http://dblp.uni-trier.de/pers/hd/p/Parhar:Ajeet", \
		"http://dblp.uni-trier.de/pers/hd/l/Leckie:Christopher", \
		"http://dblp.uni-trier.de/pers/hd/c/Challa:Subhash"
		]

for s in seed:
	authors.add(s)
print "Spinning"
for s in seed:
	crawlable_urls.put(s)
crawlable_urls.join()
fp.close()
