import sys
import operator

wcounts = {}

# input comes from STDIN

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    if line in wcounts.keys():
        wcounts[line] += 1
    else:
        wcounts[line] = 1

sorted_wcounts = sorted(wcounts.items(), key=operator.itemgetter(1), reverse = True)

for idx,row in enumerate(sorted_wcounts):
    if idx < 10:
        print('%s,%s' % (row[0],row[1]))
    elif sorted_wcounts[idx][1] == sorted_wcounts[idx+1][1]:
            print('%s,%s' % (row[0],row[1]))
    else:
        break
