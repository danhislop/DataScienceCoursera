#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:14:05 2019

@author: danhi
"""
import pandas as pd

# Read in the two files but call the data old and new and create columns to track
old = pd.read_excel('pandasdiff.sample-address-1.xlsx', 'Sheet1', na_values=['NA'])
new = pd.read_excel('pandasdiff.sample-address-2.xlsx', 'Sheet1', na_values=['NA'])
old['version'] = "old"
new['version'] = "new"


old_accts_all = set(old['account number'])
new_accts_all = set(new['account number'])

dropped_accts = old_accts_all - new_accts_all
added_accts = new_accts_all - old_accts_all

all_data = pd.concat([old,new],ignore_index=True)

# keep='last' means when you find a duplicate, keep one of them (the last one).  
# therefore the resulting list isn't really a list of non-duplicates.  it's a cleaned and complete list
# including lines with changes and some without
#--------------------------------------------------------------------------------------------------------------
#------------------------------ I could use this to compare a userlist to term list ---------------------------
#--------------------------------------------------------------------------------------------------------------
changes = all_data.drop_duplicates(subset=["account number","name","street","city","state","postal code"], keep='last')

# testing keep=False.  this kept ONLY the non-duplicates.  really a list of changed lines. (naming here is faulty)
#--------------------------------------------------------------------------------------------------------------
#--------------------------------i could use this to compare a userlist to a census ---------------------------
#--------------------------------------------------------------------------------------------------------------
falsedrop = all_data.drop_duplicates(subset=["account number","name","street","city","state","postal code"], keep=False)

#dupe_accts creates a python LIST of account numbers that are duplicated on the dataframe called 'changes'
dupe_accts = changes[changes['account number'].duplicated() == True]['account number'].tolist()

# dupes then looks through dataframe 'changes' and returns all lines where account number matches the list dupe_accounts
# this ends up returning the same thing as falsedrop
dupes = changes[changes["account number"].isin(dupe_accts)]


# Pull out the old and new data into separate dataframes
change_new = dupes[(dupes["version"] == "new")]
change_old = dupes[(dupes["version"] == "old")]

# Drop the temp columns - we don't need them now
change_new = change_new.drop(['version'], axis=1)
change_old = change_old.drop(['version'], axis=1)

# Index on the account numbers
change_new.set_index('account number', inplace=True)
change_old.set_index('account number', inplace=True)

# Combine all the changes together  DAN work on these concat options
df_all_changes = pd.concat([change_old, change_new],
                            axis='columns',
                            keys=['old', 'new'],
                            join='outer')

def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

df_all_changes = df_all_changes.swaplevel(axis='columns')[change_new.columns[0:]]
df_changed = df_all_changes.groupby(level=0, axis=1).apply(lambda frame: frame.apply(report_diff, axis=1))
df_changed = df_changed.reset_index()

df_removed = changes[changes["account number"].isin(dropped_accts)]
df_added = changes[changes["account number"].isin(added_accts)]

output_columns = ["account number", "name", "street", "city", "state", "postal code"]
writer = pd.ExcelWriter("my-diff.xlsx")
df_changed.to_excel(writer,"changed", index=False, columns=output_columns)
df_removed.to_excel(writer,"removed",index=False, columns=output_columns)
df_added.to_excel(writer,"added",index=False, columns=output_columns)
writer.save()