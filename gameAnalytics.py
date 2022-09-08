from asyncio.windows_events import NULL
from datetime import datetime
from enum import unique
from itertools import count
from msilib import sequence
from operator import indexOf
from pickle import TRUE
from matplotlib.pyplot import title
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

from dateutil import parser
import datetime

gameDataset = "steam_games.json"


def parse(path):
    g = open(path, 'r', encoding="utf-8")
    for l in g:
        yield eval(l)


f = []


for row in parse(gameDataset):
    f.append(row)

df = pd.DataFrame(f)

df["title"] = df["title"].fillna(df.pop("app_name"))

# used the url for the associated row to find the name of the item and entering
df.at[2580, "title"] = "Duet"

df = df.drop(df[df["release_date"].isnull()].index)
df = df.reset_index()

#print(df[df["release_date"] != "Soon.."].index)

# df = df.drop(index=74)  # removing the row that is full of NaN values
# df = df.reset_index()  # resetting the index values since I took out a row

#print(df[df["release_date"] == "Beta\u6d4b\u8bd5\u5df2\u5f00\u542f"].index)
#df = df.drop(df[df["tags"].isnull()].index)
#df = df.reset_index()

idx = []
for i in range(len(df)):
    item = df.loc[i]
    # print(type(item["tags"]))
    try:
        if("Movie" in item["tags"]):
            idx.append(i)
        elif("Documentary" in item["tags"]):
            idx.append(i)
            #df = df.drop(index=i)
  #          print(i)
 #           print(item["title"])
    except:
        continue

df.drop(index=idx)

df = df.drop(df[df["tags"].isnull()].index)

df = df.drop(df[df["release_date"] == "Soon.."].index)
df = df.drop(index=36)
df = df.drop(df[df["release_date"] == "Coming Soon"].index)
df = df.drop(df[df["release_date"] == "Q2 2017"].index)
df = df.drop(df[df["release_date"] == "TBA"].index)
df = df.drop(df[df["release_date"] == "When it's done"].index)
df = df.drop(df[df["release_date"] == "coming soon"].index)
df = df.drop(df[df["release_date"] == "Q2 2018"].index)
df = df.drop(df[df["release_date"] == "Q1 2018"].index)
df = df.drop(df[df["release_date"] == "Winter 2017"].index)
df = df.drop(df[df["release_date"] == "Fall 2017"].index)
df = df.drop(df[df["release_date"] == "soon"].index)
df = df.drop(df[df["release_date"] == "Summer 2017"].index)
df = df.drop(df[df["release_date"] == "Spring 2018"].index)
df = df.drop(df[df["release_date"] == "Winter 2018"].index)
df = df.drop(df[df["release_date"] == "To be Announced"].index)
df = df.drop(df[df["release_date"] == "TBD"].index)

#    df[df["release_date"] == "BetaBeta\u6d4b\u8bd5\u5df2\u5f00\u542f"].index)
df = df.reset_index()

tags = []
for i in range(len(df)):
    game = df.loc[i]
    tags += game["tags"]

t2 = pd.Series(tags)
# print(t2.unique())
t3 = t2.unique()
print(t3[0])
t4 = [0] * len(t3)

t5 = []
for tag in t3:
    t5.append(tag)

for tag in t2:
    t4[t5.index(tag)] += 1

orderedTags = []
orderedCount = []
for i in range(len(t4)):
    orderedTags.append(t5[t4.index(max(t4))])
    orderedCount.append(max(t4))
    t5.remove(t5[t4.index(max(t4))])
    t4.remove(max(t4))

print(orderedCount[0:9])
print(orderedTags[0:9])
print(len(t2.unique()))
dates = []
for i in range(len(df)):
    # print(df.loc[i]["release_date"])
    if len(df.loc[i]["release_date"]) != 4:
        try:
            dates.append(parser.parse(df.loc[i]["release_date"]).date())
        except:
            continue
    else:

        temp = "{0}-01-01".format(df.loc[i]["release_date"])
        try:
            dates.append(parser.parse(temp).date())
        except:
            continue
#print(dates[1: 10])
# print(dates[1])
# print(dates.year)
years = []
for date in dates:
    years.append(date.year)

print(years[1:5])
years2 = np.array(years)
# print(np.unique(years2))

years = list(i for i in years if i >= 2003 and i <= 2017)
print(min(years))
temp = pd.Series(years)
print(temp.unique())
plt.bar(orderedTags[0:9], orderedCount[0:9])
plt.title('top 10 tags')
plt.xticks(rotation=45, ha='right')
plt.show()

plt.hist(years, bins=len(temp.unique()))
plt.title('Game releases across the years 2003 - 2017')
plt.show()

#np.histogram(years2, bins=5)
#sequence(min(years2), max(years2), 5)
# plt.bar(xAxis,yAxis)
#plt.xlabel('xAxis name')
#plt.ylabel('yAxis name')
# plt.show()
