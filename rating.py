'''This file is for the personal rating algorithm'''
import datetime

def rate(cve_info:tuple, mentions:int) -> int:
    """
    Function to create a personal rating based on 
    the times the CVE was mentioned
    the date the CVE was last modified
    calculated together with the CVSS score


    Args:
        cve_info (tuple): contains CVSS score [0] & last modified date [3]
        mentions (int): times the CVE was mentioned

    Returns:
        int: personal score
    """
    time = 1
    mention = 1
    score = cve_info[0]

    date1 = datetime.date.today()

    if cve_info[3] is not None:
        date2 = datetime.datetime(int(cve_info[3][:4]), \
                                    int(cve_info[3][5:7]), \
                                    int(cve_info[3][8:10]))
        if date2.year < date1.year:
            time = 1.2
        elif date2.month < date1.month:
            time = 1.1

    if mentions > 10:
        mention = 1.3

    if score != 0:
        score = round(cve_info[0] * time * mention, 1)
        if score > 10:
            score = 10
    elif score == 0 and mentions > 10:
        score = 5

    return score
