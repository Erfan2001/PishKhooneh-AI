import numpy as np
import pandas as pd
from pandas import json_normalize
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# --------------------------  Kilid DB   ---------------------------------
with open('Files/Kilid.json','r', encoding='utf-8') as json_file:
    kilid = json.load(json_file).get('data')
kilid_df = json_normalize(kilid)
# --------------------------  Melkana DB   ---------------------------------
with open('Files/Melkana.json','r', encoding='utf-8') as json_file:
    Melkana = json.load(json_file).get('data')
Melkana_df = json_normalize(Melkana)
# --------------------------  Shabesh DB   ---------------------------------
with open('Files/Shabesh.json','r', encoding='utf-8') as json_file:
    Shabesh = json.load(json_file).get('data')
Shabesh_df = json_normalize(Shabesh)
# --------------------------  Sheypoor DB   ---------------------------------
with open('Files/Sheypoor.json','r', encoding='utf-8') as json_file:
    Sheypoor = json.load(json_file).get('data')
Sheypoor_df = json_normalize(Sheypoor)
# --------------------------  Divar DB   ---------------------------------
with open('Files/Divar.json','r', encoding='utf-8') as json_file:
    divar = json.load(json_file).get('data')
divar_df = json_normalize(divar)
# --------------------------  Get all neighbors   ---------------------------------
with open('Predict_Crawler_Ganj/neighbors.json','r', encoding='utf-8') as json_file:
    neighbors = json.load(json_file).get('neighbourhoods')
# Join these data from different websites
all_df=pd.concat([kilid_df,Melkana_df,Shabesh_df,Sheypoor_df,divar_df])
# Predict on just 200 top neighbors
consider_neighbors=all_df['neighborhood'].value_counts()[:200]
new_df=all_df[all_df['neighborhood'].isin(consider_neighbors.index)]
# Use only some features to predict
new_df=new_df[['neighborhood','area','price','year','room']]
new_df=new_df[new_df['year'].notna()]
# Get total available neighbors in database of Ganj
totalAvailableNeighbors=[]
for item in neighbors:
    totalAvailableNeighbors.append(item.get('name'))
new_df=new_df[new_df['neighborhood'].isin(totalAvailableNeighbors)]
# Remove NAN values
new_df.dropna(inplace=True)
new_df.reset_index(inplace=True)
# Separate just some of records which are in common with list of total available neighbors and replace with their id
for index,item in enumerate(new_df['neighborhood']):
    for new_item in neighbors:
        if new_item.get('name') == item:
            new_df.at[index,'neighborhood'] = new_item.get('id')
# Get X & Y for prediction
x = np.asanyarray(new_df[new_df.columns.difference(['price'])])
y = np.asanyarray(new_df['price'])
# Split train & test dataset
x_train, x_test, y_train, y_test = train_test_split( x, y, test_size=0.3, random_state=4)
# Use random forest algorithm for prediction
reg = RandomForestRegressor(random_state=2)
reg.fit(x_train, y_train)
# Test our dataset
y_pred = reg.predict(x_test)
# Find score  84... % :)
print(r2_score(y_test, y_pred))
