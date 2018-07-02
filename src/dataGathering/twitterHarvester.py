import pandas as pd;
import twitter;
import getpass;
import datetime;
import pymysql;
import warnings
import sys
import os
from sqlalchemy import create_engine

# home made function to store twitter authentication
import loginInfo;

# Ignore warnings
warnings.filterwarnings("ignore", category = Warning)

searchType = "older"
#searchType = "newer"
#------------------------------------------------------------------------------
#                         Setup twitter Api function
#------------------------------------------------------------------------------
def setupTwitterApi(user):
    # get info from loginInfo script
    twitterAuth = loginInfo.getTwitterAuth(user)
    # make connection to api
    api = twitter.Api(consumer_key=twitterAuth.consumerKey,
                    consumer_secret=twitterAuth.consumerSecret,
                    access_token_key=twitterAuth.accessToken,
                    access_token_secret=twitterAuth.accessTokenSecret)

    return api
#------------------------------------------------------------------------------
#                         SQL functions
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
    newIndex = info[~info.isin(df[key].tolist())[key]].index.tolist()

    info = info[~info.isin(df[key].tolist())[key]]
    # store tweets
    info.to_sql(name = table,
            con = con,
            if_exists = "append",
            index = False)

    # close Connnection
    con.close()

    return newIndex

#------------------------------------------------------------------------------
#                             Use Twitter Api
#------------------------------------------------------------------------------
if __name__ == "__main__":
    # get username from system
    user = getpass.getuser()
    # connect to API
    api = setupTwitterApi(user)
    print("API Connnection Successful!")
    dbAuth = loginInfo.getSQLLogin(user)
    # make connection to api
    conURL = 'mysql+pymysql://' + dbAuth.username + ':' + dbAuth.password + '@localhost:3306/cse587?charset=utf8'
    engine = create_engine(conURL , echo=False)

    # setup information to feed api
    d = datetime.datetime.now()
    today = d.strftime("%Y-%m-%d")
    searchTerms = ["Cambridge Analytic","Facebook"]
    tables = ["cambridgeAnalytic","facebook"]

    cols = ["tweetID","tweetDate"]

    rateLimitExceeded = False
    #rateLimitExceeded = True
    j = 0;

    print("Collecting tweets", end = '')

    while rateLimitExceeded != True:

        # do modulo math to cycle through terms
        termToUse = j%len(searchTerms)

        try:
            if searchType == "newer":
                # get newest tweet id
                newestTweetQuery = "SELECT max(tweetID) AS tweetID FROM " + tables[termToUse]
                newestTweetID = sqlQueryExecuter(engine,newestTweetQuery)
                newestTweetID = newestTweetID.at[0,"tweetID"]

                # get tweets newer than newest tweet
                tweets = api.GetSearch(term = searchTerms[termToUse],
                            since_id = newestTweetID,
                            count = 100)

            elif searchType == "older":
                # get oldest tweet id
                oldestTweetQuery = "SELECT min(tweetID) AS tweetID FROM " + tables[termToUse]
                oldestTweetID = sqlQueryExecuter(engine,oldestTweetQuery)
                oldestTweetID = oldestTweetID.at[0,"tweetID"]

                # run the twitter api
                #print("Collecting Tweets...")
                # get tweets older than oldest tweet
                tweets = api.GetSearch(term = searchTerms[termToUse],
                            max_id = oldestTweetID,
                            count = 100)
            else:
                print("Nothing defined for this search type")

            # create lists
            tweetID = []
            tweetDate = []
            tweetList = []
            newIndex = []

            # Populate the lists
            for i in range(0,len(tweets)):

                tmp = tweets[i]
                tweet = tmp.AsDict()
                tweetID.append(tweet["id"])
                # transform date
                tmpDate = datetime.datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y")
                tweetDate.append(tmpDate.strftime("%Y-%m-%d %H:%M:%S"))
                # encode as utf8 to deal with emojis
                tweetList.append(tweet["text"].encode("utf-8"))

            # Create a dictionary from the lists
            tmpDict = {cols[0] : tweetID, cols[1] : tweetDate}
            # Create a dataframe from the dictionary
            df = pd.DataFrame(data = tmpDict)

            #print("Storing Collected Tweets...")
            newIndex = storeToDatabase(engine,df,tables[termToUse],"tweetID")

            # get Tweets that are new
            newTweets = [tweetList[i] for i in newIndex]
            newTweetID = [tweetID[i] for i in newIndex]

            #write new tweets to text file
            for k in range(len(newTweets)):
                f = open("../../data/tweets/" + tables[termToUse]  + "/"+ str(newTweetID[k]) + ".txt", "w+")
                f.write(str(newTweets[k]))
                f.close()

            j += 1
            print(".",end = "")
            sys.stdout.flush()
        except:
            rateLimitExceeded = True
            print("\nRate Limit Exceeded!")
            print("scanned through " + str(100*j) + " tweets.")
    # end of while loop
    print("\nStoring tweets as csv's...")

    # need to cycle through tables and store all
    for i in range(0,len(tables)):
        selectAllQuery = "SELECT * FROM " + tables[i]
        dfAll = sqlQueryExecuter(engine,selectAllQuery)
        dfAll = dfAll.set_index("tweetID")
        csvName = "../../data/" + tables[i] + "TweetID_CSV_" + str(today)
        dfAll.to_csv(csvName)

    d = datetime.datetime.now()

    print("Done.")

    print("\nRan at: " + d.strftime("%Y-%m-%d %H:%M:%S") + "\n")
