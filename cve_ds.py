'''File for CVE DATA SCIENCE'''
import pprint
import requests

class CVESearch:
    '''
    Class for CVE-Search etc.
    '''

    def __init__(self) -> None:
        self.url = "https://cvepremium.circl.lu/api/"

    def get_vendors(self):
        '''Returns all vendors stored in the databases'''

        request = requests.get(self.url + "browse", timeout=5).json()
        pprint.pprint(request.keys())
        print(type(request)) #Dict
        print(request.get('vendor')[10]) #List

    def get_products_per_vendor(self):
        '''Get all the products associated to a vendor with known CVEs'''

        vendor = input("For which VENDOR do you want to know the products?")
        request = requests.get(self.url + "browse/" + vendor, timeout=5).json()
        pprint.pprint(request)

    def get_vulnerabilities_per_product(self):
        '''Get all the vulnerabilities associated to a certain vendor and a certain product'''

        vendor = input("Which VENDOR?").lower()
        product = input("Which PRODUCT?").lower()
        request = requests.get(self.url + "search/" + vendor + "/" + product, timeout=5).json()
        pprint.pprint(request)

    def get_cve_info(self):
        '''Get infos about a certain CVE'''

        cve = input("What CVE are you searching for?")
        request = requests.get(self.url + "cve/" + cve, timeout=5).json()
        #pprint.pprint(request.get('id'), request.get('summary'))
        print(request.get('id'))
        print(request.get('summary'))

    def db_info(self):
        '''Get infos about the used databases of the API'''

        request = requests.get(self.url + 'dbinfo', timeout=5).json()
        pprint.pprint(request)

    def latest_30_cves(self):
        '''Print newest 30 CVEs which were uploaded to the DBs'''

        request = requests.get(self.url + 'last', timeout=5).json()
        pprint.pprint(request)
        for vul in request:
            print(vul.get('id'))
            print(vul.get('summary'))
            print(vul.keys())


test = CVESearch()
test.get_vendors()
#test.get_products_per_vendor()
#test.get_vulnerabilities_per_product()
#test.get_cve_info()
#test.db_info()
#test.latest_30_cves()

'''CVE-ID und Titel ausgeben'''

# OpenCVE offers a public API to retrieve DATA:
# Documentation can be found at: https://docs.opencve.io/
# API to retrieve CVE data from OpenCVE: https://www.opencve.io/api

# auth = requests.HTTPBasicAuth('CyberRadar', 'Test123'))
# '''
# To get a JSON with all the products associated to a vendor
# e.g. vendor = microsoft --> .../vendors/microsoft
# '''
# vendors =  requests.get('https://www.opencve.io/api/vendors/microsoft', auth = )
# print(format(vendors.json()))

# '''
# To get a JSON with all the products associated to a vendor
# e.g. vendor = microsoft --> .../vendors/microsoft/products
# '''
# microsoft = requests.get('https://www.opencve.io/api/vendors/microsoft/products', auth = )
# print(format(microsoft.json()))
# print(microsoft.json())
# cves_product_cve = requests.get('https://www.opencve.io/api/vendors/microsoft/products/powerpoint/cve', auth = )
# print(format(cves_product_cve.json()))
