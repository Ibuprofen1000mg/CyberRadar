'''File for retrieving data from RSS feeds of different websites'''
import requests
import feedparser

RSS_FILE_NAME = "./RSS.txt"

class RSSCVE:
    
    def __init__(self):
        self.websites = []
        with open(RSS_FILE_NAME, "r") as rssfile:
            for line in rssfile.readlines():
                self.websites += line

    def print_rssfile(self) -> None:
        with open(RSS_FILE_NAME, "r") as rssfile:
            print(rssfile.read())

    def append_website(self, *website_string) -> bool:
        try:
            with open(RSS_FILE_NAME, "a+") as rssfile:
                for website in website_string:
                    rssfile.write(website+"\n")
            return True
        except:
            raise Exception("Error could not append {} to {} file".format(website_string, RSS_FILE_NAME))   
                
    def remove_website(self, *website_string):
        with open(RSS_FILE_NAME, "r") as rssFile:
            lines = rssFile.readlines()

        with open("sample.txt", "w") as rssFile:
            for line in lines:
                if line.strip("\n") != website_string:
                    rssFile.write(line)

    def parse_websites(self):
        with open(RSS_FILE_NAME, "r") as rssFile:
            for line in rssFile.readlines():
                #print(line)
                single_feed = feedparser.parse(line)
                for entry in single_feed.entries:
                    print(entry.title)          

if __name__ == "__main__":
    newRssReader = RSSCVE()
    newRssReader.append_website('http://www.cvedetails.com/widget.php?numrows=10&vendor_id=0&product_id=0&version_id=0&hasexp=1&opec=1&opov=1&opcsrf=1&opfileinc=1&opgpriv=1&opsqli=1&opxss=1&opdirt=1&opmemc=1&ophttprs=1&opbyp=1&opginf=1&opdos=1&orderby=3&cvssscoremin=0')   
    newRssReader.parse_websites()

    #https://dev.to/mr_destructive/feedparser-python-package-for-reading-rss-feeds-5fnc

    #Fetch Websites
    #Add new Websites to a list
    #Remove Websites from list
    #REGEX
    