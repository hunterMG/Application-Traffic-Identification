#!/home/yg/.local/share/virtualenvs/Application-Traffic-Identification-8Rjd059g/bin/python

import tensorflow as tf
hello = tf.constant("Hello, TensorFlow!")
sess = tf.Session()
print(sess.run(hello))