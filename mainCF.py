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


import imp
imp.reload(UserCF)
imp.reload(UserCF_IIF)
imp.reload(UserTimeCF)
imp.reload(ItemCF)
imp.reload(ItemCF_IUF)
imp.reload(ItemTimeCF)
imp.reload(Evaluation)
imp.reload(LFM)
imp.reload(GeoCF)


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


def output(result):
    with open('output.txt', 'w') as f:
        f.write(json.dumps(result, indent=2))

    f.close()


if __name__ == '__main__':
    data = readData('movielens/ua.base')
    train = transform(data)

    data = readData('movielens/ua.test')
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
#        W = UserCF.UserSimilarity(train)
 #       rank = UserCF.Recommend('1',train,W)
  #      result = UserCF.Recommendation(test.keys(), train, W)

    # W = UserCF_IIF.UserSimilarity(train)
    # rank = UserCF_IIF.Recommend('1', train, W)
    # print(sorted(rank.items(), key=operator.itemgetter(1), reverse=True))
    # result = UserCF_IIF.Recommendation(test.keys(), train, W)
    # print({k: result[k] for k in list(result)[:2]})

#        W = ItemCF.ItemSimilarity(train)
 #       rank = ItemCF.Recommend('1',train,W)
  #      result =  ItemCF_IUF.Recommendation(test.keys(),train, W)

    # W = ItemTimeCF.ItemSimilarity(train)
    # rank = ItemTimeCF.Recommend('1', train, W)
    # print(sorted(rank.items(), key=operator.itemgetter(1), reverse=True))

    W = UserTimeCF.Similarity(train)
    # rank = UserTimeCF.Recommend('1', train, W)
    # rank = ItemTimeCF.Recommend('4', train, W)
    # print(len(rank))
    # print(sorted(rank.items(), key=operator.itemgetter(1), reverse=True))

    result = UserCF_IIF.Recommendation(test.keys(), train, W)
    print(Evaluation.Recall(train, test, result))
    print(Evaluation.Precision(train, test, result))
    # print(len(result))
    output(result)

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
    # rank = obj.recommend('1', train)
    # print(sorted(rank.items(), key=operator.itemgetter(1), reverse=True))
