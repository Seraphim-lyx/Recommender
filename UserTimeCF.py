# -*- coding: utf-8 -*-
"""

"""

import math
import operator


def Similarity(train):
    # build inverse table for item_users
    item_users = dict()
    for u, items in train.items():
        for i, item in items.items():
            if i not in item_users:
                item_users[i] = dict()
            # print(u)
            item_users[i][u] = item[1]  # time

    # calculate co-rated items between users
    C = dict()
    N = dict()
    alpha = 0.0001
    for i, users in item_users.items():
        # print(users)
        for u, ut in users.items():
            N.setdefault(u, 0)
            N[u] += 1
            C.setdefault(u, {})
            for v, vt in users.items():
                if u == v:
                    continue
                C[u].setdefault(v, 0)
                # penalize time distance
                C[u][v] += 1 / (1 + alpha * abs(int(ut) - int(vt)))
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


def Recommendation(users, train, W, K=10):
    result = dict()
    for user in users:
        rank = Recommend(user, train, W, K)
        R = sorted(rank.items(), key=operator.itemgetter(1),
                   reverse=True)
        result[user] = R
    return sorted(result)
