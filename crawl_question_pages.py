'''
This code stores the text of questions + answers on webpages of questions asked on http://stackoverflow.com/.
Date : 6 November, 2015
Author : SiddharthaAnand(https://github.com/SiddharthaAnand/Crawling_delights)
'''

import os
import time
import random
import urllib2
from bs4 import BeautifulSoup

log_file = file("log_data_question_text", "w")
def fetch_stackoverflow_resource(current_url, request_count, timeout=300):
	try:
		print "=============================================================================="
		request_count += 1
		print "Request no ", request_count
		print "Sending Request to ", current_url, " at time ", time.asctime()
		page_content = urllib2.urlopen(current_url, timeout=timeout)
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

def control_board(base_url, store_state_file="" ):
	ques_no = 1
	hyperlink_list = []
	store_state_file = "crawler_state_question_text.txt"
	directory = "/home/admiin-19/Sid/Crawling_delights/text_dataset/"
	#Prefix of the naem of the text data file
	filename = "question_"
	fp = file("Taglist.txt", "a+")

	if store_state_file == "":
		
		#Extract hyperlinks from q_hyperlinks.txt
		f_hyperlinks = file("q_hyperlinks.txt", "r")
		lines = f_hyperlinks.readlines()
		f_hyperlinks.close()
		for line in lines:
			hyperlink_list.append(line.strip())

	else:
		#Extract hyperlinks from store_state_file
		f_hyperlinks = file(store_state_file, "r")
		lines = f_hyperlinks.readlines()
		f_hyperlinks.close()
		for line in lines:
			hyperlink_list.append(line.strip())

	while len(hyperlink_list) != 0:
		
		try:
			url = base_url + hyperlink_list.pop(0)
			soup = BeautifulSoup(fetch_stackoverflow_resource(url))
			text_tag = soup.findAll('div', attrs={'class' : 'post-text'})
			tag_tag = soup.findAll('a', attrs={'class' : 'post-tag js-gps-track'})
			raw_text = ""

			#Extracting the text out from html source
			for text in text_tag:
				p_text_tag = text.findAll('p')
				for p_text in p_text_tag:
					raw_text = raw_text + str(p_text.text.encode("UTF-8")) + " "

			#Write the raw text in the file
			file_pointer = file(directory + filename + str(ques_no) + ".txt", "w")
			print >>file_pointer, raw_text
			file_pointer.close()
			
			#Extract subject tags
			tags = ""
			for tag in tag_tag:
				tags = tags + "#" str(tag.text.encode("UTF-8"))

			#Write the tags in another file
			print >>fp, str(ques_no) + "#" + tags

			#Increment the question id by 1
			ques_no += 1
			print "Time for Interrupt"
			print >>log_file, "Time for Interrupt"
			time.sleep(3)
		
		except KeyboardInterrupt as k:
			state_file = file(store_state_file, 'w')
			for rel_url in hyperlink_list:
				print >>state_file, rel_url
			print "Exception caught", k
			print >>log_file, "Exception caught", k
			state_file.close()
			fp.close()
			print "Pending queue ", store_state_file
			print "========================================================================="

			#printing in log
			print >>log_file, "Stored url, page no in ", store_state_file
			print >>log_file, "========================================================================="
			log_file.close()
			sys.exit(-1)

		except BaseException as be:
			print "Exception caught ", be
			sleep_time = random.randint(5, 10)
			print "Sleeping for ", sleep_time, " seconds"
			time.sleep(sleep_time)
			print "Resend request "
			#printing in log
			print >>log_file, "Exception caught ", be
			print >>log_file, "Sleeping for ", sleep_time, " seconds"
			print >>log_file, "Resend request"
			continue

if __name__ == '__main__':
	directory = "/home/admin-19/Sid/CrawlingDelights/"
	store_state_file = "crawler_state_question_text.txt"
	
	if os.path.exists(directory + store_state_file):
		control_board("http://stackoverflow.com", store_state_file)
	else:
		control_board("http://stackoverflow.com")
	print "Program stopped at ", time.asctime()

