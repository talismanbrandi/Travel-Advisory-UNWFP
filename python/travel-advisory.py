#!user/bin/python3

import pandas as pd
import requests

def main():
    '''
    This code pulls from a data base maintained by UNWFP for international travel advisory. 
    input fields: adm0_name, x, y , published, sources, info, optional2, optional3, ObjectId (sources and ObjectId are not used)
        adm0_name -> Country, 
        x -> Lat, 
        y -> Long, 
        published -> Date-Published, 
        info -> TravelAdvisory, 
        optional2 -> Quarantine, 
        optional3 -> COVID-19-Testing
    ouput fields: Country, Lat, Long, Date-Published, TravelAdvisory, Quarantine, COVID-19-Testing
    output file: ../data/travel-advisory.json
    '''
    url = 'https://services3.arcgis.com/t6lYS2Pmd8iVx1fy/ArcGIS/rest/services/COVID_Travel_Restrictions_V2/FeatureServer/0/query'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = {
        'f': 'json',
        'where': '0=0',
        'outFields': 'adm0_name,x,y,published,sources,info,optional2,optional3,ObjectId',
    }

    data = requests.get(url, headers=headers, params=params).json()

    df = pd.DataFrame.from_dict(data['features'])
    df = (pd.DataFrame.from_dict([elem[1] for elem in list(df['attributes'].items())])
          .rename(columns={'info': 'TravelAdvisory', 'optional2': 'Quarantine', 'optional3': 'COVID-19-Testing', 'adm0_name': 'Country', 'published': 'Date-Published', 
                           'x': 'Lat', 'y': 'Long'})
          .drop(columns=['sources', 'ObjectId']))
    df = df.sort_values(by='Country')
    df.to_json('../data/travel-advisory.json', orient='records')


if __name__ == "__main__":
    # execute only if run as a script
    main()
