'''File for retrieving data from RSS feeds of different websites'''
import re
import feedparser

RSS_FILE_NAME = "./Textfiles/RSS.txt"

cve_list = []

def print_rss_file() -> None:
    '''Print data inside RSS-Websites file'''
    with open(RSS_FILE_NAME, "r", encoding="utf-8") as rss_file:
        print(rss_file.read())

def append_website(*website_string) -> bool:
    '''Add website to RSS-Websites file'''
    try:
        with open(RSS_FILE_NAME, "a+", encoding="utf-8") as rss_file:
            for website in website_string:
                rss_file.write(website+"\n")
        return True
    except OSError:
        print(f"Error could not append {website_string} to {RSS_FILE_NAME} file")

def remove_website(*website_string:str):
    """Remove website from RSS-Websites file
    """
    with open(RSS_FILE_NAME, "r", encoding="utf-8") as rss_file:
        lines = rss_file.readlines()

    with open("sample.txt", "w", encoding="utf-8") as rss_file:
        for line in lines:
            if line.strip("\n") != website_string:
                rss_file.write(line)

def get_cve_in_rss(cve_number, cve_array):
    '''Returns CVE REGEX found in an array of tweets'''
    check_cve_regex = re.search('CVE-\\d{4}-\\d{4,7}', cve_number)
        #print(tweets)
    if check_cve_regex is not None:
        cve_array.append(check_cve_regex.group())

def parse_websites():
    '''Parse website(s) in RSS-Websites file'''
    with open(RSS_FILE_NAME, "r", encoding="utf-8") as rss_file:
        cve_array = []
        for line in rss_file.readlines():
            #print(line)
            single_feed = feedparser.parse(line)
            for entry in single_feed.entries:
                get_cve_in_rss(entry.title, cve_array)
                get_cve_in_rss(entry.summary, cve_array)
    return cve_array
