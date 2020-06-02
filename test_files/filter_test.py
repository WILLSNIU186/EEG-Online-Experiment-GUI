from numpy import array, ones
from scipy.signal import lfilter, lfilter_zi, butter
import matplotlib.pyplot as plt
import  numpy as np

b, a = butter(2, 0.25)
zi = lfilter_zi(b, a)
print('zi:', zi)
y, zo = lfilter(b, a, ones(10), zi=zi)
print('zo', zo)
print(y)
plt.plot(list(range(0,10)), y)
plt.show()