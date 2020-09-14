from pandas_datareader import data as web
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from Dataminer2 import daten_kompilieren



#hier kann der zu ladene Zeitraum bestimmt werden 
start = dt.datetime(2020, 1, 1)
ende = dt.datetime(2020, 9, 6)

#hier wird die yahoo WKN eingegeben 
df = web.DataReader('TSLA', 'yahoo', start, ende)

print(df.head())


#speichern der Datein als Excel (je nach Kennung anderes Dateinformat)
df.to_csv("tesla.csv", sep=';')

#hier wird die Datein wieder eingelesen 
df = pd.read_csv("tesla.csv", sep=";")

# dieser Block ist zum plotten der Daten und bestimmt das Aussehen 
df['Adj Close'].plot()
plt.grid(True)
style.use('ggplot')
plt.show()

#roling window für befehle mean() = Mittelwert max() min() median() 
df['100ma'] = df['Adj Close'].rolling(window = 100, min_periods = 0).mean()
df.dropna(inplace=True) # nimmer die NaN raus

print(df.head())

#bau der Subplots mit dem Volumen
ax1=plt.subplot2grid((6,1),(0,0),rowspan=5, colspan=1)
ax2=plt.subplot2grid((6,1),(5,0),rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.plot(df['Adj Close'],color="g")
plt.xlabel('Time[d]')
plt.ylabel('Price[USD]')

plt.show()

#anzeige statistischer Werte anhand des DF
print(df.describe())

#Vorhersage 
df = df.filter(items=['Date','Close'])

df.set_index('Date', inplace=True)

df.sort_index(ascending=True, inplace=True)
print(df.head())

for i in range(5):
    i = i + 6
    df.loc[:,('Close-' + str(i))] = df.Close.shift(i)


df.dropna(inplace=True) # nimmer die NaN raus

features = np.array(df.drop(['Close'], 1))

labels = np.array(df.filter(items=['Close']))

features = preprocessing.scale(features)

features_train, features_test, labels_test, labels_train = train_test_split(features, labels, test_size=0.2)

linear_classifier = LinearRegression()
linear_classifier.fit (features_train, labels_train)

score = linear_classifier.score(features_test, labels_test)
print(score)