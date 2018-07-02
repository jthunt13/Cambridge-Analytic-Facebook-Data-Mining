import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import os
#from gw_utility.logging import Logging

def urlScrape(row,outputFolder):
    id = row[1][0]
    url = row[1][1]
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    body = soup.find({'article':'id=story'})
    pars = body.find_all('p')
    txt = ''
    for i in pars:
        txt += '\n' + ''.join(i.findAll(text = True))
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    fname = outputFolder + '/' + id + '.txt'
    with open(fname,'w') as f:
        print(txt,file = f)
#------------------------------------------------------------------------------------------------
# Set file name to read from and range of dates to read:
filename = "../../data/1day/NewsData/FacebookURL2018-04-04.csv"
dates = ['2018-4-4','2018-4-6']
outputFolder = '../../data/1day/NewsData/facebook'
#------------------------------------------------------------------------------------------------

# Convert input dates to correct type
dates_list = [dt.datetime.strptime(date, '%Y-%m-%d').date() for date in dates]

# Read in url's, ignore first column
df = pd.read_csv(filename,parse_dates=['docDate'])
df = df.drop(df.columns[0], axis = 1)

# subset url's to only include specified date range
hits = df[(df['docDate'] >= dates_list[0]) & (df['docDate'] <= dates_list[1])].reset_index(drop=True)

# Scrape each url
err = []
for row in hits.iterrows():
    print('Row:' + str(row[0]) + '/' + str(len(hits)) + '...')
    try:
        urlScrape(row,outputFolder)
        print('done')
    except AttributeError as error:
        err.append(row[0])
print('Bad Rows: '+ str(err))
