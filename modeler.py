from collections import defaultdict
from random import choices
from nltk import ngrams
from os import listdir
#from pickle import load, dump

qaDict = defaultdict(lambda: defaultdict(int))
#qaFistDict = defaultdict(dd)
ngramsDict = defaultdict(lambda: defaultdict(int))
ngramsDict2 = defaultdict(lambda: defaultdict(int))
ngramsDict3 = defaultdict(lambda: defaultdict(int))

nNgram = 2
for chatName in listdir('clean'):
#for chatName in ['EmiliaRose_tJG_fEH10A']:
    print(chatName)
    #with open("emilia.txt", "r", encoding='utf-8') as f:
    with open(f'clean/{chatName}', "r", encoding='utf-8') as f:
        f.readline()
        for nLine, sentence in enumerate(f):
            #if nLine%1000==0:
            #    print(nLine)
            sender, sentence = sentence.strip().split(':')
            if sender != 'Bartek Paulewicz':
                question = sentence
            else:
                words = sentence.split()
                #first = words[0]
                for ngram in ngrams(words, nNgram + 1):
                    ngramsDict[ngram[:-1]][ngram[-1]] += 1
                for ngram in ngrams(words, nNgram + 2):
                    ngramsDict2[ngram[:-1]][ngram[-1]] += 1
                for ngram in ngrams(words, nNgram + 3):
                    ngramsDict3[ngram[:-1]][ngram[-1]] += 1
                #for ngram in ngrams(question.split(), nNgram):
                #    for word in words:
                #        qaDict[ngram][word] += 1
                '''
                for k1, v1 in ngramsDict1.items():
                    print(k1)
                    for k2, v2 in v1.items():
                        print(k2, v2)
                print()
                for k1, v1 in ngramsDict2.items():
                    print(k1)
                    for k2, v2 in v1.items():
                        print(k2, v2)
                
                print()
                for k1, v1 in qaDict.items():
                    print(k1)
                    for k2, v2 in v1.items():
                        print(k2, v2)
                '''
                #break
#prev = ('nie', 'wiem', 'czy', 'nie')
#for k, v in ngramsDict2[prev].items():
#    print(k, v)

print('build')
'''
for i in range(10):
    #dicts = [qaFistDict[ngram] for ngram in ngrams(question.split(), nNgram)]
    #qaFistNorm = {k: sum(d.get(k, 0) / (dSum or 1) for d, dSum in zip(dicts, (sum(d.values()) for d in dicts))) for k in
    #              set().union(*dicts)}
    #prev = choices(list(qaFistNorm.keys()), weights=qaFistNorm.values())[0]
    prev = ('nie', 'wiem', 'czy', 'nie')[:nNgram+2]
    res = list(prev)
    while True:
        ngramsPrev1 = ngramsDict[prev[2:]]
        ngramsPrev2 = ngramsDict2[prev[1:]]
        ngramsPrev3 = ngramsDict3[prev]
        sum1 = sum(ngramsPrev1.values())
        sum2 = sum(ngramsPrev2.values())
        sum3 = sum(ngramsPrev3.values())

        if ngramsPrev3:
            ngramsPrev = {k: ngramsPrev1.get(k, 0)/sum1 + ngramsPrev2.get(k, 0)/sum2 + ngramsPrev3.get(k, 0)/sum3 for k in ngramsPrev1.keys()}
            #ngramsPrev = ngramsPrev3
        elif ngramsPrev2:
            ngramsPrev = {k: ngramsPrev1.get(k, 0) / sum1 + ngramsPrev2.get(k, 0) / sum2 for k in ngramsPrev1.keys()}
            #ngramsPrev = ngramsPrev2
        else:
            ngramsPrev = ngramsPrev1

        #ngramsPrev = ngramsDict[prev]
        if ngramsPrev:
            word = choices(list(ngramsPrev.keys()), weights=ngramsPrev.values())[0]
            #word = max(zip(ngramsPrev.values(), list(ngramsPrev.keys())))[1]
            res += [word]
            prev = (*prev[1:], word)
        else:
            print(' '.join(res))
            suma = 0
            for ngram in ngrams(res, nNgram + 1):
                suma += ngramsDict[ngram[:-1]][ngram[-1]] / sum(ngramsDict[ngram[:-1]].values())
            print(suma / (len(res) - nNgram))
            suma = 0
            for ngram in ngrams(res, nNgram + 2):
                tmp = sum(ngramsDict2[ngram[:-1]].values())
                if tmp>0:
                    suma += ngramsDict2[ngram[:-1]][ngram[-1]]/tmp
            print(suma / (len(res) - nNgram))
            break

'''
'''
# question = 'no to ja jutro nie moge'
question = 'zeby nie bylo'

# dicts = [qaFistDict[ngram] for ngram in ngrams(question.split(), nNgram)]
# qaFistDict.clear()
# del qaFistDict
# qaFistNorm = {k: sum(d.get(k, 0)/(dSum or 1) for d, dSum in zip(dicts,(sum(d.values()) for d in dicts))) for k in set().union(*dicts)}
# originalPrev = choices(list(qaFistNorm.keys()), weights=qaFistNorm.values())[0]
# qaFistNorm.clear()
# del qaFistNorm

dicts = [qaDict[ngram] for ngram in ngrams(question.split(), nNgram)]
sums = [sum(d.values()) for d in dicts]
qaNorm = {k: sum(d.get(k, 0)/(dSum or 1) for d, dSum in zip(dicts, sums)) for k in set().union(*dicts)}
qaSum = sum(qaNorm.values())
qaNorm = {k: v/qaSum for k, v in qaNorm.items()}

qaKeys = set().union(*(qaDict[ngram] for ngram in ngrams(question.split(), nNgram)))

for i in range(10):
    dicts = [qaFistDict[ngram] for ngram in ngrams(question.split(), nNgram)]
    qaFistNorm = {k: sum(d.get(k, 0) / (dSum or 1) for d, dSum in zip(dicts, (sum(d.values()) for d in dicts))) for k in
                  set().union(*dicts)}
    prev = choices(list(qaFistNorm.keys()), weights=qaFistNorm.values())[0]
    res = list(prev)
    while True:
        ngramsPrev = ngramsDict[prev]
        # qaPrev = qaDict[prev]
        # ngramsSum = sum(ngramsPrev.values())
        # qaSum = sum(qaPrev.values())
        # tmpDict = {k: ngramsPrev.get(k, 0)#/(ngramsSum or 1) + qaNorm.get(k, 0)
        #           for k in ngramsPrev.keys() & qaKeys
        #           }
        if ngramsPrev:
            tmpKeys = ngramsPrev.keys()  # & qaKeys
            if tmpKeys:
                tmpDict = {k: ngramsPrev.get(k, 0) for k in tmpKeys}
                tmp = choices(list(tmpDict.keys()), weights=tmpDict.values())[0]
                # tmp = max(tmpDict.items(), key=lambda x: x[1])[0]
                res += [tmp]
                prev = (*prev[1:], tmp)
            else:
                # tmp = choices(list(ngramsPrev.keys()), weights=ngramsPrev.values())[0]
                tmp = max(tmpDict.items(), key=lambda x: x[1])[0]
                res += [tmp]
                prev = (*prev[1:], tmp)
        else:
            suma = 0
            for ngram in ngrams(res, nNgram + 1):
                suma += ngramsDict[ngram[:-1]][ngram[-1]] / sum(ngramsDict[ngram[:-1]].values())
            print(suma / (len(res) - nNgram), ' '.join(res))
            break
'''