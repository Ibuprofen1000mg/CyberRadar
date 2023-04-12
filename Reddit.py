import configparser
import os
#This is the reddit api python wrapper
import praw

class RedditCVE:

    #Configure initials for reddit class --> Credential Data for Access
    def __init__(self) -> None:
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(os.path.dirname(os.path.abspath(__file__))+"/Creds.ini")
        self.own_script = self.config['reddit']['OwnScript']
        self.secret = self.config['reddit']['Secret']
        self.client = praw.Reddit(
            client_id=self.own_script,
            client_secret=self.secret,
            user_agent="CVEFiner"
        )
        print(self.client.read_only)

    #Function to check if API Access with Tokens is working
    def check_api_function(self) -> None:
        return self.client.read_only
    
    def check_last_hot_in_subreddit(self, subreddit_name, amount_of_posts):
        for submission in self.client.subreddit(subreddit_name).hot(limit=amount_of_posts):
            print(submission.selftext)
            #pprint.pprint(vars(submission))
            #print("\n")
    
x = RedditCVE()
x.check_last_hot_in_subreddit('homelab', 1)