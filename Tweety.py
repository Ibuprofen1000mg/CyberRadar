"""This File contains neccessary elements and functions to connect to the Twitter API and retireve Data
__author__: Nic Holzapfel
"""
#########Imports#########
import configparser
import os
import re
import tweepy
#########################

class TwitterCVE:
    """This class generates a client to connect to the Twitter API. By connecting to the API, a user can fetch data from twitter feeds for further analysis
    """
    def __init__(self) -> None:
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(os.path.dirname(os.path.abspath(__file__))+"/Configuration/Creds.ini")
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

    def get_tweets(self, query_string: str, number_of_tweets: int) -> list:
        """Returns Tweets given a number of tweets and a query-string

        Args:
            query_string (str): The query-string for tweets to be searched
            number_of_tweets (int): The amount of tweets to be returned

        Returns:
            list: Found amount of tweets based on the requested query
        """
        try:
            get_tweets_by_x = self.client.search_recent_tweets(
                query=str(query_string),
                tweet_fields=['context_annotations'],
                max_results=int(number_of_tweets)
                )
            return get_tweets_by_x
        except:
            print("Twitter API Error/Faulty Credentials: Using Textfile Data")
        
    def get_cve_in_tweets(self, tweets_response)->list:
        """Returns CVE REGEX found in an array of tweets

        Args:
            tweets_response (_type_): Enter the Tweet Queries to be searched for a CVE Regex Pattern

        Returns:
            list: Found CVEs inside the Tweets
        """
        list_found_cves_in_tweets = []
        for tweets in tweets_response.data:
            check_cve_regex = re.search('CVE-\\d{4}-\\d{4,7}', tweets.text)
            #print(tweets)
            if check_cve_regex is not None:
                list_found_cves_in_tweets.append(check_cve_regex.group())
        return list_found_cves_in_tweets

