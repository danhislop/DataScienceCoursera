#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 11:20:30 2019

@author: danhi
"""

'''
This work was from a DataQuest tutorial on pandas concatenation
https://www.dataquest.io/blog/pandas-concatenation-tutorial/
Emphasis wasn't placed on organizing the work below before checking into git; just documenting.

Notes from end of tutorial: 
    
pd.concat() function: the most multi-purpose and can be used to combine multiple DataFrames along either axis.
DataFrame.append() method: a quick way to add rows to your DataFrame, but not applicable for adding columns.
pd.merge() function: great for joining two DataFrames together when we have one column (key) containing common values.
DataFrame.join() method: a quicker way to join two DataFrames, but works only off index labels rather than columns.

se axis=0 to apply a method down each column, or to the row labels (the index).
Use axis=1 to apply a method across each row, or to the column labels.

'''



import pandas as pd
import matplotlib.pyplot as plt

na = pd.read_csv('./north_america_2000_2010.csv', index_col='Country')
sa = pd.read_csv('./south_america_2000_2010.csv', index_col=0)

#put the two dataframes together so we can view plot at once:
a = pd.concat([na,sa], axis=0, join='outer', ignore_index=False)

# now let's pull in newer data from more recent years
adf = [a]

for year in range(2011,2016):
    filename = "./americas_{}.csv".format(year)
    df = pd.read_csv(filename, index_col=0)
    adf.append(df)

# update americas dataframe to include most recent years
a = pd.concat(adf, axis=1, sort=False)
a.index.names = ['Country']
print("we have americas \n\n",a)

# plot the americas
#a.transpose().plot(title="avg labor/year")


#  add in rest of world

asia = pd.read_csv('./asia_2000_2015.csv', index_col=0)
#print(asia)
#asia.transpose().plot(title="asia labor/year")
#plt.show()

europe = pd.read_csv('europe_2000_2015.csv', index_col='Country')
#print(europe)
#europe.transpose().plot()

sp = pd.read_csv('./south_pacific_2000_2015.csv', index_col=0)
#sp.transpose().plot()

world = a.append([asia, europe,sp])
world.index

#world.transpose().plot()

#world.transpose().plot(figsize=(15,10), colormap='rainbow', title='Average Labor Hours Per Year')
#plt.legend(loc='right', bbox_to_anchor=(1.3,0.5))
#plt.show()


historical = pd.read_csv('./historical.csv',index_col=0)
print(historical.head())

#now merge our world and historical into whm (m=merge)
whm = pd.merge(historical,world,left_index=True, right_index=True, how='right')

#try another method of joining into whj (j=join)
whj = historical.join(world,how='right')

whj.sort_index(inplace=True)

whj.transpose().plot(figsize=(15,10), colormap='rainbow', title='Average Labor Hours Per Year')
plt.legend(loc='right', bbox_to_anchor=(1.3,0.5))
plt.show()

