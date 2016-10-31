from flask import Flask, request, jsonify, session, render_template, redirect, url_for
import time
import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import Stream
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

app = Flask(__name__)

host = ''
awsauth = AWS4Auth('', '', 'us-east-1', 'es')

es = Elasticsearch(
		hosts=[{'host': host, 'port': 443}],
		http_auth=awsauth,
		use_ssl=True,
		verify_certs=True,
		connection_class=RequestsHttpConnection
)


@app.route("/search", methods=['POST'])
def search():
	req = request.json
	print req
	search_key = req['search_key']
	search_key = search_key.lower()
	latitude = []
	longitude = []
	text = []
	name = []
	
	res = es.search(index="tweet-index", body={"query": {"wildcard": {"text":'*'+search_key+'*'}}},size=400)
	print("Got %d Hits:" % res['hits']['total'])
	hits = res['hits']['hits']
	if hits:
		for hit in hits:
			print hit
			latitude.append(hit['_source']['latitude'])
			longitude.append(hit['_source']['longitude'])
			text.append(hit['_source']['text'])
			name.append(hit['_source']['name'])

	return jsonify({'latitude' : latitude, 'longitude' : longitude, 'text' : text, 'name' : name})

@app.route("/")
def main():
	print(es.info())
	return render_template('index.html')

if __name__ == "__main__":
	app.run()