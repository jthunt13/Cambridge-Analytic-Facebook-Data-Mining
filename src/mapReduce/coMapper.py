import sys
from nltk.corpus import stopwords
import string
import re
from unidecode import unidecode

# Define and add stop words
stop_words = set(stopwords.words('english'))
stop_words.add('advertisement')
stop_words.add('percent')
stop_words.add('said')
stop_words.add('mr')
stop_words.add('new')
stop_words.add('-')

# Used to remove punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))

# Initialize list to collect all words in article or tweet
allWords = []

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = unidecode(line)
    line = line.strip()

    # split the line into words
    words = line.split()

    for word in words:
        w = word.lower()

        # remove punc, quotes
        w = regex.sub('', w)
        w = w.replace('\"','')

        if w in stop_words:
            continue

        if w == '':
            continue

        allWords.append(w)

for idx, val in enumerate(allWords):
    for i in range(idx,len(allWords)-1):
        if val == allWords[i+1]:
            continue
        else:
            print('%s,%s' % (val, allWords[i+1]))
