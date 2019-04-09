#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: dan hislop |  https://github.com/danhislop | hislopdan@gmail.com
Created on Wed Apr  3 19:41:50 2019
The following is my work, in response to Data Visualization class questions
"""

## Test Question 1: Use the pandas read_csv method to read the csv file into a pandas dataframe, matching specifications
import pandas as pd

filepath = '/anaconda3/Topic_Survey_Assignment.csv'  #can be downloaded from filepath = 'https://cocl.us/datascience_survey_data'
survey = pd.read_csv(filepath, index_col=0)
print('\n Show if there are any nulls in the dataset? \n')
print(survey.isna().sum())

# Sort, and replace total count values by percentage values
survey.sort_values(by='Very interested', inplace=True, ascending=False)
total_respondents = 2233  #this value was given 
for column in survey:
    survey[column] = round(survey[column]/total_respondents, 2)

print('\n Show the dataset with values changed to percentage and sorted by Very Interested \n')
print(survey)

# Test Question 2: Use the artist layer of Matplotlib to visualize the percentage
# must match visual specifications given for label value/location, borders, and backgrounds

# Setup a bar chart 
ax = survey.plot(kind='bar', 
                 figsize=(20,8),
                 width=0.8,
                 fontsize=14,
                 color=['#5cb85c', '#5bc0de', '#d9534f'])

ax.set_title("Percentage of Respondents' Interest in Data Science Areas", fontsize=16)

# Remove top, left, right borders, and set on white background
ax.patch.set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# to prepare for labels, bring all the values from dataframe into one list; convert to string and add % symbol
values = survey.iloc[:,0].tolist() + survey.iloc[:,1].tolist() + survey.iloc[:,2].tolist()
values = [round(i*100,2) for i in values]
valstring = [str(i)+"%" for i in values]
rects = ax.patches   # creates a list of each patch (bar) in the chart

# for each patch, set location and value of label
for rect, value in zip(rects, valstring):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, value,
            ha='center', va='bottom')
    
    
