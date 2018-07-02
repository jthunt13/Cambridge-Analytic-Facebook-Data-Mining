import pandas as pd;
import requests;
import getpass;
import datetime
import pymysql
import warnings
import json
import time
import math
import os
from sqlalchemy import create_engine

# home made function to store authentications
import loginInfo;

# Ignore warnings
warnings.filterwarnings("ignore", category = Warning)

# variables to change
searchTerms = ["Facebook","Cambridge Analytic"]
searchTable = ["nytFacebookDocs","nytCamAnalyDocs"]
direction = "newest"
pagesToScanThrough = 200
#------------------------------------------------------------------------------
#                           NYT api Function
#------------------------------------------------------------------------------
def getArticleURL(searchTerm, pages, direction,key):

    for i in range(1,pages +1):
        print("Getting page: " + str(i))
        reqStart = r"http://api.nytimes.com/svc/search/v2/articlesearch.json?q="
        reqPart2 = searchTerm.replace(" ","+") + '&document_type:("article")'
        reqPart3 = "&page=" + str(i) + "&sort=" + direction
        req = reqStart + reqPart2 + reqPart3 + "&api-key=" + key
        r = requests.get(req)

        docDict = {}

        if str(r) == "<Response [503]>":
            print("Service Unavailable!")
        else:
            try:
                data = r.json()

                docs = []
                urls = []
                pubDate = []

                for j in range(0,len(data["response"]["docs"])):
                    urls.append(data["response"]["docs"][j]["web_url"])
                    docs.append(data["response"]["docs"][j]["_id"])
                    d = data["response"]["docs"][j]["pub_date"]
                    # convert date
                    tmp = datetime.datetime.strptime(d,"%Y-%m-%dT%H:%M:%S%z")
                    d2 = datetime.datetime.strftime(tmp,"%Y-%m-%d")
                    pubDate.append(d2)

                tmpDict = {"docID" : docs,"docURL" : urls, "docDate" : pubDate}

                if i == 1:
                    df = pd.DataFrame.from_dict(tmpDict)
                    #df = df.set_index("docID")
                else:

                    df2 = pd.DataFrame.from_dict(tmpDict)
                    #df2 = df2.set_index("docID")
                    df = df.append(df2)

                # wait a second until making next request
                time.sleep(1)
            except ValueError:
                print("Got a Value Error!")
                break;

    return df
#------------------------------------------------------------------------------
#                             SQL Functions
#------------------------------------------------------------------------------
def sqlQueryExecuter(engine,query):
    # make connection from engine
    con = engine.connect()
    # store tweets
    df = pd.read_sql(query, con = con)
    # close Connnection
    con.close()
    # return query result
    return df

def storeToDatabase(engine,info,table,key):
    # make connection to database from engine
    con = engine.connect()
    # get keys stored
    
    query = "SELECT " + key + " FROM " + table

    df = sqlQueryExecuter(engine,query)
    # remove duplicates
    info = info[~info.isin(df[key].tolist())[key]]
    # store tweets
    info.to_sql(name = table,
            con = con,
            if_exists = "append",
            index = False)

    # close Connnection
    con.close()

#------------------------------------------------------------------------------
#                           Script to run the functions
#------------------------------------------------------------------------------
if __name__ == "__main__":

    # get keys and login info for DB
    user = getpass.getuser()
    apiKey = loginInfo.getNYTimesAuth(user)
    dbAuth = loginInfo.getSQLLogin(user)

    # make connection to DataBase
    conURL = 'mysql+pymysql://' + dbAuth.username + ':' + dbAuth.password + '@localhost:3306/cse587?charset=utf8'
    engine = create_engine(conURL , echo=False)

    # get date to store
    d = datetime.datetime.now()
    today = d.strftime("%Y-%m-%d")
    try:
        for i in range(0,len(searchTable)):
            print("Getting URLS for search term " + str(i +1) + " from API...")
            data = getArticleURL(searchTerms[i],math.floor(pagesToScanThrough/len(searchTable)),direction,apiKey)
            print("Storing URLS to database...")
            storeToDatabase(engine,data,searchTable[i],"docID")
    except:
        print("Storing URLS to CSV...")

        for i in range(0,len(searchTable)):
            q1 = "SELECT * FROM " + searchTable[i]
            df = sqlQueryExecuter(engine,q1)
            df.to_csv("../../data/" + searchTerms[i] + "URL" + today +".csv")

    print("Done.")
