from nltk.corpus import stopwords
from nltk import PorterStemmer
import nltk
from nltk.tokenize import word_tokenize
import math
import re
from collections import OrderedDict
nltk.download('punkt')

p = PorterStemmer()

def processparagraph(input: str) -> list:
    sen_list = nltk.tokenize.sent_tokenize(input)
    sen_copy = [word_tokenize(removechar(sen)) for sen in sen_list]
    res = []
    for each in sen_copy:
        newlist = [p.stem(word.lower()) for word in each if word not in stopwords.words()]
        res.append(newlist)
    return res, sen_list

def tfidf(input: list) -> dict:
    worddic = dict()
    vectordic = dict()
    wordset = [set(each) for each in input]
    for sen in wordset:
        for word in sen:
            if word not in worddic:
                worddic[word] = 1
            else:
                worddic[word] += 1
            
    for index, sen in enumerate(wordset):
        sen_vector = dict()
        for word in sen:
            tf = input[index].count(word) / len(sen)
            idf = math.log(len(input) / worddic[word])
            sen_vector[word] = tf * idf
        vectordic[index] = sen_vector
    return vectordic
            
def cosinesimilarity(matrix: dict) -> dict:
    res = dict()
    for i in matrix:
        vectori = matrix[i]
        temp = dict()
        for j in matrix:
            if i != j:
                vectorj = matrix[j]
                score = cosinehelper(vectori, vectorj)
                temp[j] = score
        res[i] = temp
    return res


def cosinehelper(vectori: dict, vectorj: dict) -> float:
    res : float = 0
    producti : float = 0
    productj : float = 0
    for wordi in vectori:
        if wordi in vectorj:
            res += vectorj[wordi] * vectorj[wordi]
    for wi, scorei in vectori.items():
        producti += scorei ** 2
    for wj, scorej in vectorj.items():
        productj += scorej ** 2
    return res / (math.sqrt(producti) * math.sqrt(productj))
            
    
def removechar(text):
    regex = r'[^a-zA-Z0-9\s]'
    text = re.sub(regex,'',text)
    return text

# def calsimilarity(input1: list, input2: list) -> float:
#     sharedword = [word for word in input1 if word in input2]     
#     return len(sharedword) / (math.log(input1) + math.log(input2))
'''
Here we use TextRank algorithm to rank the most related texts
'''
def pagerank(matrix: dict, damping = 0.85, epslone = 0.0001) -> list:
    prob = dict()
    for i in matrix:
        prob[i] = 1 / len(matrix)
    smallenough = False
    while not smallenough:
        count = 0
        newprob = dict()
        for i in matrix.keys():
            sumoutside : float = 0
            for j in matrix[i].keys():
                visited = list()
                suminside : float = 0
                for k in matrix[j].keys():
                    if j != k:
                        if set([j, k]) not in visited:
                            suminside += matrix[j][k]
                            visited.append(set([j, k]))
                if suminside == 0:
                    sumoutside += 0
                else:
                    sumoutside += (matrix[i][j] / suminside) * prob[j]
                newscore = (1 - damping) + damping * sumoutside
            newprob[i] = newscore
        for index, score in prob.items():
            if abs(score - newprob[index]) < epslone:
                count += 1
        if count == len(matrix.keys()):
            smallenough = True
        prob = newprob
    return newprob

def rank(input: dict, percent = 0.5) -> list:
    sort = OrderedDict(reversed(list({k: v for k, v in sorted(input.items(), key=lambda item: item[1])}.items())))
    items = list(sort.keys())[:int(len(input) * percent)]
    return items

def main(test: str) -> list:
    text, senlist = processparagraph(test)
    tfidfvalue = tfidf(text)
    cosinevalue = cosinesimilarity(tfidfvalue)
    sort = pagerank(cosinevalue)
    ranked = rank(sort)
    sortedranked = sorted(ranked)
    res = [senlist[index] for index in sortedranked]
    return res
main()