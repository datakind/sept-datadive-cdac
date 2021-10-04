import geopandas as gpd
import plotly as ply
import json


data_path = '/home/grace/cluster_code/broadband_dd/data/'
state = 'il'
shp_file_path = data_path+state+'_spdf.shp'

geodf = gpd.read_file(shp_file_path)

geodf.to_file(data_path+state+'shape', driver = "GeoJSON")
with open(data_path+state+'shape') as geofile:
    j_file = json.load(geofile)
