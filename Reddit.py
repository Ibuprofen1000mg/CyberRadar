"""MISSING!!!"""
import configparser
import os
import re
#This is the reddit api python wrapper
from collections import Counter
import praw


class RedditCVE:
    """MISSING!!!"""
    #Configure initials for reddit class --> Credential Data for Access
    def __init__(self) -> None:
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(os.path.dirname(os.path.abspath(__file__))+"/Creds.ini")
        self.own_script = self.config['reddit']['OwnScript']
        self.secret = self.config['reddit']['Secret']
        self.client = praw.Reddit(
            client_id=self.own_script,
            client_secret=self.secret,
            user_agent="CVEFinder"
        )
        print(self.client.read_only)

    #Function to check if API Access with Tokens is working
    def check_api_function(self) -> None:
        """MISSING!!!"""
        return self.client.read_only

    def check_last_new_in_subreddit(self, subreddit_name, amount_of_posts):
        """MISSING!!!"""
        return self.client.subreddit(subreddit_name).new(limit=amount_of_posts)

    def get_cve_in_reddit(self, reddit_response, global_cve_list)->list:
        '''Returns CVE REGEX found in an array of reddits'''
        check_cve_regex = re.search('CVE-\\d{4}-\\d{4,7}', reddit_response, re.IGNORECASE)
        if check_cve_regex is not None:
            global_cve_list.append(check_cve_regex.group().upper())
        return global_cve_list

    def retrieve_reddit_cve_list(self) -> list:
        """MISSING!!!"""
        cve_list = []
        try:
            with open("Subreddits.txt", "r", encoding="utf-8") as reddit_file:
                for line in reddit_file.readlines():
                    reddit_string_tuple = self.check_last_new_in_subreddit(line, 20)
                    for text_values in reddit_string_tuple:
                        self.get_cve_in_reddit(text_values.title,cve_list)
                        self.get_cve_in_reddit(text_values.selftext,cve_list)
            return cve_list
        except FileNotFoundError:
            print("File Error!")

    def retrieve_cve_count(self, cve_string):
        """MISSING!!!"""
        try:
            return Counter(self.retrieve_reddit_cve_list())[cve_string]
        except TypeError:
            print(f"{cve_string} not found or problem finding string!")

#print(RedditCVE().retrieve_cve_count('CVE-2023-2033'))
#if __name__ == "__main__":
#    p = RedditCVE().retrieve_reddit_cve_list()
#    print(list(Counter(p).keys()))
#    print(list(Counter(p).values()))

# print(Counter(p).keys())
# print(Counter(p).values())

# with open("Subreddits.txt", "r") as reddit_file:
#     for line in reddit_file.readlines():
#         reddit_string_tuple = x.check_last_new_in_subreddit(line, 10)
#         for text_values in reddit_string_tuple:
#             x.get_cve_in_reddit(text_values.title,cve_list)
#             #print((text_values.title))
