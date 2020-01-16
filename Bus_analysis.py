# -*- coding: utf-8 -*-

#Cleaning data and visualizing 

"""
Created on Sat Nov 16 11:09:51 2019

@author: Tisi
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Bus_Breakdown_and_Delays.csv', thousands=',')

#check the data
dataset.head(10)

#get column names
column_names = dataset.columns
print(column_names)

# check data information
print(dataset.info())

# Also check if the column is unique
for i in column_names:
  print('{} is unique: {}'.format(i, dataset[i].is_unique))

# Check the index values
dataset.index.values

# Exctract information I want to keep 
delay_info = dataset[['How_Long_Delayed',
                      'Breakdown_or_Running_Late',
                      'School_Year', 
                      'Run_Type',
                      'Bus_No',
                      'Route_Number',
                      'Reason',
                      'Occurred_On',
                      'Boro',
                      'Bus_Company_Name',
                      'School_Age_or_PreK',
                      'Number_Of_Students_On_The_Bus'
                      ]]

#cleaning data 
# dealing with missing value
delay_info.info()
# first check data on buses being delayedthat are running late or brokendown
np.logical_and(delay_info['How_Long_Delayed'].isnull(), delay_info['Breakdown_or_Running_Late'] =='Running Late').sum().sum()
np.logical_and(delay_info['How_Long_Delayed'].isnull(), delay_info['Breakdown_or_Running_Late'] =='Breakdown').sum().sum()
delay_info['How_Long_Delayed'].isnull().sum().sum() #most of missing data are for buses that had a breakdown, 
#according to record these buses did not make a trip, another bus was required to send in its place

#drop missing data from 'how long bus delayed' and all other missing data - for this exercise
delay_info.dropna(inplace = True)

#fix index after dropping some values
delay_info.reset_index(inplace = True, drop= True) 

# cleaning the delayed time variable
delay_info['How_Long_Delayed'].value_counts()


# Cleaning How_Long_Delayed as it is string entries and have different variations of data
delayed_str = delay_info["How_Long_Delayed"].values
trial = ["-", ":\", hr", "min", "/"]
for t in trial:
    matching = [s for s in delayed_str if t in str(s)]
    print(matching[0:10])

import re
sub_data = delay_info.iloc[511,0]
delayed = re.split('([0-9]+)', sub_data)
df = pd.DataFrame(np.array(delayed).reshape(-1,len(delayed)))



data = []
for i in range(0, 320442):
    delayed = re.split('([0-9]+)', delay_info['How_Long_Delayed'][i])
    data.append(delayed)
    
data = pd.DataFrame(np.array(data))
data = data.rename(columns ={0: 'time'}) 

data = pd.DataFrame(data.time.values.tolist(), index= data.index)



#(^[0-9]+[-:\/]*[0-9]*)'

#create dictionary for data type convert the data type to correct format
data_type = {
    "category":["Breakdown_or_Running_Late", 
                "School_Year", "Run_Type", 
                "Bus_No", "Route_Number", 
                "Reason", "Boro", 
                "Bus_Company_Name",
                "School_Age_or_PreK"],
    #"float":   ["How_Long_Delayed"], 
    "int":     ["Number_Of_Students_On_The_Bus"],
    "datetime64":["Occurred_On"],
    "object":  []    
}


#Coverting data fomart
for m, col in data_type.items():
    delay_info[col] = delay_info[col].astype(m)
    
print(delay_info.info())


# Visualization
# Reasons for delays
reason = delay_info.groupby("Reason").size()
lth = range(len(reason))
plt.bar(lth, reason)
plt.xticks(lth, reason.index, rotation = 90)
plt.show()


#Time for delays
time_delayed = delay_info.groupby('How_Long_Delayed').size()
lth = range(len(time_delayed))
plt.bar(lth, time_delayed)
plt.xticks(lth, time_delayed.index, rotation = 90)
plt.show()



# Time delays occuring often
delay_time = delay_info.groupby(delay_info["Occurred_On"].map(lambda t: t.hour)).size()
lth = range(len(delay_time))
plt.bar(lth, delay_time)
plt.xticks(lth, delay_time.index, rotation=90)
plt.title("Number of Delays by Hour of the Day")
plt.ylabel("Number of delays reported")
plt.xlabel("Hour of the day")
plt.show()


df = pd.DataFrame(np.array(delayed).reshape(-1,len(delayed)))

for i in range(0, 1000):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    corpus.append(review)


time_delayed = []
for i in range(0, 369237):
    delayed = re.findall('[^0-9]+', '-', delay_info['How_Long_Delayed'][i])
    time_delayed.append(delayed)
