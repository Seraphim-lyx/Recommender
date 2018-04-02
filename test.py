from collections import Counter
import numpy as np
import operator
import matplotlib.pyplot as plt
import ItemCF
from pylab import *
import matplotlib.ticker as mtick
# a = {key: value/m for key, value in a.items()}
x = ['10','20','40','80','160']
y_ = [3,5,7,8,3]
y = [50.3232,10.32134,30.3143214,40.34214,50.34241]

f = open('output.txt', 'w')
f.writelines('abc\n')
f.writelines('bcd')
f.close()