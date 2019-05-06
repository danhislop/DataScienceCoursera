#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 11:59:06 2019

@author: danhi
"""

"""
An example illustrating how to index pandas DataFrames. 
source reading and example was https://brohrer.github.io/dataframe_indexing.html
I went through and added my own labels at to what each .loc or .iloc was doing
"""
import numpy as np
import pandas as pd

mtns = pd.DataFrame([
    {'name': 'Mount Everest',
        'height (m)': 8848,
        'summited': 1953,
        'mountain range': 'Mahalangur Himalaya'},
    {'name': 'K2',
        'height (m)': 8611,
        'summited': 1954,
        'mountain range': 'Baltoro Karakoram'},
    {'name': 'Kangchenjunga',
        'height (m)': 8586,
        'summited': 1955,
        'mountain range': 'Kangchenjunga Himalaya'},
    {'name': 'Lhotse',
        'height (m)': 8516,
        'summited': 1956,
        'mountain range': 'Mahalangur Himalaya'},
])
mtns.set_index('name', inplace=True)

# show the dataframe
print("Remember: ------\n")
print("Use .loc[] for lables \n")
print("Use .iloc[] for positions \n\n\"")
print('\n df is: \n', mtns)

print('\n return a series of one column (will include index) \n')
print(mtns.loc[:, 'height (m)'])
print(type(mtns.loc[:, 'height (m)']))

print('\n return a numpy array of one column \n')
print(mtns.loc[:, 'height (m)'].values)
print(type(mtns.loc[:, 'height (m)'].values))

print('\n find all rows [:, of a single column ,mountain range  \n')
print(mtns.loc[:, 'mountain range'])

print('\n find a single row and all columns of it \n')
print(mtns.loc['K2', :])

print('\n find a single row and a single column \n')
print(mtns.loc['K2', 'mountain range'])

print('\n find several rows, given specific labels \n')
print(mtns.loc[['K2', 'Lhotse'],:])
print(mtns.loc[['height (m)' == 8848],:])

print('\n find several columns in a row \n')
print(mtns.loc[:, 'height (m)': 'mountain range'])

print('\n find specific columns \n')
print(mtns.loc[:, ['height (m)', 'summited']])

print('\n find all rows where a column value meets criteria \n')
print(mtns.loc[mtns.loc[:, 'summited'] <= 1954, :])
print(mtns.loc[mtns.loc[:, 'mountain range'] == 'Mahalangur Himalaya',:])

print('\n now using iloc, we find data by row and column number \n')
print(mtns.iloc[0, :])
print(mtns.iloc[:, 2])
print(mtns.iloc[0, 2])
print(mtns.iloc[[1, 3], :])
print(mtns.iloc[:, 0:2])
print('\n this first narrows by position, then locates K2 row within \n')
print(mtns.iloc[:, 0:2].loc['K2', :])
#print(mtns.iloc[:, 0].loc['K2', :])
