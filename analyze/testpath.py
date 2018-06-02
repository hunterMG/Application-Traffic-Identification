import os

file = './1/cat.jpg'
full_name = os.path.split(file)[-1]
print(full_name)
name = os.path.splitext(full_name)[0]
name = name + '.npy'
print(name)