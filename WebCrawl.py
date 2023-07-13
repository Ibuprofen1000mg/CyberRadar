'''File for retrieving data from RSS feeds of different websites'''
import re
import requests
from bs4 import BeautifulSoup
from collections import Counter


WEBSITES_FILE_NAME = "./Textfiles/Websites.txt"
header = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

cve_array = []

def get_cve_in_Website(string_to_search):
    '''Returns CVE REGEX found in an array of tweets'''
    return re.findall('CVE-\\d{4}-\\d{4,7}', string_to_search)

def parse_websites():
    '''Parse website(s) in RSS-Websites file'''
    with open(WEBSITES_FILE_NAME, "r", encoding="utf-8") as web_file:
        for url in web_file.readlines():
            try:
                x = requests.get(url, headers=header)
                soup = BeautifulSoup(x.content.decode('utf-8'),  "html.parser")
                #print(soup.text)
                #print((soup.text))
                x = (get_cve_in_Website(soup.text.upper()))
                if x:
                    cve_array.extend(x)
            except:
                print(f"Website Error with {url}")
    return cve_array
