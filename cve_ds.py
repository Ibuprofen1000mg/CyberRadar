'''File for CVE DATA SCIENCE'''
import pprint
import time
import requests
import json

URL = "https://cvepremium.circl.lu/api/"
URL2 = "https://api.cvesearch.com/search?q=" #Slower API
URL3 = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=" #Faster API

headers = {'Accept': 'application/json'}

s = requests.Session()

# author: Benjamin Götz?
def get_vendors():
    '''Returns all vendors stored in the databases'''

    request = requests.get(URL + "browse", timeout=50).json()
    pprint.pprint(request.keys())
    print(type(request)) #Dict
    print(request.get('vendor')[10]) #List

def get_products_per_vendor():
    '''Get all the products associated to a vendor with known CVEs'''

    vendor = input("For which VENDOR do you want to know the products?")
    request = requests.get(URL + "browse/" + vendor, timeout=50).json()
    pprint.pprint(request)

def get_vulnerabilities_per_product():
    '''Get all the vulnerabilities associated to a certain vendor and a certain product'''

    vendor = input("Which VENDOR?").lower()
    product = input("Which PRODUCT?").lower()
    request = requests.get(URL + "search/" + vendor + "/" + product, timeout=5).json()
    pprint.pprint(request)

def get_cve_severity_and_score(cvenumber):
    '''Return the severity and the cvss of a CVE'''
    request = requests.get(URL + "cve/" + cvenumber, timeout=50).json()
    return request["typical_severity"], request["cvss3"]

# def get_nested(data, *args):
#     if args and data:
#         element  = args[0]
#         if element:
#             value = data.get(element)
#             return value if len(args) == 1 else get_nested(value, *args[1:])

def get_cve_info(cve):
    '''
    Return the severity and the cvss of a CVE from NIST API
    
    :param str cve: The CVE which shall be queried
    :return: basic and details information of the CVE
    :rtype: tuple
    '''
    try:
        request = s.get(URL3 + cve, timeout=40, headers=headers).json()
        cvss30 = request["vulnerabilities"][0]['cve']['metrics'].get('cvssMetricV30')
        #print(cvss30)
        cvss31 = request["vulnerabilities"][0]['cve']['metrics'].get('cvssMetricV31')
        #print(cvss31)
    except IndexError or json.decoder.JSONDecodeError or requests.exceptions.JSONDecodeError:
        cvss30 = None
        cvss31 = None

    if cvss30 is not None:
        score = cvss30[0]['cvssData'].get('baseScore')
        severity = cvss30[0]['cvssData'].get('baseSeverity')
    elif cvss31 is not None:
        score = cvss31[0]['cvssData'].get('baseScore')
        severity = cvss31[0]['cvssData'].get('baseSeverity')
    else:
        score = 0
        severity = "N/A"

    print(score, severity)
    return score, severity

def get_cve_info2(cve):
    '''
    Return the severity and the cvss of a CVE from CVEDetails API
    
    :param str cve: The CVE which shall be queried
    :return: basic and details information of the CVE
    :rtype: tuple
    '''
    cve = cve.lower()
    print(cve)
    time.sleep(1)
    try:
        request = s.get(URL2 + cve, timeout=40).json()

        details = request["response"][cve].get('details')
        score = request["response"][cve]['details'].get('cvssV3_score')
        severity = request["response"][cve]['details'].get('confidence')

        if details is not None:
            score = details.get('cvssV3_score')
            severity = details.get('confidence')
        else:
            score = 0
            severity = "N/A"

    except KeyError:
        score = 0
        severity = "N/A"

    print(score, severity)
    return score, severity

def db_info():
    '''Get infos about the used databases of the API'''

    request = requests.get(URL + 'dbinfo', timeout=50).json()
    pprint.pprint(request)

def latest_30_cves():
    '''Print newest 30 CVEs which were uploaded to the DBs'''

    request = requests.get(URL + 'last', timeout=50).json()
    pprint.pprint(request)
    for vul in request:
        print(vul.get('id'))
        print(vul.get('summary'))
        print(vul.keys())

#Only Debugging Purpose
#get_cve_info2("CVE-2022-23808")
