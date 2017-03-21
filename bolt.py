#! /usr/bin/env python
#This makes possible to run this program as a script invoking the interpreter

#########################
##     HEADER INFO     ##
#########################

__author__ = "Kike Puma"
__copyright__ = "Copyright 2007, CosasDePuma"
__credits__ = ["KikePuma", "CosasDePuma"]
__license__ = "GPL-3.0"
__version__ = "1.0.2 Bolt"
__maintainer__ = "KikePuma"
__email__ = "kikefontanlorenzo@gmail.com"
__status__ = "In development"

########################
##       PROGRAM      ##
########################

#Libraries and APIs
import sys #System Threading
import tweepy #API Twitter
import codecs #Text Encoder
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

#Extend the class streamListener
class spoutModule(tweepy.StreamListener):
    def on_status(self, status):
        if not hasattr(status, 'retweeted_status'): #Ignore retweets
            print "[!] " + status.source.encode('utf-8') + " <> " + status.text.encode('utf-8') #Print the Tweet in UTF-8 Encoding
            #Create Tweet Information in JSON
            tweet = {
                    "feeling": "",
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
            print "Connection refused. Max number of tries. Please wait and try again"
        elif status_code == 401:
            print "Wrong credentials"
        else:
            print "Ocurrio un error"
        #Return: True dont' stop the program, False stop it
        return False

    def on_timeout(self):
        print 'Timeout...'   
        return True

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
