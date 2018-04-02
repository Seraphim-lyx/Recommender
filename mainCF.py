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


def output(train, test, result):

    # with open('output.txt', 'w') as f:
    #     f.write(json.dumps(result, indent=2))
    # f.close()
    recall = Evaluation.Recall(train, test, result) * 100
    precision = Evaluation.Precision(train, test, result) * 100
    print("Recall:{0}".format(recall))
    print("Precision:{0}".format(precision))
    return recall, precision 

def plot(list_, color):
    
    k = ['10', '20', '40', '80', '160']
    ax = plt.subplot()
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.xticks(arange(len(k)),k)

    plt.plot(list_, color, label=c.__dict__['__name__'])
    plt.xlabel('K')
    plt.ylabel('Accuracy')

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
    return output(train, test, result)

if __name__ == '__main__':
    data = readData('movielens/ub.base')
    train = transform(data)

    data = readData('movielens/ub.test')
    test = transform(data)

    numFlod = 5
    precision = 0
    recall = 0
    coverage = 0
    popularity = 0
    # for i in range(0, numFlod):
    # [oriTrain, oriTest] = SplitData(data, numFlod, 1, 0)

    # test = transform(oriTest)
    # print(len(train))
    # print(len(sorted(train)))
    # for i in train.keys():
    #     print(i)

    # for i in test.keys():
    # count += 1
    # test = transform(oriTest)
    # print(count)
    # print(test)


    # W = ItemTimeCF.ItemSimilarity(train)
    # rank = ItemTimeCF.Recommend('1', train, W)
    # print(sorted(rank.items(), key=operator.itemgetter(1), reverse=True))

    # W = UserCF.Similarity(train)

    # result = UserCF.Recommendation(test.keys(), train, W, 10, 80)

    # output(train, test, result)

    # result = ItemCF.Recommendation(test.keys(), train, W, 10, 3)
    # print(Evaluation.Recall(train, test, result))
    # print(Evaluation.Precision(train, test, result))
    # output(result)

    # W = UserCF_IIF.Similarity(train)
    # result = UserCF_IIF.Recommendation(test.keys(), train, W, 10, 80)
    # print(Evaluation.Recall(train, test, result))
    # print(Evaluation.Precision(train, test, result))
    # output(result)

    # W = UserTimeCF.Similarity(train)
    # result = UserTimeCF.Recommendation(test.keys(), train, W, 5, 80)
    # output(train, test, result)
    k = ['10', '20', '40', '80', '160']
    obj = GeoCF.GeoCF(ItemTimeCF)
    result = obj.recommendation(test.keys(), train, 5, 80)
    output(train, test, result)
##################################################################

    # W = ItemCF.Similarity(train)
    # result = ItemCF.Recommendation(test.keys(), train, W, 5, 10)
    # output(train, test, result)

    # W = ItemCF_IUF.Similarity(train)
    # result = ItemCF_IUF.Recommendation(test.keys(), train, W, 5, 10)
    # output(train, test, result)

    # W = ItemTimeCF.Similarity(train)
    # result = ItemTimeCF.Recommendation(test.keys(), train, W, 5, 10)
    # output(train, test, result)
    
    
    # r, p = getEvaluation(ItemCF, train, test)
    # plot(r, 'b-o')
    # plot(ItemCF_IUF, train, test, 'g-o')
    # plot(ItemTimeCF, train, test, 'r-o')
    # leg = plt.legend(loc='best', ncol=2, mode="expand",
    #                      shadow=True, fancybox=True)
    # leg.get_frame().set_alpha(0.5)
    # plt.show()

    #     [P, Q] = LFM.LatentFactorModel(train, 100, 30, 0.02, 0.01)
    #     rank = LFM.Recommend('2', train, P, Q)
    #     result = LFM.Recommendation(test.keys(), train, P, Q)

    #     N = 30
    #     precision += Evaluation.Precision(train, test, result, N)
    #     recall += Evaluation.Recall(train, test, result, N)
    #     coverage += Evaluation.Coverage(train, test, result, N)
    #     popularity += Evaluation.Popularity(train, test, result, N)

    # precision /= numFlod
    # recall /= numFlod
    # coverage /= numFlod
    # popularity /= numFlod

    # print("%20s%20s%20s%20s" %
    #       ('precision', 'recall', 'coverage', 'popularity'))
    # print("%20s%%%20s%%%20s%%%20s" %
    #       (precision * 100, recall * 100, coverage * 100, popularity))
    # # 运行完标志
    # print('Done!')

    # obj = GeoCF.GeoCF(UserTimeCF)
    # rank = obj.recommend('1', train, 80)
    # print(sorted(rank.items(), key=operator.itemgetter(1), reverse=True))
    # print(sorted(rank))
