    """_summary_

    Returns:
        _type_: _description_
    """
import configparser
import os
import re
#This is the reddit api python wrapper
from collections import Counter
import praw
from prawcore.exceptions import Forbidden

# author: Nic Holzapfel ?

config = configparser.ConfigParser(interpolation=None)
config.read(os.path.dirname(os.path.abspath(__file__))+"/Configuration/Creds.ini")
own_script = config['reddit']['OwnScript']
secret = config['reddit']['Secret']
client = praw.Reddit(
    client_id=own_script,
    client_secret=secret,
    user_agent="android:com.example.cyberradar:v1.2.3"
    )

#Function to check if API Access with Tokens is working
def check_api_function() -> None:
    """MISSING!!!"""
    return client.read_only

def check_last_new_in_subreddit(subreddit_name, amount_of_posts):
    """MISSING!!!"""
    return client.subreddit(subreddit_name).new(limit=amount_of_posts)

def get_cve_in_reddit(reddit_response, global_cve_list)->list:
    '''Returns CVE REGEX found in an array of reddits'''
    check_cve_regex = re.search('CVE-\\d{4}-\\d{4,7}', reddit_response, re.IGNORECASE)
    if check_cve_regex is not None:
        global_cve_list.append(check_cve_regex.group().upper())
    return global_cve_list

def retrieve_reddit_cve_list() -> list:
    """MISSING!!!"""
    cve_list = []
    try:
        with open("Textfiles/Subreddits.txt", "r", encoding="utf-8") as reddit_file:
            for line in reddit_file.readlines():
                reddit_string_tuple = check_last_new_in_subreddit(line, 5)
                for text_values in reddit_string_tuple:
                    get_cve_in_reddit(text_values.title,cve_list)
                    get_cve_in_reddit(text_values.text,cve_list)
        return cve_list
    except FileNotFoundError:
        print("File Error!")

def retrieve_cve_count(cve_string):
    """MISSING!!!"""
    try:
        return Counter(retrieve_reddit_cve_list())[cve_string]
    except TypeError:
        print(f"{cve_string} not found or problem finding string!")
