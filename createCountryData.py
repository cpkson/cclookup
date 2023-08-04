"""
"""

import xml.etree.ElementTree as etree
import pandas as pd
from pandas import DataFrame
from os import walk
import json

def main():
    """
    

    Returns
    -------
    None.

    """
    
    with open("config.json") as json_data_file:
        config = json.load(json_data_file)
    

    xml_file=open(config['data']['output_data_path']+config['files']['xml_output_file'],"r")
    
    xml_string = xml_file.read()
    
    dct = xml_to_dict(xml_string)
    
    print(str(dct))


def xml_to_dict(xml_string):
    root = etree.fromstring(xml_string)
    result = {}
    for child in root:
        if len(child) == 0:
            result[child.tag] = child.text
        else:
            result[child.tag] = xml_to_dict(etree.tostring(child))
    return result


def load_data(f_path : str) -> DataFrame:
    """
    

    Parameters
    ----------
    f_path : str
        Local file path data is stored in

    Returns
    -------
    DataFrame
        loaded data in DataFrame format.

    """
    filenames = next(walk(f_path), (None, None, []))[2]  # [] if no file

    df_list = []
    for f in filenames:
        try:
            df = pd.read_csv(f_path + f)
            df_list.append(df.astype(str))
        except FileNotFoundError:
            print('CSV file not found')
            return 0
    
    df = pd.concat(df_list)
    
    iata_countries = ['UK',
                      'United Kingdom', 
                      'USA',
                      'Russia',
                      'Netherlands',
                      'United Arab Emirates',
                      'USA (LA)',
                      'Central African Republic',
                      'Dominican Republic',
                      'Channel Islands',
                      'The Bahamas']
    
    iso_countries =  ['United Kingdom of Great Britain and Northern Ireland (the)',
                      'United Kingdom of Great Britain and Northern Ireland (the)',
                      'United States of America (the)',
                      'Russian Federation (the)',
                      'Netherlands (the)',
                      'United Arab Emirates (the)',
                      'United States of America (the)',
                      'Central African Republic (the)',
                      'Dominican Republic (the)',
                      'Guernsey',
                      'Bahamas (the)']
    
    df['Country'] = df['Country'].replace(iata_countries,iso_countries)
    df = df.fillna('')
    
    return df
    
def combine_data(iata_data : DataFrame, iso_data : DataFrame) -> DataFrame:
    """
    

    Parameters
    ----------
    iata_data : DataFrame
        DataFrame containing Iata data.
    iso_data : DataFrame
        DataFrame containing Iso data.

    Returns
    -------
    DataFrame
        ISO and IATA combined DataFrame.

    """
    return iata_data.join(iso_data.set_index('Country'),on='Country',how='left')
    
    
if __name__ == "__main__":
    main()