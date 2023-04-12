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
        self.config.read(os.path.dirname(os.path.abspath(__file__))+"/Creds.ini")
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
        '''Returns Tweets given a number of tweets and a query-string'''
        get_tweets_by_x = self.client.search_recent_tweets(
            query=str(query_string),
            tweet_fields=['context_annotations'],
            max_results=int(number_of_tweets)
            )
        return get_tweets_by_x

    def get_new_twitter_accounts(self, query_string, number_of_tweets) -> list:
        '''Returns Tweet-authors given a number of tweets and a query-string'''
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

    def get_cve_in_tweets(self, tweets_response)->list:
        '''Returns CVE REGEX found in an array of tweets'''
        list_found_cves_in_tweets = []
        for tweets in tweets_response.data:
            check_cve_regex = re.search('CVE-\d{4}-\d{4,7}', tweets.text)
            #print(tweets)
            if check_cve_regex != None:
                list_found_cves_in_tweets.append(check_cve_regex.group())
        return list_found_cves_in_tweets

    #Sort collected tweets by frequency
    def sort_tweets_by_cve_frequency(self, list_of_cve):
        '''Sorts the number of cves to their frequency'''
        Counter(list_of_cve).keys() # equals to list(set(words))
        Counter(list_of_cve).values() # counts the elements' frequency



NewTwitter = TwitterCVE()
retrieveLast10 = NewTwitter.get_tweets("#CVE", 100)
z = NewTwitter.get_cve_in_tweets(retrieveLast10)
y = NewTwitter.sort_tweets_by_cve_frequency(z)

