'''File to create own rating'''
import datetime
import cve_ds
from reddit import RedditCVE

class Rating:
    '''Class for rating the different CVEs based on different params'''

    def __init__(self) -> None:
        self.time = 1
        self.mention = 1

    def rate(self, cve_info, mentions):
        '''Rating function'''
        date1 = datetime.date.today()
        date2 = datetime.datetime(int(cve_info[0]['date_modified'][:4]), \
                                  int(cve_info[0]['date_modified'][5:7]), \
                                  int(cve_info[0]['date_modified'][8:10]))
        if not date2.year < date1.year:
            print("Year !<")
            if date2.month < date1.month:
                print("Month <")
                self.time = 0.8

        if mentions > 3:
            self.mention = 1.3

        print(self.time, self.mention)

        score = round(cve_info[1]["cvssV3_score"] * self.time * self.mention, 1)
        print(score)
        if score > 10:
            score = 10
        print(cve_info[1]["cvssV3_score"])
        return score


rate = Rating()
print(rate.rate(cve_ds.get_cve_info2("CVE-2023-23397"), RedditCVE().retrieve_cve_count("CVE-2023-23397")))
