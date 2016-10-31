from flask import Flask, request, jsonify, session, render_template, redirect, url_for
import time
from HTMLParser import HTMLParser
import tweepy
import json
from threading import Thread
from tweepy.streaming import StreamListener
from tweepy import Stream
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth



temp={}

class MyListener(StreamListener):

    def on_error(self, status):
		print(status)

    def on_data(self, data):
		decoded = json.loads(data)
		if decoded.get('coordinates',None) is not None:
			coordinates = decoded.get('coordinates','').get('coordinates','')
			temp["text"]= decoded['text']
			temp["id"]= str(decoded['id'])
			temp["name"]= decoded['user']['screen_name']
			temp["latitude"]= str(decoded['coordinates']['coordinates'][1])
			temp["longitude"]= str(decoded['coordinates']['coordinates'][0])
			temp["search_key"]= 'trump'
			final = json.dumps(temp)
			host = ''
			awsauth = AWS4Auth('', '', 'us-east-1', 'es')

			es = Elasticsearch(
					hosts=[{'host': host, 'port': 443}],
					http_auth=awsauth,
					use_ssl=True,
					verify_certs=True,
					connection_class=RequestsHttpConnection
			)
			res = es.index(index="tweet-index", doc_type='tweet', id=temp["id"], body=final)
			print(res['created'])
		return True	

if __name__ == '__main__':
	auth = tweepy.OAuthHandler("", "")
	auth.set_access_token("", "")

	api = tweepy.API(auth)
	#track = ['obama', 'trump', 'manchester', 'pogba', 'clinton']
	start_time = time.time()
	twitter_stream = Stream(auth, MyListener())
	twitter_stream.filter(track=['pogba', 'trump', 'manchester', 'clinton', 'rashford', 'zlatan', 'rooney', 'mourinho', 'messi', 'ronaldo'])

