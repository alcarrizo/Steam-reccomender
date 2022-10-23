from asyncio.windows_events import NULL
from itertools import count
from operator import indexOf
from pickle import TRUE
from pydoc import doc
from tkinter.tix import Tree
import pandas as pd
import numpy as np
import json
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import gzip


userDataset = "australian_users_items.json.gz"
gameDataset = "steam_games.json.gz"


# reads in the data from the file since there are a lot of rows


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)

# gets the game's metadata


def getGameInfo(game, df):
    data = NULL
    Found = False
    for i in range(len(df)):
        if df.loc[i]["title"].upper() == game.upper():
            data = df.loc[i]
            Found = True
        if Found == True:
            break
    return data


# Reading in the datasets and cleaning
user = []
for row in parse(userDataset):
    user.append(row)
userDf = pd.DataFrame(user)
# dropping users who own less than 2 items
userDf = userDf.drop(userDf[userDf["items_count"] < 2].index)
userDf = userDf.reset_index()

f = []


for row in parse(gameDataset):
    f.append(row)

df = pd.DataFrame(f)
# if item is missing a title, fill it in with the item's app name if possible
df["title"] = df["title"].fillna(df.pop("app_name"))

# used the url for the associated row to find the name of the item and entering
df.at[2580, "title"] = "Duet"


df = df.drop(index=74)  # removing the row that is full of NaN values
df = df.reset_index()  # resetting the index values since I took out a row

# removing the rows that have no tags
df = df.drop(df[df["tags"].isnull()].index)
df = df.reset_index()

# Making an array containing the tags for every game in the dataset
gameText = []
for i in range(len(df)):
    game = df.loc[i]
    temp = ", ".join(game["tags"])
    gameText.append(temp)

# "Deponia"
getRecs = True  # boolean variable to loop off of
while(getRecs):
    targetGameTitle = input()
    targetGame = getGameInfo(targetGameTitle, df)
    game = ", ".join(targetGame["tags"])

    gameText.append(game)

    TfidfVec = TfidfVectorizer()
    tfidf = TfidfVec.fit_transform(gameText)

    vals = cosine_similarity(tfidf[-1], tfidf)

    idx = []

    # getting the 50 most similar games
    for i in range(50):
        temp = vals.argsort()[0][-3 - i]
        idx.append(temp)

    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    gameText.remove(game)

    similarGames = []
    for i in idx:
        similarGames.append(df.loc[i]["title"])

    # making a list that will count the amount of times a similar game appears in a list that has the target game
    appeared = [0]*len(similarGames)

    for i in range(len(userDf)):
        temp = userDf.loc[i]["items"]
        userItems = []
        for item in temp:
            userItems.append(item["item_name"])
        if targetGame["title"] in userItems:
            for i in range(len(similarGames)):
                if similarGames[i] in userItems:
                    appeared[i] += 1

    similarOrdered = []

    # ordering the games by how often they appeared alongside the target game in lists
    for i in range(len(appeared)):
        similarOrdered.append(similarGames[appeared.index(max(appeared))])
        similarGames.remove(similarGames[appeared.index(max(appeared))])
        appeared.remove(max(appeared))

    # outputting the top 10 games
    print("Target game: " + targetGame["title"])
    for i in range(10):
        print(similarOrdered[i])
