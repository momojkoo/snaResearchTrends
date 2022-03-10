#-*- coding:utf-8 -(-
# Python 3
# sna.py
# created by Jasuk Koo
# 2022.2.21

from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from VocabDict import VocabDict

vDict = VocabDict()
vDict2 = VocabDict()

wCountAll = {}
userStopWords = {} # user stop words list
sWords = [] #selected words
vThreshold = 10

filename = "Titles.txt"
outCheckFilename = "checkOut.txt" # outfile for check
outMorphemeFilename = "morphemeOut.txt" # outfile for morpheme
outFreqAllFilename = "frequencyOut.txt" # outfile for freq
outfile2Filename = "cofrequencyOut.txt" # outfile for co-freq

# morpheme analysis
kiwi = Kiwi()
kiwi.load_user_dictionary("userDict.txt")
stopwords = Stopwords()
userStopWordsFilename = "userStopwords.txt"

# load user-specified stop words
with open(userStopWordsFilename) as f:
    userStopWords = [line.strip() for line in f.readlines()]

# tokenTagList = {"NNG", "NNP", "NNB", "NP", "VV", "VA", "SL"}
tokenTagList = {"NNG", "NNP", "NP", "SL"}

# read file and tokenize
ofp = open(outCheckFilename, "w", encoding='utf-8')
ofmp = open(outMorphemeFilename, "w", encoding='utf-8')
lineNo = 1
for line in open(filename, encoding='utf-8'):
    ofp.write("============================\n")
    ofp.write(line)
    sTokens = [] # selected Tokens
    token = kiwi.tokenize(line, normalize_coda=True, stopwords=stopwords)
    for t in token:
        if t.tag in tokenTagList :
            if (t.form).lower() not in userStopWords:
                sTokens.append((t.form).lower())
    ofp.write(">> " + ", ".join(sTokens) + "\n")
    ofmp.write(str(lineNo) + "|" + ", ".join(sTokens) + "\n")
    sWords.append(sTokens)
    lineNo += 1
ofmp.close()
ofp.close()

# count frequency
for sTokens in  sWords:    # word count
    for w in sTokens:
        wId = vDict.getIdOrAdd(w)
        if wId not in wCountAll : wCountAll[wId] = 0
        wCountAll[wId] += 1

# write out the frequency results
ofp1 = open(outFreqAllFilename, "w", encoding='utf-8')
for i, num in wCountAll.items():
    ofp1.write(vDict.getWord(i) + "|" +str(num) + "\n")
    # select only those that appear vThreshold or more times and store then in vDict2
    if num < vThreshold: continue
    vDict2.getIdOrAdd(vDict.getWord(i))
ofp1.close()

# free up vDict
# vDict = None

wl = vDict2.len()
count = [[]]
count = [[0 for i in range(wl)] for i in range(wl)]

# count the frequency they appear together
for line in sWords:
    words = list(set(line))
    wids = list(filter(lambda wid : wid>=0, [vDict2.getId(w) for w in words]))
    for i, a in enumerate(wids):
        for b in wids[i+1:]:
            if a > b: 
                a0 = b
                b0 = a
            else :
                a0 = a
                b0 = b
            count[a0][b0] += 1 # count up

# vDict2.printWords()

# print out : freq, co-freq, factor
ofp2 = open(outfile2Filename, "w", encoding='utf-8')
for i in range(wl):
    for j in range(wl):
        if count[i][j] > 0:
            ni = wCountAll[vDict.getId(vDict2.getWord(i))]
            nj = wCountAll[vDict.getId(vDict2.getWord(j))]
            nij = count[i][j]
            factor = nij / (ni * nj) * 100 # 
            ofp2.write(vDict2.getWord(i) + "|" + vDict2.getWord(j) + "|" + str(ni) + "|" +  str(nj)  + "|" +  str(nij) + "|" + "%.6f"%factor +"\n")
ofp2.close()
