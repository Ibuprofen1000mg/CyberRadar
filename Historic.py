import requests
from bs4 import BeautifulSoup
import datetime

today = datetime.date.today()
datasets = []
url = "https://www.cvedetails.com/browse-by-date.php"

response = requests.get(url)

soup = BeautifulSoup(response.content.decode('utf-8'),  "html.parser")
data = soup.find_all("td", attrs={"class":"num"})

cve_data = []
for x in data:
    cve_data.append(x.text)
for x in range(1999, today.year+1):
    datasets.append(x)

def dates_array():
    return datasets

def data_array():
    strip_list = [ x.replace('\t', '').replace('\n', '') for x in cve_data ]
    return strip_list
