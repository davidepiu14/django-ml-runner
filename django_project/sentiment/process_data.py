import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import ast 
from datetime import datetime as dt
import numpy as np

df_trump=pd.read_csv("tweets_donald_trump.csv",sep=",")
df_biden=pd.read_csv("tweets_joe_biden.csv",sep=",")
df_trump=df_trump.dropna(thresh=2)#rimuove le righe con all'interno almeno 2 NA
df_biden=df_biden.dropna(thresh=2)#rimuove le righe con all'interno almeno 2 NA

def clean_tweet(tweet):
  """"sostituisce con uno spazio vuoto tramite regular esxpression i pattern all'interno delle parentesi"""
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

def prepr(df):
  """ 
  funzione preprocessing dati
  """
  df=df[df['text']!="text"]
  df['text'] = df['text'].apply(clean_tweet)
  df.drop(df.columns[7:], axis=1, inplace=True)
  df=df.loc[2:]
  df=df.dropna(thresh=3)
  df=df[df['sentiment'].str.startswith('{')]
  df['sentiment']=df['sentiment'].apply(ast.literal_eval)
  df=pd.concat([df.drop(['sentiment'], axis=1), df['sentiment'].apply(pd.Series)], axis=1)
  
  return df 
    
df_trump=prepr(df_trump)
df_biden=prepr(df_biden)

df_biden['candidato'] = 'biden'
df_trump['candidato'] = 'trump'

a = pd.DataFrame(df_biden.groupby('sign').size()/df_biden['sign'].count()*100)

# aggiunta colonna con percentuali tweet negativi, positivi, neutrali  trump
a['trump']=df_trump.groupby('sign').size()/df_trump['sign'].count()*100
a.columns=['biden','trump']
a.to_csv('data_for_pie.csv')#salvo i dati in un csv che utilizzerò per i grafici
df=pd.concat([df_trump, df_biden], ignore_index=True)


df['new_date_column'] = pd.to_datetime(df['date_tweet'],errors='coerce').dt.date
#raggruppo per data e candidato
g = df.groupby(["candidato", "new_date_column"])
#media giornaliera di polarity giornaliera per candidato
daily_averages = g.aggregate({"polarity":np.mean})
#converto in un dataframe
daily_averages=pd.DataFrame(daily_averages)
daily_averages.to_csv('media_polarity.csv', index = True)
df=pd.read_csv("media_polarity.csv")

#rimodello il dataset creato, l'indice è la data, le colonne sono i nomi dei candidati e all'interno delle celle troviamo la media giornaliera di polarity
df=df.pivot(index='new_date_column', columns='candidato', values='polarity')
#visualizzo media polarity
df.to_csv('media_polarity.csv')