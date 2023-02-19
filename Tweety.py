import tweepy
import configparser
import os
import pandas as pd
import re
import numpy as np
from collections import Counter

class TwitterCVE:

    def __init__(self) -> None:
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(os.path.dirname(os.path.abspath(__file__))+"/TwitterCreds.ini")
        self.api_key = self.config['twitter']['ApiKey']
        self.api_key_secret = self.config['twitter']['ApiKeySecret']
        self.access_token = self.config['twitter']['AccessToken']
        self.access_token_secret = self.config['twitter']['AccessTokenSecret']
        self.bear_token = self.config['twitter']['BearerToken']
        self.client = tweepy.Client(
            bearer_token=self.bear_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_key_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )
        self.auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

    #Get Last X Tweets with filered Search
    def get_tweets(self, query_string, number_of_tweets) -> list:
        get_tweets_by_x = self.client.search_recent_tweets(
            query=str(query_string),
            tweet_fields=['context_annotations'],
            max_results=int(number_of_tweets)
            )
        return get_tweets_by_x

    def get_new_twitter_accounts(self, query_string, number_of_tweets) -> list:
        get_username_by_tweet = self.client.search_recent_tweets(
            query=str(query_string),
            max_results=int(number_of_tweets),          
            expansions = 'author_id',
            user_fields = ['username'],
            )
        new_username_list = []
        for x in range(0, number_of_tweets-1):
            print(get_username_by_tweet.includes['users'][x])
            new_username_list[x] = get_username_by_tweet.includes['users'][x]    
            print(new_username_list[x])
        return new_username_list

    def get_cve_in_tweets(self, tweets_response):
        list_found_cves_in_tweets = []
        for tweets in tweets_response.data:
            check_cve_regex = re.search('CVE-\d{4}-\d{4,7}', tweets.text)
            print(tweets[0])
            if check_cve_regex != None:
                list_found_cves_in_tweets.append(check_cve_regex.group())
        return list_found_cves_in_tweets

    #Sort collected tweets by frequency
    def sort_tweets_by_cve_frequency(self, list_of_cve):
        print(Counter(list_of_cve).keys()) # equals to list(set(words))
        print(Counter(list_of_cve).values()) # counts the elements' frequency


#Filter Tweets by 
# NewTwitter = TwitterCVE()
# retrieveLast10 = NewTwitter.get_new_twitter_accounts("#CVE", 10)
# list_found_cves_in_tweets = []
# for tweets in retrieveLast10.data:
#     check_cve_regex = re.search('CVE-\d{4}-\d{4,7}', tweets.text)
#     print(tweets[0])
#     if check_cve_regex != None:
#         list_found_cves_in_tweets.append(check_cve_regex.group())




##THis prints a twitter user list with cve referenced in their tweets
NewTwitter = TwitterCVE()
#x = NewTwitter.get_tweets("#CVE", 10)
#print(x)
retrieveLast10 = NewTwitter.get_tweets("#CVE", 100)
list_found_cves_in_tweets = []
for tweets in retrieveLast10.data:
    check_cve_regex = re.search('CVE-\d{4}-\d{4,7}', tweets.text)
    #print(tweets[0])
    if check_cve_regex != None:
        list_found_cves_in_tweets.append(check_cve_regex.group())

y = NewTwitter.sort_tweets_by_cve_frequency(list_found_cves_in_tweets)

#print(NewTwitter.get_cve_in_tweets(x))
#print(x.includes['users'][0])
#for z in x.includes['users']:
#    print(z)

#print(list_found_cves_in_tweets)
