import requests
import json

res = requests.get("http://www.cvedetails.com/json-feed.php?numrows=10&vendor_id=0&product_id=0&version_id=0&hasexp=0&opec=0&opov=0&opcsrf=0&opfileinc=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opginf=0&opdos=0&orderby=3&cvssscoremin=0")
x = json.loads(res.content)
print(x[0])

#keys = dict_keys(['cve_id', 'cwe_id', 'summary', 'cvss_score', 'exploit_count', 'publish_date', 'update_date', 'url'])