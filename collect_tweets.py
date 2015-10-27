#This code takes into account the twitter REST API and collects information
#regarding tweets on movies.
#Query is the movie name
#Results are stored in json format.
#author : SiddharthaAnand
#https://github.com/SiddharthaAnand/Crawling_delights

import os
import tweepy
import time
import sys
import json
import movies_name

consumer_key = "sxs8aEROib01jaCKYrctKVAyqqid"
consumer_secret = "sP92rzVMq4Kx5TArhdntRzqCkNetAGd9nR60GhlRBezTRfBYO5mid"
access_token="s1145526739-wpafPpg41vb8c4qOMhYZjocFstZi7l9rXug1Btoid"
access_token_secret="shqJPdYPaliso3MkXoL5twTJkm3oVvcYur3ivSxAxI2E4fid"


def authenticate():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	return api

#def collect_tweets(api, query):
def collect_tweets(api, dest_file):
	start_time = time.time()
	requests = 0
	dict = {}
	user = 0
	composite_data = {}
	movies  = movies_name.value
	try:
		for query in movies:
			requests = 0
			try:

				for tweet in tweepy.Cursor(api.search, q=query, count=100).items():
					requests += 1
					user += 1

					dict['author_screen_name'] = tweet.author.screen_name
					dict['created_at'] = str(tweet.created_at)
					dict['author_id'] = tweet.author.id
					dict['author_followers_count'] = tweet.author.followers_count
					dict['location'] = tweet.author.location
					dict['text'] = tweet.text
					dict['retweeted'] = tweet.retweeted
					composite_data[str("user_") + str(user)] = dict
					dict = {}
					time.sleep(1)
					if (requests % 50) == 0 and long(time.time() - start_time) < 60:
						snooze = int(60 - (long(time.time()) - start_time))
						time.sleep(snooze)
						print query, "Sleeping for___________", snooze
						start_time = time.time()
						#requests = 0
					
					print query, requests, tweet.created_at, time.asctime()
			except Exception as g:
				print "Exception inside_______________", g
				print "Sleeping for a few minutes_____"
				time.sleep(1200)#20 Minutes
				continue

					
	except Exception as e:
		print "Exception encountered", e
	finally:
		print "Writing to file__________", dest_file
		f = open(dest_file, "a")
		js = json.dumps(composite_data)
		print >>f, js
		f.close()
		print "File Size", os.path.getsize(dest_file)


if __name__ == '__main__':
	#query = sys.argv[1]
	dest_file = sys.argv[1]
	api = authenticate()
	#collect_tweets(api, query)
	collect_tweets(api, dest_file)