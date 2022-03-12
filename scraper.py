#!/usr/bin/env python3

from bs4 import BeautifulSoup
import lxml
import requests

# pip3 install bs4 lxml requests


class ClaimStatusScraper:

    BASE_URL = 'https://ucpi.sco.ca.gov/en/Claim'
    CLAIM_STATUS_URL = 'https://ucpi.sco.ca.gov/en/Claim/ClaimStatus'

    cookies = None
    hidden_inputs = {}

    def __init__(self):
        self.init_session()


    def init_session(self):
        # Get cookies and the token from the search form
        r = requests.get(self.CLAIM_STATUS_URL, 
                         cookies=requests.cookies.RequestsCookieJar())
        self.cookies = r.cookies
        self.hidden_inputs = { input.get('name') : input.get('value') \
                               for input in self.xpath(r.text, '//form/input')}
    

    def status(self, claim_id):
        payload = {
            'claimId': claim_id
        }
        payload.update(self.hidden_inputs)
        r = requests.post(self.CLAIM_STATUS_URL, cookies=self.cookies, data=payload)
        selector  = '//table[@class="hrs-table"]/tbody/tr/td[2]/text()'
        return str(self.xpath(r.text, selector)[0])


    def xpath(self, text, selector):
        soup = BeautifulSoup(text, 'html.parser')
        dom = lxml.etree.HTML(str(soup))
        return dom.xpath(selector)


if __name__ == '__main__':
    import sys

    scraper = ClaimStatusScraper()
    claim_id = sys.argv[1]
    print(scraper.status(claim_id))
