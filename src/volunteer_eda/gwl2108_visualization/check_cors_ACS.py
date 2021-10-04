import numpy as np
import pandas as pd
import plotly.express as px

#this code checks the extent to which socio-economic values in the ACS data are correlated with broadband access values. BUT THE ACS FILE HAS SOME OUTLIERS (e.g., rows with 0s and other odd values) THAT ARE MESSING UP THESE CALCULATIONS, THEY NEED TO BE REMOVED BEFORE THESE PLOTS CAN BE OF VALUE. Also, a lot of the broadband related values are close to ceiling, which makes correlation difficult to interpret as well. 

state = 'il'
data_path = '/home/grace/cluster_code/broadband_dd/data/'
#load ACS
df = pd.read_csv(data_path+'acs_2019_'+state.upper()+'.csv')


#want to create a new internet variable from the number of children and number of children with comptuers (can also use this to turn other values into fractions)
def child_comp(row):
    return row['n_children_computer']/row['n_children']
def any_internet(row):
    return row['nhh_computer_any_internet']/row['households']

df['f_child_comp'] = df.apply (lambda row: child_comp(row), axis=1)
df['f_any_internet'] = df.apply (lambda row: any_internet(row), axis=1)


broadband = ['f_broadband','f_computer','f_child_comp','f_any_internet']
socio_econ = ['mhi','f_black','f_hispanic']


b_vals = []
se_vals = []
for b_name in broadband:
    b_vals.append(df[b_name].to_numpy())
for se_name in socio_econ:
    se_vals.append(df[se_name].to_numpy())

b_vals = np.array(b_vals); se_vals = np.array(se_vals)

corrs = np.zeros((len(broadband),len(socio_econ)))
for bi in range(len(b_vals)):
    for sei in range(len(se_vals)):
        inds = np.intersect1d(np.where(~np.isnan(se_vals[sei,:]))[0],np.where(~np.isnan(b_vals[bi,:]))[0])
        corrs[bi,sei] = np.corrcoef(se_vals[sei,inds],b_vals[bi,inds])[0,1]


fig = px.imshow(corrs.T,y=socio_econ, x=broadband)
fig.show()

