#!/usr/bin/env python
from pathlib import Path
from contents import parse, get_text

def get_hash(doc):
    ''' Return the hash of the specified doc

    Parameters
    ----------
        doc : Path
            Path to file to hash
    '''
    return hash(get_text(doc))

def compare_documents(doc1, doc2, checked):
    ''' Return True of specified documents have the same content

    Parameters
    ----------
        doc1 : Path
            Path to first file to check
        doc2 : Path
            Path to second file to check
        checked : dict
            Object with documents previously checked for memoization
    '''
    if doc1 in checked:
        memo = checked[doc1]
    elif doc2 in checked:
        memo, doc1, doc2 = checked[doc2], doc2, doc1
    else:
        memo = {}

    if doc2 not in memo:
        memo[doc2] = get_hash(doc1) == get_hash(doc2)

    checked[doc1] = memo

    return checked

def compare_directory(directory, glob='rec*'):
    ''' Return dict with duplicate file names

    Parameters
    ----------
        directory : Path
            Directory with documents to check
    '''
    documents = list(directory.glob(glob))
    list_size = len(documents) - 1
    checked = {}

    for i, first in enumerate(documents):
        for j, second in enumerate(documents):

            if i != j and i < list_size and j < list_size:
                checked = compare_documents(first, second, checked)

    return checked
