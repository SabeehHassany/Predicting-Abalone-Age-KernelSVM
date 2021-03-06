# -*- coding: utf-8 -*-
"""kernel_svm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uXJ923AZFn4mk1Nc1-uFblIFkJuzZstG

# Kernel SVM
Support Vector Machines work on a similar basis as support vector regression, using support vectors to create an accurate projection of the data. However, for classification, we can use a radial basis function kernel which can give us very accurate and granular distances by finding the sigma of the kernel and classifying points that way. This is a computational biology dataset that consists of a set of variables that help predict the age of abalone sen snails (a tedious process normally done by cracking open their shells and measuring the ring formation on the inside.

### Importing the libraries
These are the three go to libraries for most ML.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""### Importing the dataset
I imported the dataset through Pandas dataframe then using iloc assign everything besides the last column as our independent variable(s) or X and the last column as our dependent variable or Y. The name of the dataset has to be updated and it must be in the same folder as your .py file or uploaded on Jupyter Notebooks or Google Collab.

For this specific dataset, because we are  predicting the age of the abalones (which is a continous value) we have to categorize the ages and then convert it into a string dtype because the classifier cannot interpret categories as columns of data.
"""

ds = pd.read_csv('abalone.csv')
category = pd.cut(ds.iloc[:, -1],bins=[0,8,16,24],labels=['A','B','C'])

ds.insert(9,'Range',category)
ds['Range'] = ds['Range'].astype(str)

X = ds.iloc[:, :-2].values
y = ds.iloc[:, 9].values

"""#### OneHot
Here, we have OneHotEncode the first row which is the abalone gender.
"""

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0])], remainder='passthrough')
X = ct.fit_transform(X)

"""### Splitting the dataset into the Training set and Test set
Here I used a normal 80/20 test size and also assign 'random_state' to 0 for consistency.
"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

"""### Feature Scaling
We can feature scale our data to make it easier for our model to train on our data and give us accurate results that aren't shifted by the presence of extreme outliers. It's not necessary, but helpful for getting more accurate results.
"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""### Training the Kernel SVM model on the Training set
In most cases, rbf kernel grants the best results but due to the linear nature of our data a linear kernel works better.
"""

from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = None)
classifier.fit(X_train, y_train)

"""### Predicting the Test set results
This is used the X_test to predict our abalone age and then comparing the prediction and actual age group in a concatenated print.
"""

y_pred = classifier.predict(X_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

"""## Confusion Matrix
The confusion matrix is a useful metric for classification models to allow us to visualize the correct positive, false positive, false negative, and correct negative predictions as well as a ultimate accuracy score on the bottom. Because we have three categories, the  confusion matrix has an added degree but the accuracy is still an impressive 80%!
"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accs = accuracy_score(y_test, y_pred)
print(accs)