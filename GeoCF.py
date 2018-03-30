import UserTimeCF
import operator
from collections import Counter


class GeoCF(object):
    """docstring for GeoCF"""

    def __init__(self, algo):
        self.grank = {}
        self.algo = algo

    def readZip(self, filename):
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
                if userid is not key and value[:num] is z]
        # return self.uzip[userid][:num]

    def getSubTrain(self, train, zipList):
        sub = {}
        for z in zipList:
            if z in train:
                sub.setdefault(z, train[z])
        return sub

    def rankCombine(self, train):
        W = self.algo.Similarity(train)
        rank = self.algo.Recommend('1', train, W)
        print(sorted(rank.items(), key=operator.itemgetter(1), reverse=True))
        # self.grank = dict(Counter(self.grank) + Counter(rank))

    def geoCalculate(self, weight):
        pass

    def recommend(self, user, train, W):
        for i in range(4):
            ziplist = self.getZipList(user, i)
            subtrain = self.getSubTrain(train, zipList)
            W = self.algo.Similarity(subtrain)
            rank = c.Recommend('3', subtrain, W)
            self.resultCombine(rank)


# obj = GeoCF()
# obj.readZip('movielens/u.user')
# print(sorted(obj.uzip))
# print(len(obj.getZipList('1', 0)))
