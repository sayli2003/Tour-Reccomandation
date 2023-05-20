from sklearn.tree import DecisionTreeClassifier 
from pandas.io.pytables import DataCol 
from sklearn.model_selection import train_test_split  
from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
import numpy as nm   
import matplotlib.pyplot as mtp  
import pandas as pd  

def R_Admin(From_City,From_State,Dest,days,season,budget):
  # importing libraries  
  import numpy as nm   
  import matplotlib.pyplot as mtp  
  import pandas as pd  
  
  #importing datasets  
  data_set= pd.read_csv('static\DataBase - AdminRecommendation (1).csv')  
  Selling=[]
  for i in data_set["Num_Sold"]:
    if(20<=i and i<35):
      Selling.append("Not Good")
    elif(35<=i and i<50):
      Selling.append("Satisfactory")
    elif(50<=i):
      Selling.append("Excellent")
  data_set["Selling"]= Selling
  
  
  label_encoder = preprocessing.LabelEncoder()
  x_test=[-1]*9
  x_test[0]=0
  x_test[1]=From_City
  x_test[2]=From_State
  x_test[3]=Dest
  x_test[4]=days
  x_test[5]=season
  x_test[6]=budget
  x_test[7]=0
  x_test[8]='None'
  data_set.loc[len(data_set.index)] = x_test
  data=data_set.apply(label_encoder.fit_transform)
  x= data.iloc[:, 1:7].values  
  y= data.iloc[:, 8].values  

  # Splitting the dataset into training and test set.  
  x_test=x[len(x)-1]
  x=x[0:len(x)-1]
  y=nm.delete(y, len(y)-1)
  x_train=x
  y_train=y

  #Fitting Decision Tree classifier to the training set  
  from sklearn.tree import DecisionTreeClassifier  
  classifier= DecisionTreeClassifier(criterion='entropy', random_state=0)  
  classifier.fit(x_train, y_train)  
  
  #Predicting the test set result  
  y_pred= classifier.predict([x_test]) 

  y_pred=label_encoder.inverse_transform(y_pred)
  print("Package is")
  print(y_pred)
  return y_pred[0]



