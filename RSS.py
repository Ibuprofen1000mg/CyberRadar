'''File for retrieving data from RSS feeds of different websites'''
import feedparser
import re
from collections import Counter


RSS_FILE_NAME = "./RSS.txt"

class RSSFeed:
    """
    Class to get RSS-Feed(s) from CVE-Website(s) 
    Parsing the RSS-Feed(s) 
    And deliver data to the dashboard
    """

    def __init__(self):
        self.websites = []
        with open(RSS_FILE_NAME, "r", encoding="utf-8") as rss_file:
            for line in rss_file.readlines():
                self.websites += line

    def print_rss_file(self) -> None:
        '''Print data inside RSS-Websites file'''
        with open(RSS_FILE_NAME, "r", encoding="utf-8") as rss_file:
            print(rss_file.read())

    def append_website(self, *website_string) -> bool:
        '''Add website to RSS-Websites file'''
        try:
            with open(RSS_FILE_NAME, "a+", encoding="utf-8") as rss_file:
                for website in website_string:
                    rss_file.write(website+"\n")
            return True
        except OSError:
            print(f"Error could not append {website_string} to {RSS_FILE_NAME} file")

    def remove_website(self, *website_string):
        '''Remove website from RSS-Websites file'''
        with open(RSS_FILE_NAME, "r", encoding="utf-8") as rss_file:
            lines = rss_file.readlines()

        with open("sample.txt", "w", encoding="utf-8") as rss_file:
            for line in lines:
                if line.strip("\n") != website_string:
                    rss_file.write(line)

    def get_cve_in_RSS(self, cve_number, cve_array):
        '''Returns CVE REGEX found in an array of tweets'''
        check_cve_regex = re.search('CVE-\\d{4}-\\d{4,7}', cve_number)
            #print(tweets)
        if check_cve_regex is not None:
            cve_array.append(check_cve_regex.group())
  
  
  
    def parse_websites(self):
        '''Parse website(s) in RSS-Websites file'''
        with open(RSS_FILE_NAME, "r", encoding="utf-8") as rss_file:
            cve_array = []
            for line in rss_file.readlines():
                #print(line)
                single_feed = feedparser.parse(line)
                for entry in single_feed.entries:
#RSS-Feed BSI:
# title,title_detail{.},links{.},link,published,published_parsed,summary,summary_detail{.}
#RSS-Feed Packetstormsec:
# title, title_detail{.},links{.},link,id,guidislink,comments,published,published_parsed,summary,summary_detail{.},tags
                    # print(entry.title)
                    # print(entry.link)
                    # print(entry.published)
                    # print(entry.summary)
                    # print('---------------------')
                    self.get_cve_in_RSS(entry.title, cve_array)
                    self.get_cve_in_RSS(entry.summary, cve_array)
            x = cve_array
            print(list(zip(Counter(x).keys(), Counter(x).values())))

if __name__ == "__main__":
    newRssReader = RSSFeed()
    newRssReader.parse_websites()