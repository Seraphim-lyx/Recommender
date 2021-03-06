# -*- coding: utf-8 -*-
"""

"""

import UserCF
import UserCF_IIF
import UserTimeCF
import ItemCF
import ItemCF_IUF
import ItemTimeCF
import GeoCF
import random
import Evaluation
import LFM
import operator
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import imp
from pylab import *

imp.reload(GeoCF)
imp.reload(UserCF)
imp.reload(UserCF_IIF)
imp.reload(UserTimeCF)
imp.reload(ItemCF)
imp.reload(ItemCF_IUF)
imp.reload(ItemTimeCF)
imp.reload(Evaluation)
imp.reload(LFM)



def readData(filename):
    data = []
    fr = open(filename, 'r')
    for line in fr.readlines():
        lineArr = line.strip().split()
        data.append([lineArr[0], lineArr[1], lineArr[2], lineArr[3]])
    return data


def SplitData(data, M, k, seed):
    test = []
    train = []
    M = 8
    random.seed(seed)
    for user, item, rating, time in data:
        if random.randint(0, M-1) == k:
            test.append([user, item, rating, time])
        else:
            train.append([user, item, rating, time])
    print(len(train))
    return train, test


#
def transform(oriData):
    ret = dict()
    for user, item, rating, time in oriData:
        if user not in ret:
            ret[user] = dict()
        ret[user][item] = [rating, time]
    return ret


def output(train, test, result, k):

    popularity = Evaluation.Popularity(train, test, result)
    coverage = Evaluation.Coverage(train, test, result) * 100
    print("K is:", k)
    print("popularity:{0}".format(popularity))
    print("coverage:{0}".format(coverage))
    return popularity, coverage 

def plot(list_, color, c):
    
    k = ['10', '20', '40', '80', '160']
    ax = plt.subplot()
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.xticks(arange(len(k)),k)

    plt.plot(list_, color, label=c)
    plt.xlabel('K')
    plt.ylabel('coverage')

def getEvaluation(c, train, test):
    rlist = []
    plist = []
    k = ['10', '20', '40', '80', '160']
    for i in k:
        r, p = getResult(c, train, test, int(i))
        rlist.append(r)
        plist.append(p)
    return rlist, plist

def getResult(c, train, test, k):
    W = c.Similarity(train)
    result = c.Recommendation(test.keys(), train, W, 5, k)
    return output(train, test, result, k)

if __name__ == '__main__':
    data = readData('movielens/ub.base')
    train = transform(data)

    data = readData('movielens/ub.test')
    test = transform(data)

    

    # r, p = getEvaluation(ItemCF, train, test)
    geoTime = [20.618336886993603, 22.068230277185503, 21.727078891257996, 20.533049040511727, 19.78678038379531]
    geoItem = [16.172043010752688, 17.124463519313306, 16.773504273504273, 15.940170940170939, 15.437100213219615]
    plot(getEvaluation(UserCF, train, test)[1], 'b-o', 'UserCF')
    plot(getEvaluation(UserCF_IIF, train, test)[1], 'g-o', 'UserCF_IIF')
    plot(getEvaluation(UserTimeCF, train, test)[1], 'r-o', 'UserTimeCF')
    # plot(geoTime, 'c-o', 'GeoTimeCF')
    plot(getEvaluation(ItemCF, train, test)[1], 'm-^', 'ItemCF')
    plot(getEvaluation(ItemCF_IUF, train, test)[1], 'y-^', 'ItemCF_IUF')
    plot(getEvaluation(ItemTimeCF, train, test)[1], 'k-^', 'ItemTimeCF')
    # plot(geoItem, 'b-^', 'GeoItemCF')

    leg = plt.legend(loc='best', ncol=2, mode="expand",
                         shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.show()

    # [P, Q] = LFM.LatentFactorModel(train, 100, 30, 0.02, 0.01)
    # rank = LFM.Recommend('2', train, P, Q)
    # print(rank)
    # result = LFM.Recommendation(test.keys(), train, P, Q)

    #     N = 30
    #     precision += Evaluation.Precision(train, test, result, N)
    #     recall += Evaluation.Recall(train, test, result, N)
    #     coverage += Evaluation.Coverage(train, test, result, N)
    #     popularity += Evaluation.Popularity(train, test, result, N)

  