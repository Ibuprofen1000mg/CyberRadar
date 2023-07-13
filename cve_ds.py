# Author: Benjamin Götz
'''File for CVE DATA SCIENCE'''
import pprint
import requests

URL = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=" #Faster API
URL2 = "https://api.cvesearch.com/search?q=" #Slower API
URL3 = "https://cvepremium.circl.lu/api/"

headers = {'Accept': 'application/json'}

s = requests.Session()

def get_cve_info(cve):
    '''
    Return the severity and the cvss of a CVE from NIST API
    
    :param str cve: The CVE which shall be queried
    :return: basic and details information of the CVE
    :rtype: tuple
    '''
    try:
        request = s.get(URL + cve, timeout=40, headers=headers).json()

        cvss30 = request["vulnerabilities"][0]['cve']['metrics'].get('cvssMetricV30')
        cvss31 = request["vulnerabilities"][0]['cve']['metrics'].get('cvssMetricV31')
        description = request["vulnerabilities"][0]['cve']['descriptions'][0].get('value')
        last_modified = request["vulnerabilities"][0]['cve'].get('lastModified')

    except requests.exceptions.JSONDecodeError:
        cvss30 = None
        cvss31 = None
        description = None
        last_modified = None

    if cvss30 is not None:
        score = cvss30[0]['cvssData'].get('baseScore')
        severity = cvss30[0]['cvssData'].get('baseSeverity')
    elif cvss31 is not None:
        score = cvss31[0]['cvssData'].get('baseScore')
        severity = cvss31[0]['cvssData'].get('baseSeverity')
    else:
        score = 0
        severity = "N/A"

    return score, severity, description, last_modified

def get_cve_info2(cve):
    '''
    Return the severity and the cvss of a CVE from CVEDetails API
    
    :param str cve: The CVE which shall be queried
    :return: basic and details information of the CVE
    :rtype: tuple
    '''
    cve = cve.lower()

    try:
        request = s.get(URL2 + cve, timeout=40).json()

        score = request["response"][cve]['details'].get('cvssV3_score')
        severity = request["response"][cve]['details'].get('severity')
        description = request["response"][cve]['basic'].get('description')
        last_modified = request["response"][cve]['basic'].get('date_modified')

    except requests.exceptions.JSONDecodeError:
        score = None
        severity = None
        description = None
        last_modified = None

    return score, severity, description, last_modified

def get_cve_info3(cve:str):
    """_summary_

    Args:
        cve (str): _description_

    Returns:
        _type_: _description_
    """
    cve = cve.lower()

    try:
        request = s.get(URL3 + "cve/" + cve, timeout=40).json()

        score = request.get("cvss3")
        severity = request["access"].get("complexity")
        description = request.get("summary")
        last_modified = request.get("last-modified")

    except requests.exceptions.JSONDecodeError:
        score = None
        severity = None
        description = None
        last_modified = None

    return score, severity, description, last_modified


### Functions for potential further development
def get_vendors():
    '''Returns all vendors stored in the databases'''

    request = requests.get(URL3 + "browse", timeout=50).json()
    pprint.pprint(request.keys())
    print(type(request)) #Dict
    print(request.get('vendor')[10]) #List

def get_products_per_vendor():
    """Get all the products associated to a vendor with known CVEs"""

    vendor = input("For which VENDOR do you want to know the products?")
    request = requests.get(URL3 + "browse/" + vendor, timeout=50).json()
    pprint.pprint(request)

def get_vulnerabilities_per_product():
    '''Get all the vulnerabilities associated to a certain vendor and a certain product'''

    vendor = input("Which VENDOR?").lower()
    product = input("Which PRODUCT?").lower()
    request = requests.get(URL3 + "search/" + vendor + "/" + product, timeout=5).json()
    pprint.pprint(request)

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
