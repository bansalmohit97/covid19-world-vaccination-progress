# Project Name: Covid Vaccination World Progress
# Created by: Mohit Bansal
# Created On: 2021-08-11

#Importing libraries
import numpy as np
import pandas as pd
import pyodbc
import time
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


#Conection to Windows Authenticated SQL Server
server = 'DESKTOP-FR8RFRB\SQLEXPRESS01'
database = 'DSTraining'
cnxn = pyodbc.connect(r'Driver=SQL Server;Server='+server+';Database='+database+';Trusted_Connection=yes;')
cursor = cnxn.cursor()

#Calling Objects from the two SQL tables
df_daily_object = pd.DataFrame(cursor.execute(
    "SELECT * FROM WRK_CovidVacinated_Daily"
))

df_weekly_object = pd.DataFrame(cursor.execute(
    "SELECT * FROM WRK_CovidVacinated_Weekly"
))

#Creating empty Data Frames
df_daily_columns = [
    "RowNumber",
    "country",
    "iso_code",
    "date",
    "daily_vaccinations_expected",
    "daily_vaccinations",
    "daily_vaccinations_per_million",
    "vaccines",
    "source_name",
    "source_website"
]
df_daily = pd.DataFrame(columns=df_daily_columns)

df_weekly_columns = [
    "RowNumber",
    "country",
    "iso_code",
    "date",
    "total_vaccinations",
    "people_vaccinated",
    "people_fully_vaccinated",
    "total_vaccinations_per_hundred",
    "people_vaccinated_per_hundred",
    "people_fully_vaccinated_per_hundred",
    "vaccines",
    "source_name",
    "source_website"
]
df_weekly = pd.DataFrame(columns=df_weekly_columns)

#Since, the DF typecast for object of both the tables has just a single row, so using loop in order to
#export each row into the respective Dataframes
#DF1: df_daily_object
for i in range(0, len(df_daily_object[0])):
    df_daily_series = pd.Series(list(df_daily_object[0][i]), index=df_daily.columns)
    df_daily = df_daily.append(df_daily_series, ignore_index=True)
#DF2: df_weekly_object
for i in range(0, len(df_weekly_object[0])):
    df_weekly_series = pd.Series(list(df_weekly_object[0][i]), index=df_weekly.columns)
    df_weekly = df_weekly.append(df_weekly_series, ignore_index=True)

#Since, the columns in df_weekly Dataframe are all dependent on the columns in df_daily DF, so using a left
#join will just result in an increase in time consumption since, the covariance will be huge
#resulting in a negatice effect with the response

#Keeping the predictors and response from the dataset
df_daily_original = df_weekly[['country', 'date', 'total_vaccinations']]

#Saving the above dataframe into a csv to avoid processing time every time I run the program
df_daily_original.to_csv('df_daily_original', index=False)


#Reading the csv file into a dataframe
df_daily_original = pd.read_csv('df_daily_original.csv')

#Data Preprocessing
#1. Conversion of date to year, month, day separate columns
split_funcY = lambda x: int(x['date'].split('-')[0])
split_funcM = lambda x: int(x['date'].split('-')[1])
split_funcD = lambda x: int(x['date'].split('-')[2])
df_daily_original['year'] = df_daily_original.apply(split_funcY, axis=1)
df_daily_original['month'] = df_daily_original.apply(split_funcM, axis=1)
df_daily_original['day'] = df_daily_original.apply(split_funcD, axis=1)

del df_daily_original['date']

#2. Data Encoding for the 'country' column: A total of 219 countries
encode_country = preprocessing.LabelEncoder()
df_daily_original['country_encoded'] = encode_country.fit_transform(df_daily_original['country'])

#Creating a datframe with the needed columns
df_actual = df_daily_original[['country_encoded', 'year', 'month', 'day', 'total_vaccinations']]
#print(df_actual)

#Creating a correlatio matrix
print(df_actual.corr())

#Train - Test Split
df_test = df_actual[(df_actual['month'] == 7) & (df_actual['day'] > 18)]
df_train = df_actual[(df_actual['month'] != 7) | ((df_actual['month'] == 7) & (df_actual['day'] <= 18))]

#Shuffle dataframes
df_train = df_train.sample(frac = 1)
df_test = df_test.sample(frac = 1)

#Since, the reponse variable is a continous integer vriable, applying a basic Linear Regression Model to predict the vaccinations for the month of July
#Model creation
lrmodel = LinearRegression()

#Model Fit
X_train = df_train[['country_encoded', 'month', 'day']]
Y_train = df_train['total_vaccinations']
lrmodel.fit(X_train, Y_train)

#Model Results
print(lrmodel)

#Model Prediction on Test
X_test = df_test[['country_encoded', 'month', 'day']]
Y_test = df_test['total_vaccinations']
predicted_dv = lrmodel.predict(X_test)
df_test = df_test.assign(predicted_total_vaccinations = list(predicted_dv))
#print(df_test.columns)

#Model Accuracy & Result - CAP Curve

rmse_result = np.sqrt(np.mean(np.square(df_test['predicted_total_vaccinations'] - df_test['total_vaccinations'])))
print('Root Mean Square Error:', rmse_result)

adjusted_r_square = 1 - (1-lrmodel.score(X_train, Y_train))*(len(Y_train)-1)/(len(Y_train)-(X_train.shape[1])-1)
print('Adjusted R square:', adjusted_r_square)

#print(df_test[['total_vaccinations','predicted_total_vaccinations']].head(15))

#Plot of true vs predicted values
plt.figure(figsize=(10, 10))
plt.scatter(df_test['total_vaccinations'], df_test['predicted_total_vaccinations'], color='g')
plt.xlabel('True Value')
plt.ylabel('Predicted Values')

plt.show()

'''
INSIGHTS FROM PLOT:
The plot displays that for the smaller values for the true daily vaccinations, the model still predicts the 
values to be really large. One such explanation of this can be for some countries there might not be any data 
in the training dataset so, the model couldn't predict from the past data. 

Also, since, the predictors were not very great with correlating with the response variable, the model turned
out to be really poor. Hence, we need more predictors to model the response variable.

Conclusion: Data Modelling can't be performed on such a small dataset with predictors not at all related
to the response variable.
'''
