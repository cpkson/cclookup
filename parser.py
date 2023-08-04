# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 12:51:37 2023

@author: parkic
"""
from typing import Dict
from ccMapper.data.glossary import CC_GLOSSARY
from ccMapper.exceptions import InvalidIATACodeError

def iataParser(self, parse: str) -> Dict[str, Dict[str, str]]:
    """
    Parses the submitted code to see if IATA airport

    Parameters
    ----------
    parse : str
        code to parse.

    Returns
    -------
    Dict[str, Dict[str, str]]
        Dictionary of results

    """
    for x, k in CC_GLOSSARY.items:
        if parse == k['airport']:
            return x, k

    raise InvalidIATACodeError('Airport not found in the official IATA glossary')
