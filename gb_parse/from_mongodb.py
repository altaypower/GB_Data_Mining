"""Inserting df from MongoDB"""
import pymongo
from pymongo import MongoClient
import os

client = MongoClient('localhost', 27017)
db = client["gb_parse_16_02_2021"]
collection = db.GbHHItem

cursor = collection.find()
dataframe = (list(cursor))

import pandas as pd
df=pd.DataFrame.from_dict(dataframe)
df=df.drop(columns='_id')
df_clear = df.drop_duplicates(subset=['url'], keep='first')

print(df)

path='/home/fn/anaconda3/HH_df/'
df.to_csv(os.path.join(path,r'vacansy.csv'))



