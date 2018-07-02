import pandas as pd
import os
os.getcwd()

def reEncodeDirectory(f):

    for i in range(len(f)):
        # strip .txt off of file names
        fname = f[i].replace(".txt","")
        # open file to write too
        f2 = open(fname + "ascii.txt","w")
        # open file to decode and decode it and write it to another file
        with open(f[0], encoding = "utf-8") as f1:
            for line in f1:
                line = str.encode(line).decode("unicode_escape").encode("ascii",errors = "ignore")
                line =line.decode("unicode_escape").replace('b"b',"").replace("b'","")
                f2.write(line)

        # close files
        f1.close()
        f2.close()
# reencode facebook
os.chdir("/home/jkhadley/Documents/Programs/CSE587/Lab2/data/TwitterData/facebook/")
f = os.listdir()
reEncodeDirectory(f)

# reencode cambridgeAnalytic
os.chdir("/home/jkhadley/Documents/Programs/CSE587/Lab2/data/TwitterData/cambridgeAnalytic/")
f = os.listdir()
f
reEncodeDirectory(f)
