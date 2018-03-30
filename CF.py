class CF(object):
    """docstring for CF"""

    def __init__(self, arg):
        pass

    def Recommend(user_id, train, W, K=3):
        pass

    def Recommendation(users, train, W, K=10):
        result = dict()
        for user in users:
            rank = Recommend(user, train, W, K)
            R = sorted(rank.items(), key=operator.itemgetter(1),
                       reverse=True)
            result[user] = R
        return result
