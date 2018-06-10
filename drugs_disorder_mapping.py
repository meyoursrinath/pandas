import time
from collections import defaultdict
import csv
import pickle
import json
import MySQLdb
import nltk
import pandas as pd
currentTime = time.time()


def splitter(n, s):
    pieces = s.split()
    ret = [(" ".join(pieces[n:i])) for i in range(len(pieces), 0, -1)]
    listed = []
    for r in ret:
        listed.append(str(r))
    return listed


def cleanString(incomingString):
    array = [
        ",", "+", "(", ")", '.', '"', "!", "-", "@", "#", "$", "*", "=", "?", "\'", "\"", "{", "}", "[", "]", "<", ">", "`", "~", ":", "|", "\\", "/"]
    newstring = incomingString  # function to find the word combination for each interventions

    for eachChar in array:
        newstring = newstring.replace(eachChar, " ")
    return newstring


file = open('consolidated.pkl', 'rb')

# dump information to that file
trie = pickle.load(file)

# close the file
file.close()


# Reading interventions data from csv
columnsInter = defaultdict(list)  # each value in each column is appended to a list

db_connection = MySQLdb.connect("69.164.196.100", "sherlock", "z00mrxr0cks!", "sherlock_ct_new")
cursor = db_connection.cursor()
array = []
df = pd.read_sql('select id,nct_id,detailed_description from trials LIMIT 0, 150000', con=db_connection)

inter = df['detailed_description'].tolist()
interId = df['id'].tolist()
interText = df['nct_id'].tolist()

finalList = []
Except = []
count = 0

# loop to find each word in the trie are not
for eachInter in inter:
    if eachInter is None:
        continue
    else:
        gg = 0
        Ellam = eachInter
        eachInter = cleanString(eachInter)
        Id = interId[count]
        typeText = interText[count]
        lengthText = eachInter.count(' ')
        length = 0
        wordCount = 0
        while length <= (lengthText + 1):
            flag = "False"
            for piece in splitter(length, eachInter):
                if wordCount > 1:
                    wordCount = wordCount - 1
                    continue
                interventionDetail = []
                try:
                    temp = unicode(piece.lower(), 'latin1')
                except Exception:
                    print temp
                if temp in trie:
                    wordCount = temp.count(' ') + 1
                    ans = json.loads(trie[temp][0])
                    text = nltk.word_tokenize(temp)
                    result = nltk.pos_tag(text)
                    gg = 1
                    interventionDetail.append(Id)
                    interventionDetail.append(typeText)
                    interventionDetail.append(piece)
                    interventionDetail.append(ans[0])
                    interventionDetail.append(ans[1])
                    interventionDetail.append(ans[2])
                    print interventionDetail
                    finalList.append(interventionDetail)
                    break
                    length = length + (piece.count(' '))

            if flag == "False":
                length = length + 1

        count = count + 1
        if gg == 0:
            kk = []
            kk.append(Id)
            kk.append(Ellam)
            Except.append(kk)

print "Process complete.."
print len(finalList)


# final result in the csv

with open("DetailedDescription.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(finalList)

with open("ExceptDetailedDescription.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(Except)

print("Total time taken")
print(time.time() - currentTime)
