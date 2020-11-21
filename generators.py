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
    '''Simple PII generator class that pulls data from a fake address generator website.'''

    def __init__(self, url="https://www.fakeaddressgenerator.com/"):
        self.url = url

    def __repr__(self):
        ''' Generate a random profile and pretty print it to the screen '''
        data = self.generate()
        profile = None

        if data:
            items = data.items()
            width = max(len(a) for a, b in items)
            profile = '\n'.join(f'{a:>{width}}: {b}' for a, b in items)

        return f"PII(profile=\n{profile}\n)"

    def generate(self):
        ''' Return a randomly generated profile '''
        response = requests.get(self.url)

        if response.status_code==200:
            return self.parse_profile(response.content)

        print(f'Response status bad {response.status_code}. No profile could be returned.')

    def parse_profile(self, content):
        ''' Return a dict of randomly generated PII values

        Parameters
        ----------
            content (string): raw HTML content from GET request
        '''
        soup = bs(content, 'html.parser')

        table_rows = soup.find('table').findAll('tr')
        other_rows = soup.findAll('div', {'class': 'row item'})
        all_rows = table_rows + other_rows

        demographics = {}
        # Main demographic section
        for i, tr in enumerate(all_rows):
            values = []
            for tag in 'span strong'.split():
                text = tr.find(tag).text.encode('ascii', 'replace')
                text = text.replace(b"?", b" ").decode('utf8')

                if text:
                    values.append(text)
                else:
                    break
            else:
                demographics.setdefault(*values)

        return demographics



if __name__=="__main__":
    print(generate_id())
    pii = PII()
    print(pii.generate())
