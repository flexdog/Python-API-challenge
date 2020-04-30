# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 11:59:32 2020

@author: fbjba
"""

# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import gmaps
import os

# Import API key
from api_keys import g_key

weather_df=pd.read_csv('weather_df.csv')
weather_df.head()

gmaps.configure(api_key=g_key)

locations = weather_df[['Lat', 'Lng']]
weights = weather_df['Humidity']

fig=gmaps.figure()
fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
fig

desired_weather_df = weather_df[weather_df['Temp'].gt(69) & weather_df['Temp'].lt(81) & weather_df['Humidity'].gt(29) & weather_df['Humidity'].lt(61)].reset_index()
desired_weather_df.head()

hotel_df = desired_weather_df[['City','Lat', 'Lng']].copy()
hotel_df['Hotel'] = hotel_df.apply(lambda _: '', axis=1) 

hotel_df.head()

hotel_list=[]
Lat_list=[]
Lng_list=[]
City_list=[]
for row in hotel_df.itertuples():
    #
     
    #base url
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"+"location=" + str(row.Lat) +"," +str(row.Lng) + "&radius=5000&type=hotel&keyword=hotel&key=" + g_key
    
    # Execute request
    response = requests.get(base_url)
    try:
        jaysponse = response.json()
        if jaysponse['status'] == "ZERO_RESULTS":
           response.raise_for_status()
        else:
            # Convert response to json
            hotel_list.append(jaysponse['results'][0]['name'])
            Lat_list.append(jaysponse['results'][0]['geometry']['location']['lat'])
            Lng_list.append(jaysponse['results'][0]['geometry']['location']['lng'])
            City_list.append(row[1])
    except KeyError:
        print(f"No hotel found nearby.")
        
print(hotel_list)