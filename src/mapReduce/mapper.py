import sys
from nltk.corpus import stopwords
import string
import re
from unidecode import unidecode

# Define and add stop words
stop_words = set(stopwords.words('english'))
extra_words = ['advertisement','-']
for idx,x in enumerate(extra_words):
    stop_words.add(x)

# Used to remove punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))

# initialize empty dictionary for combiner
wcounts = {}

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

        if w in wcounts.keys():
            wcounts[w] += 1
        else:
            wcounts[w] = 1
for key in wcounts:
    print ('%s,%s' % (key, wcounts[key]))
