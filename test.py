from collections import Counter
import operator
c = {'a': 1, 'b': 2}

a = {'c': 3, 'a': 4}

co = Counter(a) + Counter(c)
print(dict(co))
