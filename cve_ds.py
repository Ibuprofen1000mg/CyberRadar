'''File for CVE DATA SCIENCE'''
import pprint
import requests

URL = "https://cvepremium.circl.lu/api/"

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

def get_cve_info(cvenumber):
    '''Get infos about a certain CVE'''

    #cve = input("What CVE are you searching for?")
    request = requests.get(URL + "cve/" + cvenumber, timeout=50).json()
    #pprint.pprint(request.get('id'), request.get('summary'))
    # print(request.get('id'))
    # print(request.get('summary'))
    return request

def get_cve_severity_and_score(cvenumber):
    '''Return the severity and the cvss of a CVE'''
    request = requests.get(URL + "cve/" + cvenumber, timeout=50).json()
    return request["typical_severity"], request["cvss3"]

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


# test = CVESearch()
#test.get_vendors()
#test.get_products_per_vendor()
#test.get_vulnerabilities_per_product()
#test.get_cve_info()
#test.db_info()
# test.latest_30_cves()
