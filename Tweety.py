"""This File contains elements and functions to connect to the Twitter API and retrieve Data
__author__: Nic Holzapfel
"""
#########Imports#########
import configparser
import os
import re
import tweepy
#########################

config = configparser.ConfigParser(interpolation=None)
config.read(os.path.dirname(os.path.abspath(__file__))+"/Configuration/Creds.ini")
api_key = config['twitter']['ApiKey']
api_key_secret = config['twitter']['ApiKeySecret']
access_token = config['twitter']['AccessToken']
access_token_secret = config['twitter']['AccessTokenSecret']
bear_token = config['twitter']['BearerToken']
client = tweepy.Client(
    bearer_token=bear_token,
    consumer_key=api_key,
    consumer_secret=api_key_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

def get_tweets(query_string: str, number_of_tweets: int) -> list:
    """Returns Tweets given a number of tweets and a query-string

    Args:
        query_string (str): The query-string for tweets to be searched
        number_of_tweets (int): The amount of tweets to be returned

    Returns:
        list: Found amount of tweets based on the requested query
    """
    try:
        get_tweets_by_x = client.search_recent_tweets(
            query=str(query_string),
            tweet_fields=['context_annotations'],
            max_results=int(number_of_tweets)
            )
        return get_tweets_by_x
    except:
        print("Twitter API Error/Faulty Credentials: Using Textfile Data")

def get_cve_in_tweets(tweets_response)->list:
    """Returns CVE REGEX found in an array of tweets

    Args:
        tweets_response (_type_): Enter the Tweet Queries to be searched for a CVE Regex Pattern

    Returns:
        list: Found CVEs inside the Tweets
    """
    list_found_cves_in_tweets = []
    for tweets in tweets_response.data:
        check_cve_regex = re.search('CVE-\\d{4}-\\d{4,7}', tweets.text)
        if check_cve_regex is not None:
            list_found_cves_in_tweets.append(check_cve_regex.group())
    return list_found_cves_in_tweets
