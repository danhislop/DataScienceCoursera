#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:23:12 2019
The below work was done for a test in the Machine Learning Class.
Using a set of test data, we classify loan holders based on various factors, to predict who is more likely to default on their loans.
We need to preprocess the data, normalize it, then fit to various classification models

@author: dan hislop |  https://github.com/danhislop | hislopdan@gmail.com
"""

import numpy as np
import pandas as pd
import os
from sklearn import preprocessing
import wget
import warnings
warnings.filterwarnings("ignore")

''' Preprocessing of the Data '''

# Get source file
wget.download(url='https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/loan_train.csv', out='loan_train.csv')
df = pd.read_csv('loan_train.csv')
print('\n The source data looks like: ', df.head())

# Convert string type dates to date time object
df['due_date'] = pd.to_datetime(df['due_date'])
df['effective_date'] = pd.to_datetime(df['effective_date'])

# rather than seven days of the week, club into weekend=1,0
df['dayofweek'] = df['effective_date'].dt.dayofweek
df['weekend'] = df['dayofweek'].apply(lambda x: 1 if (x>3)  else 0)

# Convert categorical features to numerica values
df['Gender'].replace(to_replace=['male','female'], value=[0,1],inplace=True)

# Narrow dataset, and use One Hot Encoding to convert education into binary variables
test_Feature = df[['Principal','terms','age','Gender','weekend']]
test_Feature = pd.concat([test_Feature,pd.get_dummies(df['education'])], axis=1)
test_Feature.drop(['Master or Above'], axis = 1,inplace=True)
print("\n The processed data now looks like: ", test_Feature.head())

#Prepare for Classification by selecting feature sets (X) and labels (y), and normalizing the data '''
X = test_Feature
y = df['loan_status'].values
print("\nMaking sure the shape shows same # of rows:  X has ", X.shape, "and y has --", y.shape, X.shape[0] == y.shape[0])

# Normalize the numbers in the data
X = preprocessing.StandardScaler().fit(X).transform(X)

# Split into train/test:  we'll use 80% to train and 20% for testing
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
print('\nAfter dividing into an 80/20 split for train and test, we have: ')
print ('Train set:', X_train.shape, 'and Test set:', X_test.shape)


''' Now we can classify the Data using several models '''
print("\n\n Now on to classify the data. \n\n")

# Classify using KNN
print("\n--------Using K Nearest Neighbor-------- \n")
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.metrics import f1_score
from sklearn.metrics import jaccard_similarity_score

ks = 10
mean_acc = np.zeros((ks - 1)) # setup an array to store mean accuracy scores
# Try various values of k
for k in range(1,ks): 
    n = KNeighborsClassifier(n_neighbors = k).fit(X_train, y_train)
    
    # Predict the test set
    yhat_kn = n.predict(X_test)
    
    # Evaluate
    mean_acc[k-1] = metrics.accuracy_score(y_test, yhat_kn)

print("the highest accuracy was ", mean_acc.max(), "with k=", mean_acc.argmax()+1)
best_k = mean_acc.argmax()+1
# rerun it with k= mean_acc.argmax()+1 and let that be the one that stands for future predictions

knn = KNeighborsClassifier(n_neighbors = best_k).fit(X_train, y_train)
yhat_knn = knn.predict(X_test)
#print(yhat_knn[0:10], "\n\n", y_test[0:10])


# Check accuracy
print("accuracy score using knn is: ", metrics.accuracy_score(y_test, yhat_knn))
print("f1 score       using knn is: ", f1_score(y_test, yhat_knn, average='weighted'))
print("jaccard score  using knn is: ", jaccard_similarity_score(y_test, yhat_knn))


print("\n--------Using Decision Tree -------- \n")

from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier(criterion="entropy", max_depth = 4)
tree

# Fit and Predict
tree.fit(X_train, y_train)
yhat_tree = tree.predict(X_test)
#print(yhat_tree[0:10], "\n\n", y_test[0:10])

# Check accuracy
print("accuracy score using tree is: ", metrics.accuracy_score(y_test, yhat_tree))
print("f1 score       using tree is: ", f1_score(y_test, yhat_tree, average='weighted'))
print("jaccard score  using tree is: ", jaccard_similarity_score(y_test, yhat_tree))



print("\n--------Using Support Vector Machine (SVM) -------- \n")
# fit the data using SVM, radial basis function
from sklearn import svm
defaults = svm.SVC(kernel='rbf')
defaults

# fit and predict
defaults.fit(X_train, y_train)
yhat_svm = defaults.predict(X_test)
#print(yhat_svm[0:10], "\n\n", y_test[0:10])

# Check accuracy
print("accuracy score using svm is: ", metrics.accuracy_score(y_test, yhat_svm))
print("f1 score       using svm is: ", f1_score(y_test, yhat_svm, average='weighted'))
print("jaccard score  using svm is: ", jaccard_similarity_score(y_test, yhat_svm))


print("\n--------Using Logistic Regression -------- \n")
from sklearn.linear_model import LogisticRegression

#Fit and Train
logr = LogisticRegression(C=0.01, solver='liblinear').fit(X_train, y_train)
yhat_logr = logr.predict(X_test)
yhat_logr

# Check accuracy
print("accuracy score using log reg is: ", metrics.accuracy_score(y_test, yhat_logr))
print("f1 score       using log reg is: ", f1_score(y_test, yhat_logr, average='weighted'))
print("jaccard score  using log reg is: ", jaccard_similarity_score(y_test, yhat_logr))


# Create a summary table of results
print("\n\n The below table summarizes the accuracy of each model, by evaluating with Jaccard and F-1.  Closer to 1 = more accurate \n" )
methods = [yhat_knn,yhat_tree, yhat_svm, yhat_logr]
types = ['knn','tree', 'svm', 'logr']
col_names = ('Algorithm','Jaccard','F1-score')
count = 0
output = pd.DataFrame(columns=col_names)

for method, type in zip(methods, types):
    # evaluate accuracy of each:
    f = f1_score(y_test, method, average='weighted')
    j = jaccard_similarity_score(y_test, method)
    row = [type, f, j]
    output.loc[count] = row  # Add this row to the dataframe called output
    count = count + 1

output.set_index('Algorithm', inplace=True)
print(output)
