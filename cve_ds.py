'''File for CVE DATA SCIENCE'''
import json
import pprint
import requests
# Documentation: https://requests.readthedocs.io/en/latest/
from requests.auth import HTTPBasicAuth
# Needed for authentification for opencve.io




class CVESearch:
    '''
    Class for CVE-Search etc.
    '''

    def __init__(self) -> None:
        self.url = "https://cvepremium.circl.lu/api/"

    def get_vendors(self):
        '''Returns all vendors stored in the databases'''

        request = requests.get(self.url + "browse")
        #print(request.json())
        pprint.pprint(request.json())

    def get_products_per_vendor(self):
        '''Get all the products associated to a vendor with known CVEs'''

        vendor = input("For which vendor do you want to know the products?")
        request = requests.get(self.url + "browse/" + vendor).json()
        pprint.pprint(request)

    def get_vulnerabilities_per_product(self):
        '''Get all the vulnerabilities associated to a certain vendor and a certain product'''

        vendor = input("Which vendor?").lower()
        product = input("Which product?").lower()
        request = requests.get(self.url + "search/" + vendor + "/" + product).json()
        pprint.pprint(request)

    def get_cve_info(self):
        '''Get infos about a certain CVE'''

        cve = input("What CVE are you searching for?")
        request = requests.get(self.url + "cve/" + cve).json()
        pprint.pprint(request)

    def db_info(self):
        '''Get infos about the used databases of the API'''

        request = requests.get(self.url + 'dbInfo').json()
        pprint.pprint(request)

    def latest_30_cves(self):
        '''Print newest 30 CVEs which were uploaded to the DBs'''
        pass
# Missing functions

    '''
    To get a JSON of the last 30 CVEs including CAPEC, CWE and CPE expansions
    '''
#last_30_CVEs = requests.get('https://cve.circl.lu/api/last')
#print(last_30_CVEs.text)



#test = CVE_Search()
#test.getVendors()
#test.getProductsPerVendor()
#test.getVulnerabilitiesPerProduct()
#test.getCVEInfo()
#test.dbInfo()



# OpenCVE offers a public API to retrieve DATA:
# Documentation can be found at: https://docs.opencve.io/
# API to retrieve CVE data from OpenCVE: https://www.opencve.io/api

'''
To get a JSON with all the products associated to a vendor
e.g. vendor = microsoft --> .../vendors/microsoft
'''
# vendors =  requests.get('https://www.opencve.io/api/vendors/microsoft', auth = HTTPBasicAuth('CyberRadar', 'Test123'))
# print(format(vendors.json()))

'''
To get a JSON with all the products associated to a vendor
e.g. vendor = microsoft --> .../vendors/microsoft/products
'''
# microsoft = requests.get('https://www.opencve.io/api/vendors/microsoft/products', auth = HTTPBasicAuth('CyberRadar', 'Test123'))
# print(format(microsoft.json()))
# print(microsoft.json())
# cves_product_cve = requests.get('https://www.opencve.io/api/vendors/microsoft/products/powerpoint/cve', auth = HTTPBasicAuth('CyberRadar', 'Test123'))
# print(format(cves_product_cve.json()))
