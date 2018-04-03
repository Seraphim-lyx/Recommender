import UserTimeCF
import operator
from collections import Counter


class GeoCF(object):
    """docstring for GeoCF"""

    def __init__(self, algo):
        self.grank = {}
        self.algo = algo
        self.readZip()

    def readZip(self, filename='movielens/u.user'):
        self.uzip = {}
        with open(filename) as f:
            for line in f.readlines():
                l = line.strip('\n').split('|')
                self.uzip.setdefault(l[0], 0)
                self.uzip[l[0]] = l[4]

    def getZipList(self, userid, num):
        # if num is 0:
        #     num = None
        z = self.uzip[userid][:num]
        return [key for key, value in self.uzip.items()
                if value[:num] == z]
        # return self.uzip[userid][:num]

    def getSubTrain(self, train, zipList):
        sub = {}
        for z in zipList:
            sub[z] = train[z]
        return sub

    def rankCombine(self, ranklist, rank):
        # W = self.algo.Similarity(train)
        # rank = self.algo.Recommend('1', train, W)
        # print(sorted(rank.items(), key=operator.itemgetter(1), reverse=True))
        return dict(Counter(ranklist) + Counter(rank))

    def geoCalculate(self, weight):
        pass

    def recommend(self, user, train, k):
        weight = [0.2,0.3,0.5]
        ranklist = {}
        for i in range(len(weight)):

            zipList = self.getZipList(user, i+1)
            subtrain = self.getSubTrain(train, zipList)
            W = self.algo.Similarity(subtrain)
            rank = self.algo.Recommend(user, subtrain, W, k)
            rank = {k:v*weight[i] for k, v in rank.items()}
            ranklist = self.rankCombine(ranklist, rank)
        return ranklist

    def recommendation(self, users, train, top=10, k=3):
        result = {}
        for u in users:
            print(u)
            ranklist = self.recommend(u, train, k)
            result[u] = sorted(ranklist.items(), key=operator.itemgetter(1),
                               reverse=True)[:top]
        return result


# obj = GeoCF(UserTimeCF)
# obj.readZip('movielens/u.user')
# print(sorted(obj.uzip))
# print(len(obj.getZipList('1', 0)))
