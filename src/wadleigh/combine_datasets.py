#simple code to join the data sets 
#This code expects the raw data files to be in a folder named "Broadband_Data" in the same folder as this file

import pandas as pd
import os

#file names
ookla_data = "ookla_combined_nv.csv"
fcc_data = "fcc_477_census_tract_NV.csv"
acs_data = "acs_2019_NV.csv"

#folder where files are saved
dirname = os.path.dirname(__file__)
data_folder_path = os.path.join(dirname, "Broadband_Data")

#join folder and file name
ookla_dataframe = pd.read_csv(os.path.join(data_folder_path, ookla_data))
fcc_dataframe = pd.read_csv(os.path.join(data_folder_path, fcc_data))
acs_dataframe = pd.read_csv(os.path.join(data_folder_path, acs_data))

#rename the GEOID column of the FCC data to "GEOID" in order to merge (tract in the FCC data is the GEOID of each tract)
fcc_dataframe.rename(columns={"tract": "GEOID"}, inplace = True)
acs_dataframe.rename(columns={"geoid": "GEOID"}, inplace = True)

merged_dataframe = pd.merge(fcc_dataframe, ookla_dataframe, how="outer", on=["GEOID"])
merged_dataframe = pd.merge(merged_dataframe, acs_dataframe, how="outer", on=["GEOID"])

#print the start of the merged dataframe and the list of column names, just to check
print(merged_dataframe.head())
print(list(merged_dataframe.columns))

#functions to aggregate data from stack overflow
#https://stackoverflow.com/questions/10951341/pandas-dataframe-aggregate-function-using-multiple-columns
def wavg_func(datacol, weightscol):
    def wavg(group):
        dd = group[datacol]
        ww = group[weightscol] * 1.0
        return (dd * ww).sum() / ww.sum()
    return wavg


#https://stackoverflow.com/questions/10951341/pandas-dataframe-aggregate-function-using-multiple-columns
def df_wavg(df, groupbycol, weightscol):
    grouped = df.groupby(groupbycol)
    df_ret = grouped.agg({weightscol:sum})
    datacols = [cc for cc in df.columns if cc not in [groupbycol, weightscol]]
    for dcol in datacols:
        try:
            wavg_f = wavg_func(dcol, weightscol)
            df_ret[dcol] = grouped.apply(wavg_f)
        except TypeError:  # handle non-numeric columns
            df_ret[dcol] = grouped.agg({dcol:min})
    return df_ret

#calculate and save the data averaged for each GEOID
ave_mergded_dataset = df_wavg(merged_dataframe, 'GEOID','devices')

ave_merged_dataset_name = 'averaged_merged_data_NV.csv'
ave_mergded_dataset.to_csv(os.path.join(data_folder_path, ave_merged_dataset_name))