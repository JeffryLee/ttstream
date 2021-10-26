import os
import sqlite3
import json

conn = sqlite3.connect('aws-main.db', check_same_thread=False)
c = conn.cursor()

c.execute("SELECT NAME FROM IDS")

row = c.fetchall()

conn.close()

vidlist = []
for i in range(len(row)):
    vidlist.append(str(row[i][0]))


vidlist.sort()

vidic= {}

for i in range(len(vidlist)):
    vidic[vidlist[i]] = i

with open('vid.json', 'w') as outfile:
    json.dump(vidic, outfile)




