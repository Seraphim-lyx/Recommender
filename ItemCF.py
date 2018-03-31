# -*- coding: utf-8 -*-
"""

"""

import math
import operator


def Similarity(train):
    # calculate co-rated users between items
    C = dict()
    N = dict()
    for u, items in train.items():
        for i in items:
            N.setdefault(i, 0)
            N[i] += 1
            C.setdefault(i, {})
            for j in items:
                if i == j:
                    continue
                C[i].setdefault(j, 0)
                C[i][j] += 1

    # calculate finial similarity matrix W

    W = C.copy()
    for i, related_items in C.items():
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])

        m = max(W[i].values())

        for j in W[i].keys():
            W[i][j] = W[i][j] / m

    # for i, j in W.items():
    #     for k, w in j.items():
    #         W[i][k] = w / m

    return W


def Recommend(user_id, train, W, K=3):
    rank = dict()
    ru = train[user_id]
    for i, pi in ru.items():
        for j, wij in sorted(W[i].items(),
                             key=operator.itemgetter(1), reverse=True)[0:K]:
            if j in ru:
                continue
            rank.setdefault(j, 0)
            rank[j] += 1 * wij
    return rank


# class Node:
#    def __init__(self):
#        self.weight = 0
#        self.reason = dict()
#
# def Recommend(user_id,train, W,K =3):
#    rank = dict()
#    ru = train[user_id]
#    for i,pi in ru.items():
#        for j,wij in sorted(W[i].items(), \
#                           key = operator.itemgetter(1), reverse = True)[0:K]:
#            if j in ru:
#                continue
#            if j not in rank:
#                rank[j] = Node()
#            rank[j].reason.setdefault(i,0)
#            rank[j].weight += pi * wij
#            rank[j].reason[i] = pi * wij
#    return rank

def Recommendation(users, train, W, top, K=3):
    result = dict()
    for user in users:
        rank = Recommend(user, train, W, K)
        R = sorted(rank.items(), key=operator.itemgetter(1),
                   reverse=True)[:top]
        result[user] = R
    return result
