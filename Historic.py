"""File for the generation of the historic CVE data"""
import datetime
import requests
from bs4 import BeautifulSoup


today = datetime.date.today()
datasets = []
URL = "https://www.cvedetails.com/browse-by-date.php"

response = requests.get(URL)

soup = BeautifulSoup(response.content.decode('utf-8'),  "html.parser")
data = soup.find_all("td", attrs={"class":"num"})

cve_data = []
for x in data:
    cve_data.append(x.text)
for x in range(1999, today.year+1):
    datasets.append(x)

def dates_array() -> list:
    """Returns a list containing Years from 1999 until today

    Returns:
        list: List containing years
    """
    return datasets

def data_array():
    """_summary_

    Returns:
        _type_: _description_
    """
    strip_list = [ x.replace('\t', '').replace('\n', '') for x in cve_data ]
    return strip_list
