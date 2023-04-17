'''File to create own rating'''
import datetime
import cve_ds

class Rating:
    '''Class for rating the different CVEs based on different params'''

    def __init__(self) -> None:
        self.time = 0
        self.mention = 0.1

    def rate(self, cve: list, reference: int = None):
        d1 = datetime.datetime(2023,4,17)
        d2 = datetime.datetime(int(cve['last-modified'][:4]),int(cve['last-modified'][5:7]),int(cve['last-modified'][8:10]))
        test = [d1,d2]
        print(d1 == d2)
        print(test)
        if not d2.year < d1.year:
            if d2.month < d1.month-2:
                self.time = 0.4


cve_class = cve_ds.CVESearch()
rate = Rating()
print(cve_class.get_cve_info("CVE-2021-4228")['last-modified'])
rate.rate(cve_class.get_cve_info("CVE-2021-4228"))
