"""This File contains elements and functions to connect to the Reddit API and retrieve Data\n
__Author__: Nic Holzapfel\n
"""
#########Imports#########
import configparser
import os
import re
from collections import Counter
import praw
##########################

config = configparser.ConfigParser(interpolation=None)
config.read(os.path.dirname(os.path.abspath(__file__))+"/Configuration/Creds.ini")
own_script = config['reddit']['OwnScript']
secret = config['reddit']['Secret']
client = praw.Reddit(
    client_id=own_script,
    client_secret=secret,
    user_agent="android:com.example.cyberradar:v1.2.3"
)

def check_api_function() -> str:
    """Function to check if API Access with Tokens are working

    Returns:
        str: Returns string regarding user information from the API
    """
    return client.read_only

def check_last_new_in_subreddit(subreddit_name:str, amount_of_posts:int) -> str:
    """Checks the latest posts from a given subreddit

    Args:
        subreddit_name (str): name of subreddit (e.g. homelab)
        amount_of_posts (int): the amount of latests posts

    Returns:
        str: Latests found posts from subreddits
    """
    return client.subreddit(subreddit_name).new(limit=amount_of_posts)

def get_cve_in_reddit(reddit_response:str, global_cve_list:list)->list:
    """Returns CVE REGEX found in an array of reddits

    Args:
        reddit_response (str): Input string to check for the CVE-Regex Pattern
        global_cve_list (list): Global list to append the found patterns to

    Returns:
        list: All found CVEs
    """
    check_cve_regex = re.search('CVE-\\d{4}-\\d{4,7}', reddit_response, re.IGNORECASE)
    if check_cve_regex is not None:
        global_cve_list.append(check_cve_regex.group().upper())
    return global_cve_list

def retrieve_reddit_cve_list() -> list:
    """Loops through all subreddits to retrieve latests posts from Reddit

    Returns:
        list: List of all found CVEs
    """
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

def retrieve_cve_count(cve_string:list) -> str:
    """Check how often each CVE is named inside the a list

    Args:
        cve_string (list): Input list of all CVEs 

    Returns:
        str: amount of each CVE
    """
    try:
        return Counter(retrieve_reddit_cve_list())[cve_string]
    except TypeError:
        print(f"{cve_string} not found or problem finding string!")
