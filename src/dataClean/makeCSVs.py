import pandas as pd
import os

savePath = "../../webpage/data/"

def getTopWords(df,fileName):
    df = df.sort_values("count",ascending = False)
    dfTop50 = df[:50]
    dfTop50.to_csv(savePath + fileName + "top50.csv", index = False,header = True)
    dfTop25 = df[:25]
    dfTop25.to_csv(savePath + fileName + "top25.csv", index = False,header = True)
    dfTop10 = df[:10]
    dfTop10.to_csv(savePath + fileName + "top10.csv", index = False,header = True)

#------------------------------------------------------------------------------
#                           Make CSVS for NYT data
#------------------------------------------------------------------------------
loadPath = "../../data/2weeks/NewsWords/"

df = pd.read_csv(loadPath + "wordCountNYTCambridgeAnalytic.txt",names = ["word","count"])
getTopWords(df,"nytCamAnalyFull")

df = pd.read_csv(loadPath + "wordCountNYTFacebook.txt",names = ["word","count"])
getTopWords(df,"nytFacebookFull")

df = pd.read_csv(loadPath + "cooccurrNYTCambridgeAnalytic.txt",names = ["word","count"])
df.to_csv(savePath + "nytCamAnalyFullCo.csv")

df = pd.read_csv(loadPath + "cooccurrNYTFacebook.txt",names = ["word","count"])
df.to_csv(savePath + "nytFacebookFullCo.csv")

loadPath = "../../data/1day/NewsWords/"

df = pd.read_csv(loadPath + "wordCountNYTCambridgeAnalytic.txt",names = ["word","count"])
getTopWords(df,"nytCamAnalyPartial")

df = pd.read_csv(loadPath + "wordCountNYTFacebook.txt",names = ["word","count"])
getTopWords(df,"nytFacebookPartial")

df = pd.read_csv(loadPath + "cooccurrNYTCambridgeAnalytic.txt",names = ["word","count"])
df.to_csv(savePath + "nytCamAnalyPartialCo.csv")

df = pd.read_csv(loadPath + "cooccurrNYTFacebook.txt",names = ["word","count"])
df.to_csv(savePath + "nytFacebookPartialCo.csv")

#------------------------------------------------------------------------------
#                           Make CSVS for Twitter data
#------------------------------------------------------------------------------
loadPath = "../../data/2weeks/TwitterWords/"

df = pd.read_csv(loadPath + "wordCountTwitterCambridgeAnalytic.txt",names = ["word","count"])
getTopWords(df,"twitterCamAnalyFull")

df = pd.read_csv(loadPath + "wordCountTwitterFacebook.txt",names = ["word","count"])
getTopWords(df,"twitterFacebookFull")

df = pd.read_csv(loadPath + "cooccurrTwitterCambridgeAnalytic.txt",names = ["word","count"])
df.to_csv(savePath + "twitterCamAnalyFullCo.csv")

df = pd.read_csv(loadPath + "cooccurrTwitterFacebook.txt",names = ["word","count"])
df.to_csv(savePath + "twitterFacebookFullCo.csv")

loadPath = "../../data/1day/TwitterWords/"

df = pd.read_csv(loadPath + "wordCountTwitterCambridgeAnalytic.txt",names = ["word","count"])
getTopWords(df,"twitterCamAnalyPartial")

df = pd.read_csv(loadPath + "wordCountTwitterFacebook.txt",names = ["word","count"])
getTopWords(df,"twitterFacebookPartial")

df = pd.read_csv(loadPath + "cooccurrTwitterCambridgeAnalytic.txt",names = ["word","count"])
df.to_csv(savePath + "twitterCamAnalyPartialCo.csv")

df = pd.read_csv(loadPath + "cooccurrTwitterFacebook.txt",names = ["word","count"])
df.to_csv(savePath + "twitterFacebookPartialCo.csv")
