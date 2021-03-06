# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 09:56:26 2018

@author: lanlandetian
"""

import math
import operator


def Similarity(train):
    # build inverse table for item_users
    item_users = dict()
    for u, items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            # print(u)
            item_users[i].add(u)

    # calculate co-rated items between users
    C = dict()
    N = dict()
    for i, users in item_users.items():
        for u in users:
            N.setdefault(u, 0)
            N[u] += 1
            C.setdefault(u, {})
            for v in users:
                if u == v:
                    continue
                C[u].setdefault(v, 0)
                C[u][v] += 1 / math.log(1+len(users))

    # calculate finial similarity matrix W
    W = C.copy()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    return W


def Recommend(user, train, W, K=80):
    rank = dict()
    interacted_items = train[user]
    for v, wuv in sorted(W[user].items(), key=operator.itemgetter(1),
                         reverse=True)[0:K]:
        for i, rvi in train[v].items():
            # we should filter items user interacted before
            if i in interacted_items:
                continue
            rank.setdefault(i, 0)
            # print(wuv, rvi[0])
            rank[i] += wuv * 1
    return rank


def Recommendation(users, train, W, top=10, K=80):
    result = dict()
    for user in users:
        rank = Recommend(user, train, W, K)
        R = sorted(rank.items(), key=operator.itemgetter(1),
                   reverse=True)[: top]
        result[user] = R
    return result
