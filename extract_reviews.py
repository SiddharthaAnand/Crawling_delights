#extract reviews of users from imdb.com 

import urllib2
from bs4 import BeautifulSoup

def extract_reviews(url, current_page, total_pages):
	start = 0
	review_no = 296
	
	while current_page <= total_pages:
		
		
		absolute_url = "http://www.imdb.com/title/tt3696192/reviews?start=" + str(start)
		current_page += 1
		start += 10
		print "current_page ", current_page
		page = urllib2.urlopen(absolute_url)

		soup = BeautifulSoup(page)

		#extract reviews
		img_tag = soup.findAll('img', attrs={'width' : '102'})
		text = soup.findAll('div', attrs={'id' : 'tn15content'})
		reviews_tag = text[0].findAll('p')
		review_list = []

		for r in reviews_tag:
			if "<a" not in str(r.text.encode("UTF-8")) and len(r.text) > 100:
				review_list.append(str(r.text.encode("UTF-8")))

		if len(review_list) == len(img_tag):
			index = 0
			for img in img_tag:
				if int(img['alt'][0]) >= 5 and int(img['alt'][0]) <= 7:
					print "rating ", img['alt'][0] 
					index += 1
					f = file("review_" + str(review_no) + ".txt", "w")
					#print "review_no ", review_no
					print >>f, review_list[index]
					review_no += 1
					f.close()

if __name__ == '__main__':
	#url of the review web page without the number in the end when you click on the first page review
	url = "http://www.imdb.com/title/tt3696192/reviews?start="

	#total number of pages of review written on the web page, start_page = page from which you want the review
	#total_pages = page till which you want the review
	start_page = 1
	total_pages = 3

	#extact and store in the current directory
	extract_reviews(url, 1, total_pages)


