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
    
    iata_data = load_data(config["data"]["iata_data_path"])
    iso_data = load_data(config["data"]["iso_data_path"])
    
    combined_data = combine_data(iata_data, iso_data)
    combined_data = combined_data.astype(str)
    combined_data = combined_data.replace('nan', ' ')
    root = etree.Element('data');

    for i,row in combined_data.iterrows():
        item = etree.SubElement(root, row['IATA code'])
        airport = etree.SubElement(item,'Airport')
        airport.text = row['Airport']
        country = etree.SubElement(item, 'Country')
        country.text = row['Country']
        alpha2 = etree.SubElement(item, 'Alpha2')
        alpha2.text = row['Alpha2']
        alpha3 = etree.SubElement(item, 'Alpha3')
        alpha3.text = row['Alpha3']
        numeric = etree.SubElement(item, 'numeric')
        numeric.text = row['Numeric']

    if config["data"]["output_data_path"] is None:
        return 
    with open(config["data"]["output_data_path"]+config['files']['xml_output_file'], 'w') as f:
        f.write(etree.tostring(root).decode())


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