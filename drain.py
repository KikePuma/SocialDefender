#! /usr/bin/env python
#This makes possible to run this program as a script invoking the interpreter

#########################
##     HEADER INFO     ##
#########################

__author__ = "Kike Puma"
__copyright__ = "Copyright 2007, CosasDePuma"
__credits__ = ["KikePuma", "CosasDePuma"]
__license__ = "GNU-3.0"
__version__ = "1.0.3 Drain"
__maintainer__ = "KikePuma"
__email__ = "kikefontanlorenzo@gmail.com"
__status__ = "In development"

########################
##       PROGRAM      ##
########################

#Libraries and APIs
import sys  #System Threading
import time #System Threading
import tweepy #API Twitter
import codecs #Text Encoder
import requests #HTTP Requests
import demjson #JSON Decoder
from pymongo import MongoClient #API MongoDB

#TwitterApp Keys and Access Tokens
consumerKey = ''
consumerSecret = ''
accessToken = ''
accessSecret = ''

#MongoDB Connection (MongoLab Used)
uri = 'mongodb://user:pass@host:port/db'
client = MongoClient(uri)
db = client.get_default_database()
collection_name = ''
collection = db[collection_name]

#MeaningCloud Key & Config
meaningCloudKey = ""
meaningCloudLang = "es" #Spanish

#Extend the class streamListener
class spoutModule(tweepy.StreamListener):
    def on_status(self, status):
        if not hasattr(status, 'retweeted_status'): #Ignore retweets
            print "[!] " + status.source.encode('utf-8') + " <> " + status.text.encode('utf-8') #Print the Tweet in UTF-8 Encoding
            print meaningCloudSentiment(status.text.encode('utf-8'),'FEELING')
            #Create Tweet Information in JSON
            tweet = {
                    "feeling": meaningCloudSentiment(status.text.encode('utf-8'),'FEELING'),
                    "tweet":
                    {
                        "text": status.text.encode('utf-8'),
                        "url": "https://twitter.com/" + status.user.screen_name + "/status/" + str(status.id),
                        "user": status.user.name
                    }
                    };
            #Insert the tweet info in the Collection
            collection.insert_one(tweet)


    def on_error(self, status_code):
        if status_code == 420:
            print "[X] Connection refused. Max number of tries. Please wait and try again"
        elif status_code == 401:
            print "[X] Wrong credentials"
        else:
            print "[X] Unknown Error"
        #Return: True dont' stop the program, False stop it
        return False

    def on_timeout(self):
        print '[X] Timeout...'   
        return False

#Define a function that make a HTTP request
def meaningCloudSentiment(tweet,textMode):
    url = "http://api.meaningcloud.com/sentiment-2.1"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = "key=" + meaningCloudKey + "&lang=" + meaningCloudLang + "&txt=" + tweet + "&model="

    response = requests.request("POST", url, data=payload, headers=headers)
    if textMode == 'JSON': #Return the response in RAW format
        return response

    decoded = demjson.decode(response.text) #Decode from JSON to Python
    if textMode == 'ALL': #Return the full response
        return decoded
    #Debugger
    meaningCloudStatus = decoded['status']['code']; #Get the status response code
    if meaningCloudStatus == '104':
        print "[X] You have exceeded the request limit. Waiting 5 seconds ..."
        time.sleep( 5 )
    elif meaningCloudStatus != '0':
        print "[X] MeaningStorm Unknown Error"
        sys.exit(0xBADDEAD)
    if textMode == 'DEBUG':
        return decoded
    #Get the feeling
    feeling = decoded['score_tag']
    if textMode == 'FEELING':
        return feeling

    return "ERROR MODE"

#Catch KeyboardInterrupt (Ctrl + C)
try:
    #Create the authentication
    tauth = tweepy.OAuthHandler(consumerKey,consumerSecret)
    tauth.set_access_token(accessToken,accessSecret)
    #Run the streaming (Sinfonier's Spout)
    spout = spoutModule()
    stream = tweepy.Stream(auth = tauth, listener = spout)
    #Filter the Streaming
    stream.filter(track=['BakedPuma'], async=False)
except KeyboardInterrupt:
    db.drop_collection(collection_name) #Delete the collection
    client.close() #Close the MongoDB connection
    print #Espacio en blanco
    print "\nCreated by KikePuma 2017 (https://github.com/KikePuma)" #Credits
    sys.exit(0xDEAD) #Exit the program
