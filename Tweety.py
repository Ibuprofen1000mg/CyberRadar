import tweepy
import configparser
import os
import pandas as pd
import re

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
         get_tweets_by_x = self.client.search_recent_tweets(
            query=str(query_string),
            tweet_fields=['context_annotations'],
            max_results=int(number_of_tweets)
            )

#Filter Tweets by 
NewTwitter = TwitterCVE()
retrieveLast10 = NewTwitter.get_tweets("#CVE", 100)
list_found_cves_in_tweets = []
for tweets in retrieveLast10.data:
    check_cve_regex = re.search('CVE-\d{4}-\d{4,7}', tweets.text)
    if check_cve_regex != None:
        list_found_cves_in_tweets.append(check_cve_regex.group())


print(list_found_cves_in_tweets)
