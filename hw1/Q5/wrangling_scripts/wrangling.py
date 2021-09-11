"""
cse6242 s21
wrangling.py - utilities to supply data to the templates.

This file contains a pair of functions for retrieving and manipulating data
that will be supplied to the template for generating the table. """
import csv

def username():
    return 'dhislop3'

def data_wrangling():
    with open('data/movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        table = list()
        # Feel free to add any additional variables
        ...
        
        # Read in the header
        for header in reader:
            break
        
        # Read in each row
        i=0
        for row in reader:
            if i == 100:
                break
            table.append(row)
            #table.append([row[0],row[1],float(row[2])])
            i = i + 1 

            # Only read first 100 data rows - [2 points] Q5.a
            ...

        # Order table by the last column - [3 points] Q5.b
        table.sort(key = lambda i: float(i[2]), reverse=True)

        ...
    
    return header, table

if __name__ == '__main__':
    data_wrangling()
