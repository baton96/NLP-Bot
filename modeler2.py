from collections import defaultdict, Counter
from random import choices
from nltk import ngrams
from os import listdir
import re

ngramsDict1 = defaultdict(lambda: defaultdict(int))
ngramsDict2 = defaultdict(lambda: defaultdict(int))
ngramsDict3 = defaultdict(lambda: defaultdict(int))
ngramsDict4 = defaultdict(lambda: defaultdict(int))

firstDict2 = defaultdict(lambda: defaultdict(int))
firstDict3 = defaultdict(lambda: defaultdict(int))
firstDict4 = defaultdict(lambda: defaultdict(int))

qaDict2 = defaultdict(lambda: defaultdict(int))
qaDict3 = defaultdict(lambda: defaultdict(int))
qaDict4 = defaultdict(lambda: defaultdict(int))

for chatName in listdir('clean'):
    with open(f'clean/{chatName}', "r", encoding='utf-8') as f:
        f.readline()
        prev = ''
        for sentence in f:
            sender, sentence = sentence.strip().split(':')
            if sender != 'Bartek Paulewicz':
                prev = sentence
            else:
                sWords = sentence.split()
                pWords = prev.split()
                first = sWords[0]
                
                for ngram in ngrams(pWords, 2):
                    for pWord in pWords:
                        qaDict2[ngram][pWord] += 1
                for ngram in ngrams(pWords, 3):
                    for pWord in pWords:
                        qaDict3[ngram][pWord] += 1
                for ngram in ngrams(pWords, 4):
                    for pWord in pWords:
                        qaDict4[ngram][pWord] += 1                        
                 
                for ngram in ngrams(pWords, 2):
                    firstDict2[ngram][first] += 1
                for ngram in ngrams(pWords, 3):
                    firstDict3[ngram][first] += 1
                for ngram in ngrams(pWords, 4):
                    firstDict4[ngram][first] += 1
                    
                for ngram in ngrams(sWords, 2):
                    ngramsDict1[ngram[:-1]][ngram[-1]] += 1
                for ngram in ngrams(sWords, 3):
                    ngramsDict2[ngram[:-1]][ngram[-1]] += 1
                for ngram in ngrams(sWords, 4):
                    ngramsDict3[ngram[:-1]][ngram[-1]] += 1
                for ngram in ngrams(sWords, 5):
                    ngramsDict4[ngram[:-1]][ngram[-1]] += 1        
					
q = "noo jak ty wstawisz to ja tez xd a odpisalam po takim czasie bo jak wtedy napisales to musialam isc i dopiero teraz mi sie przypomnialo"
qWords = q.split()

firstDict = Counter()

s = sum(sum(v.values()) for v in firstDict4.values())
for ngram in ngrams(qWords, 4):
    if ngram in firstDict4:
        firstDict.update({k: v/s for k, v in firstDict4[ngram].items()})    
        
s = sum(sum(v.values()) for v in firstDict3.values())
for ngram in ngrams(qWords, 3):
    if ngram in firstDict3:
        firstDict.update({k: v/s for k, v in firstDict3[ngram].items()})

s = sum(sum(v.values()) for v in firstDict2.values())
for ngram in ngrams(qWords, 2):
    if ngram in firstDict2:
        firstDict.update({k: v/s for k, v in firstDict2[ngram].items()})

#fewest = firstDict.most_common()[-1][1]
#firstDict = {k: v for k, v in firstDict.most_common() if v>fewest}      
print(len(firstDict))
#for k, v in firstDict.items():
#    print(k, v)

sentences = []
for k in firstDict.keys():
    res = []
    try:
        prev1 = (k,)
        x = [max(ngramsDict1[prev1].items(), key=lambda x:x[1])[0]]
        #for p1 in ngramsDict1[prev1].keys():
        for p1 in x:
            prev2 = (*prev1, p1)
            y = [max(ngramsDict2[prev2].items(), key=lambda x:x[1])[0]]
            #for p2 in ngramsDict2[prev2].keys():
            for p2 in y:
                prev3 = (*prev2, p2)
                for p3 in ngramsDict3[prev3].keys():
                    prev4 = (*prev3, p3)
                    for p4 in ngramsDict4[prev4].keys():
                        prev5 = (*prev4, p4)
                        #sentences += [' '.join(prev5)]                        
                        res = list(prev5)                        
                        prev5 = (prev5[1:])
                        mySet = set()
                        while True:
                            if prev5 in mySet:
                                #print(' '.join(res))
                                sentences += [' '.join(res)]
                                break
                            else:
                                mySet.add(prev5)
                            try:
                                word = max(ngramsDict4[prev5].items(), key=lambda x:x[1])[0]
                                res += [word]
                                prev5 = (*prev5[1:], word)
                            except:
                                sentences += [' '.join(res)]
                                break
                        
                        
        #break
    except:
        pass
        #print('sth fucky')

print(len(sentences))
#for i in range(50):
#    print(i, sentences[i])

scores = {}
for sentence in sentences:
    score = 0
    sWords = sentence.split()
    
    for ngram in ngrams(qWords, 4):
        s = sum(qaDict4[ngram].values())*(len(qWords)-3)*len(sWords)
        if s>0:
            for sWord in sWords:
                score += qaDict4[ngram][sWord]/s
                
    for ngram in ngrams(qWords, 3):
        s = sum(qaDict3[ngram].values())*(len(qWords)-2)*len(sWords)
        if s>0:
            for sWord in sWords:
                score += qaDict3[ngram][sWord]/s
                           
    scores[sentence] = score
    #break

sortedScores = sorted(scores.items(), key=lambda x:x[1])
print(len(sortedScores))
for k, v in sortedScores[-20:]:
    print(v, k)
	
'''

scores = {}
for sentence in sentences:    
    score = 0
    sWords = sentence.split()
    tmpScore = []
    for ngram in ngrams(qWords, 4):
        s = sum(qaDict4[ngram].values())*(len(qWords)-3)*len(sWords)
        if s>0:
            for sWord in sWords:
                #score += qaDict4[ngram][sWord]/s
                tmpScore += [qaDict4[ngram][sWord]]
    if tmpScore:
        score += sum(tmpScore)/(len(tmpScore)*(len(qWords)-3))
    
    tmpScore = []
    for ngram in ngrams(qWords, 3):
        s = sum(qaDict3[ngram].values())*(len(qWords)-2)*len(sWords)
        if s>0:
            for sWord in sWords:
                #score += qaDict3[ngram][sWord]/s
                tmpScore += [qaDict3[ngram][sWord]]
    if tmpScore:
        score += sum(tmpScore)/(len(tmpScore)*(len(qWords)-2))
                   
    scores[sentence] = score/len(sWords)

sortedScores = sorted(scores.items(), key=lambda x:x[1])
print(len(sortedScores))
for k, v in sortedScores[-20:]:
    print(v, k)
'''