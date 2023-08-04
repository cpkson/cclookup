"""
Created on Fri Aug  4 10:38:12 2023

@author: parkic
"""
from dataclasses import dataclass
from typing import Any, Dict
from pandas import DataFrame

from ccMapper.data.glossary import CC_GLOSSARY
from ccMapper.exceptions import InvalidIATACodeError
from ccMapper.parser import iataParser
from ccMapper.types import IataCode, IsoNumericCode, IsoAlpha2Code, IsoAlpha3Code, IsoCountry, Airport


@dataclass
class IataCountryCode:
    """
        IATA standard representation of a country, including ISO standard representation
        of an airport & country

        Attributes:
            iataCode (str) : iata representation
    """

    iataCode: IataCode
    isoNumericCode: IsoNumericCode
    isoAlpha2Code: IsoAlpha2Code
    isoAlpha3Code: IsoAlpha3Code
    isoCountry: IsoCountry
    airport: Airport

    def __post_init__(self) -> None:
        """
            Parse given Iata code and compute relevant fields
        """
        if (self.iataCode in CC_GLOSSARY):
            _fields = CC_GLOSSARY[self.iataCode]
            self.isoNumericCode = _fields['numeric']
            self.isoAlpha2Code = _fields['Alpha2']
            self.isoAlpha3Code = _fields['Alpha3']
            self.isoCountry = _fields['Country']
            self.airport = _fields['Airport']
        elif (self.iataCode is not None):
            _iataCode, _fields = iataParser(self.iataCode)
            self.isoNumericCode = _fields['numeric']
            self.isoAlpha2Code = _fields['alpha2']
            self.isoAlpha3Code = _fields['alpha3']
            self.isoCountry = _fields['country']
            self.airport = _fields['airport']
            self.iataCode = _iataCode 

    @property
    def is_valid(self) -> bool:
        """
        Check if the given code is valid by official summary lookup.
        """
        return self.iataCode in CC_GLOSSARY

    def as_dict(self) -> Dict[str, Any]:
        """
        Get the dictionary respresentation of the IATA data structure
        """
        return {
            'iso_numeric': self.isoNumericCode,
            'iso_alpha_2': self.isoAlpha2Code,
            'iso_alpha_3': self.isoAlpha3Code,
            'country': self.isoCountry,
            'airport': self.airport
        }

    def __str__(self) -> str:
     """
     String representation of the given code.
     """
     return str(self.IataCode)

    def match_iata_countries(self, df: DataFrame, join_col: str = 'country') -> DataFrame:
        """
        Joins IATA country information onto a provided pandas dataframe

        Parameters
        ----------
        df : DataFrame
             Dataframe contain IATA country information
        join_col : str, optional
            DESCRIPTION. The default is 'country'.

        Returns
        -------
        DataFrame
            Joined IATA & ISO country information

        """
        countries_df = DataFrame.from_dict(CC_GLOSSARY)
        return df.join(countries_df, on=join_col, how='left')
