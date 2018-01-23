import requests
import re
import time
from bs4 import BeautifulSoup
import random

user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]

queue = []
visited_urls = {}
headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) \
		AppleWebKit/537.36 (KHTML, like Gecko) \
		Chrome/27.0.1453.93 \
		Safari/537.36'}

seed_url = "https://dl.acm.org/author_page.cfm?id=81100512920&srt=publicationDate&role=all&dsp=coll"
base_url = "https://dl.acm.org/author_page.cfm?id="
query_params = "&srt=publicationDate&role=all&dsp=coll"

def crawl(seed_url, base_url):
	queue.append(seed_url)
	visited_urls[seed_url] = 1
	while(len(queue) != 0):
		url  = queue.pop(0)
		print "Sending request to ", url
		headers['user-agent'] = user_agent_list[random.randint(0, len(user_agent_list))]

		page = requests.get(url, headers=headers)
		print "Received response at ", time.asctime()
		#print url
		soup = BeautifulSoup(page.content, "lxml")
		span_tag = soup.findAll('span', attrs={'class' : 'small-text'})
		#print span_tag
		author_name = span_tag[0].text.encode('utf-8')
		#print author_name
		author_affiliation_tag = soup.findAll('a', attrs={'href' : re.compile('inst_page.cfm?')})
		#print author_affiliation_tag
		author_affiliation = [affiliation.text.encode('utf-8') for affiliation in author_affiliation_tag]
		print author_name, author_affiliation

		auth_id_tag = soup.findAll('a', attrs={'target': '_self'})
		coauthor_id_list = []
		for auth in auth_id_tag:
			id_index = auth['href'].encode('utf-8').index('id')
			_id = auth['href'].encode('utf-8')[id_index+3:]
			coauthor_id_list.append(_id)

		for _id in coauthor_id_list:
			new_url = base_url + _id + query_params
			if new_url not in visited_urls:
				visited_urls[new_url] = 1
				queue.append(new_url)
		print "Size of queue: ", len(queue)
		print "Number of unique urls ", len(visited_urls)

		time.sleep(random.randint(0, 3))
		
crawl(seed_url, base_url)