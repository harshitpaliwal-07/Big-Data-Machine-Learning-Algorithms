'''
Clean dataset with pandas
command to create log: python depricated/pandas_turtles.py > depricated/logs/pandas_turtles.log
'''

# imports
import pandas as pd 
from numpy import *

# read dataframe
df = pd.read_csv('data/turtles/turtles.csv')

# select subset of columns
df = df[['Species',
        'Dead_Alive',
        'Gear',
        'SCL_notch',
        'SCL_tip',
        'SCW',
        'CCL_notch',
        #'Circumference', # has 13k na values and only 63 actual entries
        #'Girth', # has 11k na value and only 2k actual entries
        #'Depth_mid', # has 13k na values and only 181 actual entries
        #'Tail', # has 13k na values and only 8 actual values
        #'Weight', # has 11k na values and only 2k actual entries
        #'Cap_Region', # 11k inshore and only 141 offshore
        'TestLevel_Before',
        #'TestLevel_After', # 12k na values and only 1167 entries
        'Entangled']]

# clean data
#    Species
df.dropna(subset=['Species'],inplace=True) # drop any record without a species label
df = df.loc[df['Species'].isin(['Loggerhead','Green','Kemps_Ridley'])] # other species have < 10 total tags
#    Dead_Alive
df['Dead_Alive'].replace({'Alive':'alive','Dead':'dead'},inplace=True) # correct capitalization
#    Gear
df['Gear'].replace(
    {cat:'Other' for cat in ['Shrimp trawl','General public sighting','Channel net','Headstart','Flounder trawl']},
    inplace=True) # categories with < 10 captures --> 'other' label
#    numeric columns
for col in ['SCL_notch','SCL_tip','SCW','CCL_notch','TestLevel_Before']:
    df[col].replace({0:nan},inplace=True) # 0 is put in instead of na --> correct to na
    means = df.groupby('Species')[col].transform('mean') # get mean by species
    df[col].fillna(means,inplace=True) # fill na with species mean 
#    Entangled
df['Entangled'].replace({True:'entangled',False:'free'},inplace=True) # make object from boolean

# summarize data
for col in df.columns:
    print 'col:',col
    col_dtype = df[col].dtype
    print 'dtype:',col_dtype
    print 'na values:',df[col].isnull().sum()
    if col_dtype == int or col_dtype==float:
        print(df[col].describe())
    else:
        print(df[col].value_counts())
    print '\n'

# preview dataframe
print(df.head())

# export dataframe
df.to_csv('data/turtles/turtles_clean_pandas.csv',index=False,header=False)