from nltk.corpus import brown
import numpy as np 
from collections import Counter 
from collections import defaultdict 
from math import log 
import time 
import nltk 
import re #MODIFIED...

stime = time.time()
sentences= (np.array([element for sinList in brown.tagged_sents() for element in sinList])) #MODIFIED....
words = brown.tagged_words()
tokens,taged = zip(*words) 
total =len(words)
wordcount = Counter(tokens) 
tokenTags = defaultdict(Counter) 
for token, tag in words: 
    tokenTags[token][tag] += 1 
tagcount = Counter(taged) 
for i in tagcount.keys(): 
    tagcount[i] = tagcount[i]/total 
bgram = nltk.ngrams(taged,2) 
tagtags = defaultdict(Counter) 
for tagl, tag2 in bgram: 
    tagtags[tagl][tag2] += 1 
trans = {}
StateProbs = {} 
def viterbi(prior,transition,num): 
    a = [] 
    trans[num]= [] 
    StateProbs[num+1] =[] 
    emmision = tokenTags[test[num]] 
    wn=wordcount[test[num]] 
    p ={}
    for ik,ii in emmision.items():
        #hold probs 
        min = 100000 
        for jk,ji in prior.items(): 
            if transition[jk][ik] != 0: 
                if num==0: 
                    prob =log((ii/wn),2) + (log((transition[jk][ik]/(total)))) 
                else: 
                    prob = ji + log((ii/wn), 2) + (log((transition[jk][ik]/(total)))) 
                trans[num].append([(jk,ik),prob]) 
                if min > prob: 
                    min = prob 
        p[ik] = min 
        StateProbs[num+1].append([ik,min]) 
    return p

#MODIFIED FROM BELOW.......

def convertToList(para):  #function for convert the input paragraph into List...
    return ''.join(para).split()

input=['Once the poet was walking down a road and then there was a diversion, '
       'there were two different paths and he had to choose one out of them. The poet says that as he was one person, '
       'he could travel on one road only. He had to choose one out of these two roads.'
       ' Yellow wood means a forest with leaves which are wearing out and they have turned yellow in colour — the season of autumn. It represents a world which is full of people, where people have been living for many years. '
       'They represent people who are older than the poet. '
       'The poet kept standing there and looked at the path very carefully as far as he'
       ' could see it. Before taking the path, he wanted to know how it was. '
       'Was it suitable for him or not? He was able to see the path till from where it'
       ' curved after which it was covered with trees and was hidden. '
       'It happens in our life also when we have choices, we have alternatives, '
       'but we have to choose only one out of them, we take time to think about the pros and cons, '
       'whether it is suitable for us or not and only then, we take decision on what path we should choose.']

test=(re.findall(r"[\w']+|[.,!?;]", input[0]))

#MODIFIED ABOVE....

prev = viterbi(tagcount,tagtags,0) 
for i in range(1,len(test)): 
    prev=viterbi(prev,tagtags,i) 
del trans[0] 
prevP = 0 
prev = ''
order = [] 
for i in range(len(test)-1,-1,-1): 
    if i == len(test)-1: 
        min = 100000000 
        for j in StateProbs[i+1]: 
            if min > j[1]: 
                prev = j[0] 
                min = j[1] 
                prevP = j[1] 
        order.append(prev) 
    else: 
        for g in trans[i+1]: 
            if prevP == g[1]: 
                x,y = g[0] 
                prev = x 
                order.append(prev) 
        for k in StateProbs[i+1]: 
            if k[0] == prev: 
                prevP = k[1] 

sol = [] 
for i in reversed(order): 
    sol.append(i) 
print(test) 
print(sol) 
print("--- %s seconds ---" % (time.time() - stime)) 