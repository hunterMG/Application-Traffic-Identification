#%%
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(0, 20, 100)
plt.plot(x, np.sin(x))
plt.show() 
#%%
for i in range(3):
    print(i)

#%% one hot encoding with Keras
from numpy import array
from numpy import argmax
from keras.utils import to_categorical
# define example
data = [1, 3, 2, 0, 3, 2, 2, 1, 0, 1]
data = array(data)
print(data)
# one hot encode
encoded = to_categorical(data)
print(encoded)
# invert encoding
inverted = argmax(encoded[0])
print(inverted)

#%% One-Hot Encode with scikit-learn：
from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
# define example
data = ['cold', 'cold', 'warm', 'cold', 'hot', 'hot', 'warm', 'cold', 'warm', 'hot']
values = array(data)
print(values)
# integer encode
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(values)
print(integer_encoded)
# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
print(onehot_encoded)
# invert first example
inverted = label_encoder.inverse_transform([argmax(onehot_encoded[0, :])])
print(inverted)

#%% One-Hot encode
from numpy import argmax
# define input string
data = 'hello world'
print(data)
# define universe of possible input values
alphabet = 'abcdefghijklmnopqrstuvwxyz '
# define a mapping of chars to integers
char_to_int = dict((c, i) for i, c in enumerate(alphabet))
print(char_to_int)
int_to_char = dict((i, c) for i, c in enumerate(alphabet))
# integer encode input data
integer_encoded = [char_to_int[char] for char in data] # 获得对data编码的list
print(integer_encoded)
# one hot encode    
onehot_encoded = list()
for value in integer_encoded:
       letter = [0 for _ in range(len(alphabet))]   # 生成一个全0的list
       letter[value] = 1
       onehot_encoded.append(letter)
print(onehot_encoded)   # 对data的编码结果
# invert encoding (从编码获取原字符)
inverted = int_to_char[argmax(onehot_encoded[0])]
print(inverted)

#%%
%matplotlib inline
from matplotlib import pyplot as plt
import numpy
x = numpy.linspace(0, 1, 1000)**1.5
plt.hist(x);

#%%
str = 'qwer'
s1 = set()
s1.add([c for i,c in enumerate(str)])
print(s1)

#%%
a = {1,2,3}
b = {4}
c = {5}
d = a|b|c
d

#%%
import numpy as np
a = np.array([[1,2],[3,4]])
print(type(a))
print(a*2)
c = np.ones(3)
print(c*2)