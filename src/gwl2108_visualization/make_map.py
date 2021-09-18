import plotly.express as px
import json
import pandas as pd
import numpy as np


state = 'il'
data = 'FCC'
field = 'max_up'

data_path = '/home/grace/cluster_code/broadband_dd/data/'
state_centers = {'il': [39.73,-89.45]} #gotta add other states

#Get the json file I made from the shape file (using make_map_json.py)
with open(data_path+state+'shape') as geofile:
    j_file = json.load(geofile)
for feature in j_file["features"]: #doing this because plotly needs an 'id' field with unique identifiers
    feature ['id'] = feature['properties']['GEOID'] 

if data == 'FCC':
    df = pd.read_csv(data_path+'fcc_477_census_tract_'+state.upper()+'.csv')
    id_name = 'tract'
elif data == 'ACS':
    df = pd.read_csv(data_path+'acs_2019_'+state.upper()+'.csv')
    id_name = 'geoid'
else: 
    print('invalid data type')# add error

field_vals = df[field].to_numpy()

fig = px.choropleth_mapbox(df, geojson=j_file, locations=id_name, color=field,color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",range_color=(np.min(field_vals),np.max(field_vals)),
                           zoom=6, center = {"lat": state_centers[state][0], "lon": state_centers[state][1]},
                           opacity=0.5)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.show()

