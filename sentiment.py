#app name : Kanika Thapliyal ,  description : sentiment_analysis
#minor project: isme hum monthly data ko database me store krake monthly sentiment analysis bi kr skte hai
                #because ye live data fetch ho rha hai toh hr min chnge hota rhega

import re # regular expression 
import tweepy #access to tweet app
from tweepy import OAuthHandler #authenication 
from textblob import TextBlob #text/tweet parse   dictionary hai jisme hr word ki rating de rkhi hai ki kitna use hua hai
import numpy as np
import matplotlib.pyplot as plt
import pandas
import tkinter as tk
from tkinter import Tk, Button, Label, Entry,Menubutton,Menu

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter application
        consumer_key = '2OHeVtCAyA76yAowyOFwD1Hl6'
        consumer_secret = 'wlYNUhIJXrolJjcqSuVnFBtzVnXhDBi8Ckm6bf0EOXlnn29xOx'
        access_token = '1012548667696267265-yzfdevKNanc5tPoiosFlmW1mqXOl78'
        access_token_secret = 'zq5xn4F4p1CPjSrv9Wa9DHwXDR2NtSv0xiTuB7i723wad'

        # attempt authentication    
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            print('auth.success')
        except:
            print('Error:Authentication Failed')

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())   #ye apne aap bna hota hai baki bna kste hai accordingly ki hume kya chahiye nd kya hatana hai

    
    def get_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        #to check polarity of tweet i.e sentiment
        #print(analysis.sentiment.polarity)

        #twitter aler]ady has a dictionary of different wordsi.e which are negative postive and neutral word 
        #we are using that dictionary of unique word from textblob and indentifying polarity of the text
        #these dictionary takes year to be formed nd keeps on updating
        #thus for any social site having this dictionary we can do the sentiment analysis, like this can be done for facebook , gmail etc
        

        if analysis.sentiment.polarity > 0:    #here we are getting the percentage like 0.06
            return 'positive'                   #for positive it will be > 0 and soo on, all this is pre defined
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            #ciunting the numbr of positive sentiments
            return 'negative'
    
    def get_tweets(self, query, count=10):
        #list of tweets
        
        tweets = []

        try:
            #fetching tweets from twitter, call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)     #q and count are fixed variable in this
            
            #agr bina "tweet.text" k print krvate hai toh kuch smjh nii ayega
            #tweet.text se sirf jo text hai vo ayega 
            #print(fetched_tweets)
            
            for tweet in fetched_tweets:
                #dictionary is created to store text nd uska analysis
                
                parsed_tweet = {}
                parsed_tweet['Leader'] = query
                parsed_tweet['Text'] = tweet.text   #yhan mera jo bhi tweet hai vo store hoo rha h
                parsed_tweet['Sentiment'] = self.get_sentiment(tweet.text)     #yhan uska analysis store hoo rha hai

                #now to make sure that tweets are not repeated
                # appending parsed tweet to tweets list
                if tweet.retweet_count> 0 :      #0 tweets me kya compare krenge so greater than zero
                    # making sure that if tweets have retweets then they are appended only once
                    if parsed_tweet not in tweets:  
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            #returnig the tweets list
            return(tweets)
    
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

#global variables
# lists for counting tweets and storing percentage, globally declared
ptweets=[]    
ntweets=[]
neutweets=[]
leaders=[]     #list of leaders

#now for visualization
def visualization():
    n_groups = 3   #number of bars to be plotted for each leader

    fix , ax = plt.subplots()
    #print(fix)  #gives graph window size 640 X 860
    #print(ax)   #this gives space taken by each graph for leader
    index = np.arange(n_groups)   #this gives a list [0,1,2] for 3 groups
    bar_width = 0.30  #yhan 3 graph aane hai toh 100/3 isse kam he hona chahiye varna overlap krega
    opacity = 0.6

    rects1 = plt.bar(index, ptweets, bar_width,
                    alpha=opacity,
                    color='b',
                    label='positive')

    rects2 = plt.bar(index + bar_width, ntweets, bar_width,
                    alpha=opacity,
                    color='g',
                    label='negative')

    rects3 = plt.bar(index + bar_width+ bar_width, neutweets, bar_width,
                    alpha=opacity,
                    color='r',
                    label='neutral')

    plt.xlabel('Persons')
    plt.ylabel('Sentiments')
    plt.title('Twitter sentiment analysis')
    #plt.xticks(index + bar_width, ('Narendra Modi','Donald Trump','Rahul Gandhi'))
    plt.legend()     #this represents chota box jo uper corner me aata hai nd btata hai ki postive ka kya color hai nd soo on
    plt.tight_layout()
    plt.show()

#enetring leader name in list
def entry():
    l1 = leader1.get()
    l2 = leader2.get()
    l3 = leader3.get()
    leaders.append(l1)
    leaders.append(l2)
    leaders.append(l3)

#object of class
def main():
    api = TwitterClient()   #object of the class twitter
    #calling function to get 200 tweets on donald trump
    tweetlist=[]     #it is 2d list
    #print(leaders)
    for leader in leaders:
        tweets = api.get_tweets(query = leader, count=200)
        tweetlist.append(tweets)
    #print(tweetlist)

    for leader in tweetlist:    #first leader list is accessed
        #print(leader)
        pc,nc,ntc=0,0,0
        for key in leader:    #first dictionary is accessed
            #print(key)
            #print(key['Sentiment'])
            
            if key['Sentiment']=='positive':
                pc = pc+1
            elif key['Sentiment']=='negative':
                nc = nc+1
            else:
                ntc = ntc+1
        #print(len(leader))     #here we are getting count of tweets
        #appending the percentage of sentiment
        ptweets.append((pc*100)/len(leader))
        ntweets.append((nc*100)/len(leader))
        neutweets.append((ntc*100)/len(leader))
    #print(ptweets)
    #print(ntweets)
    #print(neutweets)


#gui, making the project dynamic
root=Tk()
root.title('Twitter Sentiment Analysis')  #title of the window
root.geometry('800x1000') 

#entering the leader
label_no_of_leader = Label(text='Enter the 3 leader name ')
label_no_of_leader.grid(column=0,row=1)
label_leader_name1 = Label(text='First Leader Name')
label_leader_name1.grid(column=0,row=2)
leader1 = Entry()
leader1.grid(column=2,row=2)
label_leader_name2 = Label(text='Second Leader Name')
label_leader_name2.grid(column=0,row=3)
leader2 = Entry()
leader2.grid(column=2,row=3)
label_leader_name3 = Label(text='Third Leader Name')
label_leader_name3.grid(column=0,row=4)
leader3 = Entry()
leader3.grid(column=2,row=4)

enter_button1 = Button(text='Enter:',command= entry)
enter_button1.grid(column=2, row=5)
enter_button2 = Button(text='Result:',command= main)
enter_button2.grid(column=2, row=6)

label_of_grpah = Label(text='Press visualization to show sentiment analysis')
label_of_grpah.grid(column=0,row=7)
graph = Button(text='Visualization:',command= visualization)
graph.grid(column=4,row=9)

bt = Button(text='close',command = exit)
bt.grid(column=2, row=0)

root.mainloop()
