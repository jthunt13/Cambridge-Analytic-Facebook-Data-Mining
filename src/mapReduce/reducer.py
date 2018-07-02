import sys

wcounts = {}

# input comes from STDIN

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    word, count = line.split(',')
    count = int(count)

    if word in wcounts.keys():
        wcounts[word] += count
    else:
        wcounts[word] = count
for key in wcounts:
    print('%s,%s' % (key, wcounts[key]))
