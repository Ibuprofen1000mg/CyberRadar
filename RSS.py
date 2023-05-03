'''File for retrieving data from RSS feeds of different websites'''
import feedparser

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

    def parse_websites(self):
        '''Parse website(s) in RSS-Websites file'''
        with open(RSS_FILE_NAME, "r", encoding="utf-8") as rss_file:
            for line in rss_file.readlines():
                #print(line)
                single_feed = feedparser.parse(line)
                for entry in single_feed.entries:
                    '''
                    RSS-Feed BSI: title,title_detail{..},links{..},link,published,published_parsed,summary,summary_detail{..}
                    RSS-Feed Packetstormsec: title, title_detail{..},links{..},link,id,guidislink,comments,published,published_parsed,summary,summary_detail{..},tags
                    '''
                    print(entry.title)
                    print(entry.link)
                    print(entry.published)
                    print(entry.summary)
                    print('---------------------')

if __name__ == "__main__":
    newRssReader = RSSFeed()
    #newRssReader.append_website("https://krebsonsecurity.com/feed/")
    newRssReader.parse_websites()

    #https://dev.to/mr_destructive/feedparser-python-package-for-reading-rss-feeds-5fnc

    #Fetch Websites
    #Add new Websites to a list
    #Remove Websites from list
    #REGEX
    