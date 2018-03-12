import  csv
import pandas as  pd
import math
import numpy as np
c=0

df1 = pd.read_csv("cric_espn_dataset6th_odi.csv")
df =pd.read_csv("cricket_dataset_6th_odi.csv")

batting_val1 = list(df1["Batting_area"])
batting_val = list(df["Batting_area"])
bowling_val1 = list(df1["Bowling_area"])
bowling_val = list(df["Bowling_area"])
result = list(df1["Result"])

for each in batting_val1:
    try:
        if "empty" in each:
            batting_val1[c] = batting_val[c]
            
            
    except:
        print("error")

    c+=1    
d=0
for each in bowling_val1:
    try:
        if "empty" in each:
            bowling_val1[d] = bowling_val[d]
    except:
        print("error")

    d+=1    


dataframe = pd.Series(batting_val1)
dataframe1 = pd.Series(bowling_val1)

print(dataframe)
df1["Batting_area"] = dataframe
df1["Bowling_area"] = dataframe1

df1.to_csv('cric_espn_dataset6th_odi.csv', index=False)
