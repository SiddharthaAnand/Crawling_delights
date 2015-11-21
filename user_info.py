'''
	This code collects user page hyperlinks of those users who have answered questions
	on stackoverflow.com.
	Date : 21 November, 2015
	Author : SiddharthaAnand
'''

import sys
import time
import random
import urllib2
from bs4 import BeautifulSoup

log_file = file("log_data_user_links", "w")
filename = "q_hyperlink.txt"

def read_q_hyperlinks():
	f = file(filename, "r")
	g = f.readlines()
	f.close()
	hyperlink_list = []
	for i in g:
		hyperlink_list.append(i.strip())
	return hyperlink_list


def extract_user_hyperlinks(question_hyperlinks):
	'''This method takes as input list of hyperlinks of questions on stackoverflow.com
		and returns the list of userpage hyperlinks.
	'''
	f = open("user_hyperlinks.txt", "w")
	user_hyperlink_list = []
	upvote_list = []
	request_count = 0
	ques_no = 0
	while( len(question_hyperlinks) != 0 ):
		try:

			#Create request using urllib2 request
			print "=============================================================================="
			request_count += 1
			ques_no += 1
			relative_url = question_hyperlinks.pop(0)
			current_url = "http://www.stackoverflow.com" + relative_url

			print "Request no ", request_count
			print "frontier length ", len(question_hyperlinks)
			print "Sending Request to ", current_url, " at time ", time.asctime()
			req = urllib2.Request(current_url)

			req.add_header('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0')

			page_content = urllib2.urlopen(req)
			#page_content = urllib2.urlopen(current_url, timeout=timeout)
			print "Received response from ", current_url, " at time ", time.asctime()

			soup = BeautifulSoup(page_content)
		
			#Collect all answers
			answers_tag = soup.findAll('div', attrs={'id' : 'answers'})

			#extract different parts from the answer html
			a_upvote_tag = answers_tag[0].findAll('span', attrs={'itemprop' : 'upvoteCount'})
			for upvote in a_upvote_tag:
				print "Upvote loop"
				upvote_list.append(str(upvote.text.encode("UTF-8")))
				print upvote

			user_details_tag = answers_tag[0].findAll('div', attrs={'class' : 'user-details'})
			for index in range(len(user_details_tag)):
				if user_details_tag[index].a == None:
					continue
				user_hyperlink_list.append(user_details_tag[index].a['href'])
				print user_details_tag[index].a['href']
				#write to file
			for vote, link in zip(upvote_list, user_hyperlink_list):
				print str(ques_no) + "#" + str(vote) + "#" + str(link)
				print >>f, str(ques_no) + "#" + str(vote) + "#" + str(link)
			user_hyperlink_list = []
			upvote = []
		
		except KeyboardInterrupt as ki:
			f.close()
			log_file.close()		
			print "All files closed"
			sys.exit(-1)
			
		except BaseException as e:

			print "Exception caught at time ", time.asctime()
			print "Exception tuple ", e
			sleep_time = random.randint(5, 10)
			print "Sleeping for ", sleep_time, "seconds"
			time.sleep(sleep_time)

			#printing in log
			print >>log_file, "Exception caught at time ", time.asctime()
			print >>log_file, "Exception tuple ", e
			print >>log_file, "Sleeping for ", sleep_time, "seconds"

	

if __name__ == '__main__':
	q_hyperlink_list = read_q_hyperlinks()
	extract_user_hyperlinks(q_hyperlink_list)	

