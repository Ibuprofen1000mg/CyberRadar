'''File for retrieving data from RSS feeds of different websites'''
import re
import requests
from bs4 import BeautifulSoup
from collections import Counter


WEBSITES_FILE_NAME = "./Websites.txt"
header = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
class WebFeed:
    """
    Class to get RSS-Feed(s) from CVE-Website(s) 
    Parsing the RSS-Feed(s) 
    And deliver data to the dashboard
    """
    def __init__(self) -> None:
        self.cve_array = []

    def get_cve_in_Website(self, string_to_search):
        '''Returns CVE REGEX found in an array of tweets'''
        return re.findall('CVE-\\d{4}-\\d{4,7}', string_to_search)
  
    def parse_websites(self):
        '''Parse website(s) in RSS-Websites file'''
        with open(WEBSITES_FILE_NAME, "r", encoding="utf-8") as web_file:
            for url in web_file.readlines():
                try:
                    x = requests.get(url, headers=header)
                    soup = BeautifulSoup(x.content.decode('utf-8'),  "html.parser")
                    #print(soup.text)
                    #print((soup.text))
                    x = (self.get_cve_in_Website(soup.text.upper()))
                    if x:
                        self.cve_array.extend(x)
                except:
                    print(f"Website Error with {url}")
        x = (self.cve_array)
        print(Counter(x).keys())
        print( Counter(x).values())

if __name__ == "__main__":
    newWebFeed = WebFeed()
    newWebFeed.parse_websites()