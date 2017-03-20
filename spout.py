import sys
import tweepy #API Twitter
import codecs #Text encoder
import requests

#TwitterApp Keys and Access Tokens
consumerKey = 'yUzoUZNozKFzip2Gwgy4w1o44'
consumerSecret = 'k4oWvGnPlCZIcNrmLwvl0OiaurIUQ2EbPrx6IVnlWenvv7hDRM'
accessToken = '832570595917316097-YpWjRdr5CQT4YhLg3rnlaZQMFgXwMoP'
accessSecret = 'PJ8Zbp1oha25NMq24CzypjE1GwCH69T2BnqQlF1xpuCyC'

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
        return True

    def on_timeout(self):
        print 'Timeout...'   
        return True

#Create the autentification
tauth = tweepy.OAuthHandler(consumerKey,consumerSecret)
tauth.set_access_token(accessToken,accessSecret)

spout = spoutModule()
stream = tweepy.Stream(auth = tauth, listener = spout)

stream.filter(track=['BakedPuma'], async=False)
