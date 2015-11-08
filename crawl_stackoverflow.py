'''
This code collects hyperlinks of questions asked on http://stackoverflow.com/.
Date : 6 November, 2015
Author : SiddharthaAnand(https://github.com/SiddharthaAnand/Crawling_delights)
'''

import os
import sys
import time
import random
import urllib2
from bs4 import BeautifulSoup

log_file = file("log_data", "a")
def fetch_stackoverflow_resource(current_url, request_count, timeout=300):
	try:
		print "=============================================================================="
		request_count += 1
		print "Request no ", request_count
		print "Sending Request to ", current_url, " at time ", time.asctime()
		req = urllib2.Request(current_url)

		req.add_header('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0')

		page_content = urllib2.urlopen(req)
		#page_content = urllib2.urlopen(current_url, timeout=timeout)
		print "Received response from ", current_url, " at time ", time.asctime()

		#printing in log
		print >>log_file, "=============================================================================="
		print >>log_file, "Request no ", request_count
		print >>log_file, "Sending Request to ", current_url, " at time ", time.asctime()
		print >>log_file, "Received response from ", current_url, " at time ", time.asctime()

	except Exception as e:

		print "Exception caught at time ", time.asctime()
		print "Exception tuple ", e
		sleep_time = random.randint(5, 10)
		print "Sleeping for ", sleep_time, "seconds"
		time.sleep(sleep_time)

		#printing in log
		print >>log_file, "Exception caught at time ", time.asctime()
		print >>log_file, "Exception tuple ", e
		print >>log_file, "Sleeping for ", sleep_time, "seconds"

		#continue
	return page_content

def control_board(base_url="", page_no=1, timeout=300):
	page_size = 50
	if base_url == "":
		base_url = "http://stackoverflow.com/questions?page="
		question_type = "newest"
		page_no = 1

	filename = "q_hyperlink_nextset.txt"
	q_hyperlink = file(filename, 'a+')
	hyperlink_list = []

	while page_no < 200000:
		try:
			url = base_url + str(page_no) + "&pagesize=" + str(page_size) + "&sort=newest" #+ question_type
			soup = BeautifulSoup(fetch_stackoverflow_resource(url, page_no, timeout))
			hyperlink_tag = soup.findAll('a', attrs={'class' : 'question-hyperlink'})

			for hyperlink in hyperlink_tag:
				print str(hyperlink['href'].encode("UTF-8"))

				#printing in log
				print >>log_file, str(hyperlink['href'].encode("UTF-8"))
				hyperlink_list.append(str(hyperlink['href'].encode("utf-8")))
				if page_no % 50 == 0:
					print "Writing the hyperlinks in file ", filename
					#printing in log
					print >>log_file, "Writing the hyperlinks in file ", filename
					for link in hyperlink_list:
						print >>q_hyperlink, link
					hyperlink_list = []
			time.sleep(2)
		except KeyboardInterrupt as k:
			state_file = file(store_state_file, 'w')
			print >>state_file, url
			print >>state_file, page_no
			print "Exception caught", k
			print >>log_file, "Exception caught", k
			
			state_file.close()
			print "Stored url, page no in ", store_state_file
			print "========================================================================="

			#printing in log
			print >>log_file, "Stored url, page no in ", store_state_file
			print >>log_file, "========================================================================="
			sys.exit(-1)
		except BaseException as be:
			print "Exception caught ", be
			sleep_time = random.randint(5, 10)
			print "Sleeping for ", sleep_time, " seconds"
			time.sleep(sleep_time)
			print "Resend request "
			continue
			#printing in log
			print >>log_file, "Exception caught ", be
			print >>log_file, "Sleeping for ", sleep_time, " seconds"
			print >>log_file, "Resend request"
		
		page_no += 1

if __name__ == '__main__':
	directory = "/home/admin-19/Sid/Crawling_delights/"
	store_state_file = "crawler_state.txt"
	print "Program started"
	if os.path.exists(directory + store_state_file):
		print "File found"
		state_file = file(directory + store_state_file, 'r')
		line = state_file.readlines()
		url = line[0].strip()
		page_no = int(line[1].strip())
		timeout = 300
		control_board("http://stackoverflow.com/questions?page=", page_no, timeout)
	else:
		control_board()

	print "Program stopped at ", time.asctime()

