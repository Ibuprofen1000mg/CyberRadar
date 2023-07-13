"""File for retrieving data from RSS feeds of different websites"""
import re
import requests
from bs4 import BeautifulSoup

WEBSITES_FILE_NAME = "./Textfiles/Websites.txt"
header = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
cve_array = []

def get_cve_in_website(string_to_search:str) -> list:
    """Returns CVE REGEX found in an array of tweets

    Args:
        string_to_search (str): String to search for CVE Regex Pattern

    Returns:
        _type_: List containing found CVE given a string
    """
    return re.findall('CVE-\\d{4}-\\d{4,7}', string_to_search)

def parse_websites() -> list:
    """Parse website(s) in RSS-Websites file

    Returns:
        list: List containing all CVE Patterns from a list of Strings
    """
    with open(WEBSITES_FILE_NAME, "r", encoding="utf-8") as web_file:
        for url in web_file.readlines():
            try:
                download_website = requests.get(url, headers=header, timeout=5)
                soup = BeautifulSoup(download_website.content.decode('utf-8'),  "html.parser")
                download_website = (get_cve_in_website(soup.text.upper()))
                if download_website:
                    cve_array.extend(download_website)
            except:
                print(f"Website Error with {url}")
    return cve_array
