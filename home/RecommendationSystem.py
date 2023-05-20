import numpy as np
import pandas as pd
from apyori import apriori
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

def RecSystem(CID):  
  # importing databases
  if CID>39:
    return []
  df = pd.read_csv('static\DataBase - Apriori.csv')
  # Converting into list
  df.values.tolist()


  #Creating list of transactions 
  transacts = []
  for i in range(len(df)):
    transacts.append([int(df.values[i,j]) for j in range(0,12) if str(df.values[i,j])!='nan'])	# Removing nan values

  # Generate association rules from the frequent itemsets
  rule = apriori(transactions=transacts, min_support=0.1, min_confidence=0.5, min_lift=1.1, min_length=2)
  result=list(rule)	 # Creating list of generated rules


  #let
  hist = []	
  for i in range(0,12):	# Creating list of history of given CID
    if str(df.values[CID,i])!='nan': # Removing nan values
      hist.append(int(df.values[CID,i]))

  print("CID: ",CID)
  sugg = []
  for item in result:
    item1=item
    pair=item[0]
    item=[x for x in pair]	# Creating item list from pair
    if int(item[0]) in hist:	# check if rule item is in hist of given CID
      # append only if Recommendation does not already exist
      if int(item[1]) not in sugg:	
          sugg.append(int(item[1]))
  # Printing recommendations
  print(sugg)
  return sugg

def R_System(CID):
  # importing database
  if CID>25:
    return []
    
  package_df=pd.read_csv('static\DataBase - knn-USETHIS SearchHist.csv',usecols=['CID', 'PID', 'Rating'],
    dtype={'CID': 'int32', 'PID': 'int32', 'Rating': 'float32'})
  package_df.head()
  
  # Eliminating NAN values
  package_df = package_df.dropna(axis = 0, subset = ['PID'])
  # Grouping dataset by PID and adding rating count
  package_ratingCount = (package_df.
     groupby(by = ['PID'])['Rating'].
     count().
     reset_index().
     rename(columns = {'Rating': 'totalRatingCount'})
     [['PID', 'totalRatingCount']]
    )
  package_ratingCount.head()


  # Joining tables
  rating_with_totalRatingCount = package_df.merge(package_ratingCount,  left_on = 'PID', right_on = 'PID', how = 'left')
  rating_with_totalRatingCount.head()
  pd.set_option('display.float_format', lambda x: '%.3f' % x)


  # Considering packages with totalRatingCount equal or greater than 3
  popularity_threshold = 3
  rating_popular_package= rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
  rating_popular_package.head()
  
  # First lets create a Pivot matrix
  package_features_df=rating_popular_package.pivot_table(index='PID',columns='CID',values='Rating').fillna(0)
  package_features_df.head()
  
  package_features_df_matrix = csr_matrix(package_features_df.values)

  
  # Using cosine matrix and brute algo for NearestNeighbors
  model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
  model_knn.fit(package_features_df_matrix) # fitting data into the model
  max_rating = package_features_df.max()
 
  
  PID = package_features_df.index
  # Getting max rated package of given customer
  x = package_features_df.index[package_features_df[CID] == max_rating[CID]]
  # Getting ID of Package
  for i in range(len(PID)):
    if x[0] == PID[i]:
      query_index = i
  # Creating Knn model with k=6
  distances, indices = model_knn.kneighbors(package_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 6)
  print("CID: ",CID)
  sugg = []
  for i in range(0, len(distances.flatten())):
    if i == 0:	# To skip first row as it is the value itself
      print('Recommendations for {0}:\n'.format(package_features_df.index[query_index]))
    else:
	  # Appending Suggestions to list
      sugg.append(package_features_df.index[indices.flatten()[i]])
  return sugg



