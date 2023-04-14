import os
import configparser
import requests
import json

class TwitterLive:

    def __init__(self) -> None:
        '''Initial Setup --> Bearer Token from Twitter Required'''
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(os.path.dirname(os.path.abspath(__file__))+"/Creds.ini")
        self.bear_token = self.config['twitter']['BearerToken']
        
    def bearer_oauth(self, r):
        '''Sets Header for authentication to Twitter API'''
        r.headers["Authorization"] = f"Bearer {self.bear_token}"
        r.headers["User-Agent"] = "v2FilteredStreamPython"
        return r
    
    def get_rules(self):
        '''Rules setup to fetch from a live twitter stream'''
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", auth=self.bearer_oauth
        )
        if response.status_code != 200:
            raise Exception("Error: Cannot get rules (HTTP {}): {}".format(response.status_code, response.text))
        print(json.dumps(response.json()))
        return response.json()


    def delete_all_rules(self, rules):
        '''Removes all Rules to make new --> If rules are not deleted all previous rules are inside the stream'''
        if rules is None or "data" not in rules:
            return None
        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Error: Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        print(json.dumps(response.json()))

    def delete_single_rule(self, rule_id) -> bool:
        payload = {"delete": {"ids": rule_id}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload
        )
        if response.status_code != 200:
            print(f"Either network connection failed or rule_id {rule_id} is not present")
            raise Exception("Error: Cannot delete rule with with if {} (HTTP {}): {}".format(rule_id, response.status_code, response.text))
        return True


    def set_rule(self, new_tweet_hashtag):
        '''Set new rules, all rules will append and be used together (MAX 5 RULES ALLOWED WITHIN STANDARD DEV ACCOUNT)'''
        # You can adjust the rules if needed
        sample_rules = [
            {"value": f"{new_tweet_hashtag}"}
        ]
        payload = {"add": sample_rules}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception("Cannot add rules (HTTP {}): {}".format(response.status_code, response.text))
        print(json.dumps(response.json()))


    def get_stream(self):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream", auth=self.bearer_oauth, stream=True,
        )
        print(response.status_code)
        if response.status_code != 200:
            raise Exception("Cannot get stream (HTTP {}): {}".format(response.status_code, response.text))
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                print(json.dumps(json_response, indent=4, sort_keys=True))

if __name__ == "__main__":

    #This section is only for testing purposes, this tests all functions and tries to make a live stream from tweets
    x = TwitterLive()
    rules = x.get_rules()
    x.delete_all_rules(rules)
    x.set_rule("#cve")
    rules = x.get_rules()

    #Checks if there are rules present if yes than stream can be shown
    if rules is None or "data" not in rules:
        raise Exception("No rules Detected!")
    else:
        x.get_stream()
    