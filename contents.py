#!/usr/bin/env python
# File with scripts to extract contents from documents with XML tags
from bs4 import BeautifulSoup as bs
from pathlib import Path
import lxml
import re

def parse(document):
    '''Return a BeautifulSoup XML object or None if no document specified

    Parameter
    ---------
        document : str, Path
            Path to XML document for parsing
    '''
    if isinstance(document, str):
        document = Path(document)

    with document.open('r') as fin:
        lines = [__.strip() for __ in fin.readlines() if __.strip()][1:] # Skip the first xml tag to parse NCI.XMLs
        content = ''.join(lines)
        return bs(content, 'lxml')

def get_contents(document):
    '''Return the string contents of a document

    Parameter
    ---------
        document : str, Path
            Path to XML document for parsing
    '''
    return parse(document).text

def get_text(document, naaccrid="text.*"):
    '''Return the text content of an NCI.XML document

    Parameter
    ---------
        document : str, Path
            Path to XML document for parsing
        naaccrid : str
            Id of naaccrid to parse from the document
    '''
    document = parse(document)
    text_naaccr_ids = document.findAll("item", { "naaccrid" : re.compile(naaccrid) } )
    text_content = [__.text for __ in text_naaccr_ids]
    return '\n'.join(text_content)

