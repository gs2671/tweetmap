from flask import Flask, request, jsonify, session, render_template, redirect, url_for
import tweepy
import json
from threading import Thread
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
from requests_aws4auth import AWS4Auth

es = Elasticsearch()

app = Flask(__name__)

@app.route("/getGeo", methods=['POST'])
def getGeo():
	req = request.json
	keyword = req['key']
	"""res = {"took":47,
	 "timed_out":"false",
	 "_shards":{"total":5,"successful":5,"failed":0},
	 "hits":{
	 	"total":1,
	 	"max_score":1.0,
	 	"hits":
	 		[{
	 			"_index":"tweetmap",
	 			"_type":"tweet",
	 			"_id":"AVgGvHUOH57OLKGhrmyx",
	 			"_score":1.0,
	 			"_source":
	 			{
	 				"in_reply_to_status_id_str":"null",
	 				"in_reply_to_status_id":"null",
	 				"created_at":"Thu Oct 27 15:22:25 +0000 2016",
	 				"in_reply_to_user_id_str":"null",
	 				"source":"<a href=\"http://instagram.com\" rel=\"nofollow\">Instagram<\/a>",
	 				"retweet_count":0,
	 				"retweeted":"false",
	 				"geo":
	 					{
	 						"coordinates":[19.38374488,-99.1670182],"type":"Point"
	 					},
	 				"filter_level":"low",
	 				"in_reply_to_screen_name":"null",
	 				"is_quote_status":"false",
	 				"id_str":"791661336614744064",
	 				"in_reply_to_user_id":"null",
	 				"favorite_count":0,
	 				"id":791661336614744064,
	 				"text":"Asi Bruni yorkie saluda su amigo Polo englishbulldog #paseosperrunos delvalle",
	 				"place":
	 					{
	 						"country_code":"MX",
	 						"country":"Mexico",
	 						"full_name":"Benito Juarez, Distrito Federal",
	 						"bounding_box":
	 							{
	 								"coordinates":[[[-99.191996,19.357102],[-99.191996,19.404124],[-99.130965,19.404124],[-99.130965,19.357102]]],
	 								"type":"Polygon"
	 							},
	 						"place_type":"city",
	 						"name":"Benito Juarez",
	 						"attributes":{},
	 						"id":"7d93122509633720",
	 						"url":"https://api.twitter.com/1.1/geo/id/7d93122509633720.json"
	 					},
	 				"lang":"es",
	 				"favorited":"false",
	 				"possibly_sensitive":"false",
	 				"coordinates":
	 					{
	 						"coordinates":[-99.1670182,19.38374488],
	 						"type":"Point"
	 					},
	 				"truncated":"false",
	 				"timestamp_ms":"1477581745662",
	 				"entities":
	 					{
	 						"urls":
	 							[{
	 								"display_url":"instagram.com/p/BMEjwdnhcx0/",
	 								"indices":[92,115],
	 								"expanded_url":"https://www.instagram.com/p/BMEjwdnhcx0/",
	 								"url":"https://t.co/8IEYevBf7n"
	 							}],
	 						"hashtags":
	 							[{
	 								"indices":[10,17],"text":"yorkie"
	 							 },
	 							 {
	 							 	"indices":[39,54],"text":"englishbulldog"
	 							 },
	 							 {
	 							 	"indices":[55,70],"text":"paseosperrunos"
	 							 },
	 							 {
	 							 	"indices":[71,80],"text":"delvalle"
	 							 },
	 							 {
	 							 	"indices":[81,90],"text":"happydog"
	 							 }],
	 						"user_mentions":[],
	 						"symbols":[]
	 					},
	 				"contributors":"null",
	 				"user":
	 					{
	 						"utc_offset":-18000,
	 						"friends_count":1418,
	 						"profile_image_url_https":"https://pbs.twimg.com/profile_images/788914649651556352/MP-n3bIh_normal.jpg",
	 						"listed_count":17,
	 						"profile_background_image_url":"http://abs.twimg.com/images/themes/theme1/bg.png",
	 						"default_profile_image":"false",
	 						"favourites_count":4059,
	 						"description":"Perro paseos y campamentos, perro/gato estetica. Whats 9841531229 Cel 5537530821 Instagram @happy_tails_df",
	 						"created_at":"Sun Dec 14 00:25:13 +0000 2014",
	 						"is_translator":"false",
	 						"profile_background_image_url_https":"https://abs.twimg.com/images/themes/theme1/bg.png",
	 						"protected":"false",
	 						"screen_name":"YuliyaLolito",
	 						"id_str":"2929028424",
	 						"profile_link_color":"0084B4",
	 						"id":2929028424,
	 						"geo_enabled":"true",
	 						"profile_background_color":"C0DEED",
	 						"lang":"en",
	 						"profile_sidebar_border_color":"C0DEED",
	 						"profile_text_color":"333333",
	 						"verified":"false",
	 						"profile_image_url":"http://pbs.twimg.com/profile_images/788914649651556352/MP-n3bIh_normal.jpg",
	 						"time_zone":"Central Time (US & Canada)",
	 						"url":"null",
	 						"contributors_enabled":"false",
	 						"profile_background_tile":"false",
	 						"profile_banner_url":"https://pbs.twimg.com/profile_banners/2929028424/1472489039",
	 						"statuses_count":11851,
	 						"follow_request_sent":"null",
	 						"followers_count":1020,
	 						"profile_use_background_image":"true",
	 						"default_profile":"true",
	 						"following":"null",
	 						"name":"Happy Tails",
	 						"location":"Narvarte, DF",
	 						"profile_sidebar_fill_color":"DDEEF6","notifications":"null"
	 					}
	 			}
	 		}
	 		]
 	}}"""
	#res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
	#print(res['created'])
	#res = es.get(index="test-index", doc_type='tweet', id=1)
	#print(res['_source'])
	#es.indices.refresh(index="test-index")
	res = es.search(index="test-index", body={"query": {"match": {"text": keyword}}})
	latitude = []
	longitude = []
	text = []
	print("Got %d Hits:" % res['hits']['total'])
	for hit in res['hits']['hits']:
		latitude.append(str(hit['_source']['geo']['coordinates'][0]))
		longitude.append(str(hit['_source']['geo']['coordinates'][1]))
		text.append(str(hit['_source']['text']))
		#print("%(text)s : %(geo)s")
		#print(coordinates)

	return jsonify({'latitude' : latitude, 'longitude' : longitude, 'text' : text})	

@app.route("/")
def main():
	host = ''
	awsauth = AWS4Auth("", "", '', '')

	es = Elasticsearch(
	    hosts=[{'host': host, 'port': 443}],
	    http_auth=awsauth,
	    use_ssl=True,
	    verify_certs=True,
	    connection_class=RequestsHttpConnection
	)

	return render_template('index.html')

if __name__ == "__main__":
	app.run()