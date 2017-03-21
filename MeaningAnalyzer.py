#! /usr/bin/env python
# encoding=utf8
#This makes possible to run this program as a script invoking the interpreter

#########################
##     HEADER INFO     ##
#########################

__author__ = "Kike Puma"
__copyright__ = "Copyright 2007, CosasDePuma"
__credits__ = ["KikePuma", "CosasDePuma"]
__license__ = "GNU-3.0"
__version__ = "1.0.4 Args"
__maintainer__ = "KikePuma"
__email__ = "kikefontanlorenzo@gmail.com"
__status__ = "In development"

########################
##       COLORS       ##
########################

#Color change: "\033[cod_formato;cod_texto;cod_fondom"
ERROR = "\n\033[1;31m" #BOLD RED
POSITIVE = "\033[1;32m" #GREEN
NEUTRAL = "\033[1;37m" #WHITE
NEGATIVE = "\033[1;31m" #RED
DEFAULT = "\033[0m" #DEFAULT COLOR
CREDITS = "\033[2;37m" #LIGHT WHITE

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
import argparse #Argument Parser
from pymongo import MongoClient #API MongoDB

#Set default encoding UTF-8
reload(sys)
sys.setdefaultencoding('utf8')

#TwitterApp Keys and Access Tokens
consumerKey = ''
consumerSecret = ''
accessToken = ''
accessSecret = ''

#MongoDB Connection (MongoLab Used)
uri = 'mongodb://user:password@host:port/db'
client = MongoClient(uri)
db = client.get_default_database()
collection_name = 'feelings'
collection = db[collection_name]

#MeaningCloud Key & Config
meaningCloudKey = ""
meaningCloudLang = "es" #Spanish

#Argument Parser
parser = argparse.ArgumentParser()
parser.add_argument("-C", "--colored", help="color according to the feelings", action="store_true")
parser.add_argument("-F", "--feelings", help="show the feeling polarity in the text", action="store_true")
parser.add_argument("-I", "--irony", help="indicates the irony of the text", action="store_true")
args = parser.parse_args()

#Extend the class streamListener
class spoutModule(tweepy.StreamListener):
    def on_status(self, status):
        if not hasattr(status, 'retweeted_status'): #Ignore retweets
            meaning = meaningCloud(status.text.encode('utf-8'),'DEBUG') #Meaning Procesing
            consoleLine =  status.user.name + " (@" + status.user.screen_name + ") <> " + status.text.encode('utf-8') + DEFAULT
            data = ""
            #MEANING ARGS
            if args.irony:
		data += "[" + meaning['irony'] + "]"
            if args.feelings:
                data = "[" + meaning['score_tag'] + "]" + data
            #SET THE DATA
            if data != "":
                consoleLine = data + " " + consoleLine
            #COLOR ARGS
            if args.colored:
                if meaning['score_tag'] == "P+" or meaning['score_tag'] == "P":
                    consoleLine = POSITIVE + consoleLine #Print the tweet in White
                elif meaning['score_tag'] == "NEU" or meaning['score_tag'] == "NONE":
                    consoleLine = NEUTRAL + consoleLine #Print the Tweet in White
                elif meaning['score_tag'] == "N" or meaning['score_tag'] == "N+":
                    consoleLine = NEGATIVE + consoleLine #Print the Tweet in Red
            else:
                consoleLine = DEFAULT + consoleLine #Print the tweet in UTF-8
            print consoleLine
            #Create Tweet Information in JSON
            tweet = {
                    "feeling": meaning['score_tag'],
                    "irony": meaning['irony'],
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
            print ERROR + "[ERROR] Connection refused. Max number of tries. Please wait and try again" + DEFAULT
        elif status_code == 401:
            print ERROR + "[ERROR] Wrong credentials" + DEFAULT
        else:
            print ERROR + "[ERROR] Unknown Error" + DEFAULT
        #Return: True dont' stop the program, False stop it
        return False

    def on_timeout(self):
        print ERROR + '[X] Timeout...' + DEFAULT
        return False

#Define a function that make a HTTP request
def meaningCloud(tweet,textMode):
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
        print ERROR + "[X] You have exceeded the request limit. Waiting 5 seconds ..." + DEFAULT
        time.sleep( 5 )
    elif meaningCloudStatus != '0':
        print ERROR + "[X] MeaningStorm Unknown Error" + DEFAULT
        sys.exit(0xBADDEAD)
    if textMode == 'DEBUG':
        return decoded
    #Get the feeling
    if textMode == 'FEELING':
        response = decoded['score_tag']
    #Get the irony
    elif textMode == 'IRONY':
        response = decoded['irony']
    else:
        return "[X] ERROR"
    return response

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
    print CREDITS + "\nCreated by KikePuma 2017 (https://github.com/KikePuma)" + DEFAULT #Credits
    sys.exit(0xDEAD) #Exit the program
