#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from random import sample
from string import digits, ascii_uppercase as uppercase
from numpy import array
from numpy.random import randint
from bs4 import BeautifulSoup as bs
import requests

def generate_id(length=20):
    ''' Create a random pathology ID of a specified length '''
    numbers = array(list(digits))
    indices = randint(0, 10, length)
    return numbers[indices]

def generate_mrn(length=8, alphanum=2):
    ''' Create a random medical record number (MRN) '''
    alphanumeric = ''.join(sample(uppercase), alphanum)
    return alphanumeric + generate_id(length)


class PII:

    def __init__(self, url="https://www.fakeaddressgenerator.com/"):
        self.url = url

    def generate(self):
        ''' Return a randomly generated profile '''
        response = requests.get(self.url)

        if response.status_code==200:
            return self.parse_profile(response.content)

        raise ValueError(f'Response status bad {response.status_code}. No profile could be returned.')

    def parse_profile(self, content):
        ''' Return a dict of randomly generated PII values '''
        soup = bs(content, 'html.parser')

        demographics = {}
        table_rows = soup.find('table').findAll('tr')

        for i, tr in enumerate(table_rows):
            values = []
            for tag in 'span strong'.split():
                text = tr.find(tag).text.encode('ascii', 'replace')
                text = text.replace(b"?", b" ").decode('utf8')

                if text:
                    values.append(text)
                else:
                    values.append(i)

            demographics.setdefault(*values)

        return demographics



if __name__=="__main__":
    print(generate_id())
    pii = PII()
    print(pii.generate())
