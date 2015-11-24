'''This code reads in the urls of users and extracts user information form the page.
'''

import os
import time
import random
import urllib2
from bs4 import BeautifulSoup

log_file = file("log_data_question_text", "w")
users_stackoverflow = file("users_stackoverflow.txt", 'a')

def read_links():
	filename = file("user_hyperlinks.txt", "r")
	g = filename.readlines()
	filename.close()
	user_hyperlinks = []
	for i in g:
		user_hyperlinks.append(i.strip().split("#")[2])
	return user_hyperlinks

def send_request(current_url):
	try:
		print "=============================================================================="
		#request_count += 1
		#print "Request no ", request_count
		#print "Sending Request to ", current_url, " at time ", time.asctime()
		req = urllib2.Request(current_url)

		req.add_header('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0')

		page_content = urllib2.urlopen(req)

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

	return page_content

def extract(user_hyperlinks):
	while len(user_hyperlinks) != 0:
		

		print "Frontier remaning", len(user_hyperlinks)

		relative_url = user_hyperlinks.pop(0)
		if "/users/" not in relative_url or len(user_hyperlinks) > 17287:
			continue
		user_id = relative_url.split("/")[2]
		current_url = "http://www.stackoverflow.com" + relative_url
		try:
			page_content = send_request(current_url)
		except BaseException as bee:
			print "Exception", bee
			continue

		#Use bs4
		soup = BeautifulSoup(page_content)

		#extact user information, username, location, questions answered, poeple reached, time for membership, profile views, top tags, score
		#posts, reputation, gold, silver, bronze badges

		username_tag = soup.findAll('h2', attrs={'class' : 'user-card-name'})
		try:
			location_tag = soup.findAll('ul', attrs={'class' : 'list-unstyled'})[0]
		except Exception as e:
			print "Exception caught ", e
			print >>log_file, e
			continue
		question_answered_tag = soup.find('span', attrs={'class' : 'number'})
		#people_reached_tag = soup.findAll('span', attrs={'class' : 'number'})
		#profile_view_tag = soup.findAll('ul', attrs={'class' : 'list-unstyled'})[0]
		reputation_tag = soup.find('div', attrs={'class' : 'reputation'})
		top_tags_tag = soup.findAll('a', attrs={'class' : 'post-tag'})

		#manipulate and extract information from all the tags
		username = str(username_tag[0].text.encode("UTF-8")).strip().split("\n")[0]
		location = str(location_tag.text.split("\n")[3].encode("UTF-8")).strip()
		q_answered = str(question_answered_tag.text.encode("UTF-8"))
		reputation = str(reputation_tag.text.encode("UTF-8")).strip().split()[0]

		#collct list of tags connected to the user
		tag_list = []
		buff = ""
		for tag in top_tags_tag:
			buff = buff + str(tag.text.encode("UTF-8")) + "#"

		#Write them to file
		print >>users_stackoverflow, str(user_id) + "#" + str(username) + "#" + str(location) + "#" + str(q_answered) + "#" + str(reputation) + "#" + str(buff)
		print str(user_id) + "#" + str(username) + "#" + str(location) + "#" + str(q_answered) + "#" + str(reputation) + "#" + str(buff)

	users_stackoverflow.close()

if __name__ == '__main__':
	user_hyperlinks = read_links()
	try:
		extract(user_hyperlinks)
	except BaseException as be:
		print >>log_file, be
	finally:
		users_stackoverflow.close()
