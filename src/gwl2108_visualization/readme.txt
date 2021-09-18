This code creates a map with census tract outlines and colors determined by a given field value of a given dataset (for now FCC or ACS). It uses plotly, geopandas, pandas, and numpy.

Using plotly, shape files need to be turned into a geo json file. This is done in make_map_json.py

Once that is done, make_map.py can be used to create a map based on the desired values. 
