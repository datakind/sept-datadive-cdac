#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 10:21:21 2021

@author: vm
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#import dataset
quad = pd.read_csv('ookla_combined_fl.csv',  encoding='utf-8')
tract = pd.read_csv('fcc_477_census_tract_FL.csv')



#make a list of keys
quadkey_list = quad['quadkey'].unique()
tractqu_list = quad['GEOID'].unique()

tractce = tract['tract'].unique()


mean1_dn = np.array([]) #standard mean
mean2_dn = np.array([]) #weighted by number of tests 
mean3_dn = np.array([]) #weighted nby number of devices

mean1_up = np.array([]) #standard mean
mean2_up = np.array([]) #weighted by number of tests 
mean3_up = np.array([]) #weighted nby number of devices


#for download speed only here
for i in range(len(tractce)):

    tr = tractce[i]
    
#    find means by geoid
    tr_ookla = quad [quad['GEOID']==tr]
    tr_fcc = tract[tract['tract'] == tr]
    
    dn_spd = tr_ookla['avg_d_kbps'].to_numpy().astype('float')
    up_spd = tr_ookla['avg_u_kbps'].to_numpy().astype('float')
    
    #simple average
    mean1_dn = np.append(mean1_dn,np.mean(dn_spd)/1000)
    mean1_up = np.append(mean1_up,np.mean(up_spd)/1000)
    
    #weighted by number of tests
    n_test = tr_ookla['tests'].to_numpy().astype('float')
    mean2_dn = np.append(mean2_dn,np.mean(np.multiply(dn_spd,n_test))/(np.sum(n_test)*1000))
    mean2_up = np.append(mean2_up,np.mean(np.multiply(up_spd,n_test))/(np.sum(n_test)*1000))

    #weighted by number of devices
    n_devices = tr_ookla['devices'].to_numpy().astype('float')
    mean3_dn = np.append(mean3_dn, np.mean(np.multiply(dn_spd,n_devices))/(np.sum(n_devices)*1000))
    mean3_up = np.append(mean3_up, np.mean(np.multiply(up_spd,n_devices))/(np.sum(n_devices)*1000))

dn_diff = np.nansum(np.abs(mean2_dn-mean3_dn))/len(mean2_dn)
up_diff = np.nansum(np.abs(mean2_up-mean3_up))/len(mean2_up)
