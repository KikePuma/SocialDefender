#! /usr/bin/env python
#This makes possible to run this program as a script invoking the interpreter

#########################
##     HEADER INFO     ##
#########################

__author__ = "Kike Puma"
__copyright__ = "Copyright 2007, CosasDePuma"
__credits__ = ["KikePuma", "CosasDePuma"]
__license__ = "GPL-3.0"
__version__ = "1.0.1 Spout"
__maintainer__ = "KikePuma"
__email__ = "kikefontanlorenzo@gmail.com"
__status__ = "In development"

########################
##       PROGRAM      ##
########################

import sys #System Threading
import tweepy #API Twitter
import codecs #Text encoder

#TwitterApp Keys and Access Tokens
consumerKey = ''
consumerSecret = ''
accessToken = ''
accessSecret = ''

#Extend the class streamListener
class spoutModule(tweepy.StreamListener):
    def on_status(self, status):
        if not hasattr(status, 'retweeted_status'): #Ignore retweets
            print status.text.encode('utf-8') #Encode the text in UTF-8
            
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
