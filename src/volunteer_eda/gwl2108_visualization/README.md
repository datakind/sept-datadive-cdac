## FCC and/or ACS data visualization

This code creates a map with census tract outlines and colors determined by a given field value of a given dataset (for now FCC or ACS). It uses plotly, geopandas, pandas, and numpy.

Using plotly, shape files need to be turned into a geo json file. This is done in make_map_json.py

Once that is done, make_map.py can be used to create a map based on the desired values. 

There is also a separate script for looking at how different values in the ACS file are correlated. It produces a figure with a correlation matrix for pairs of broadband and socio-economic values. Note: the ACS file needs to be cleaned up to remove outlier rows that are messing up these results. 

Here is a link to a google colab that can connect all the accessible data in GoogleDrive: https://colab.research.google.com/drive/14VzM9Uy6TiaEQoLeDxU2abHYDTlWjfcz?usp=sharing

