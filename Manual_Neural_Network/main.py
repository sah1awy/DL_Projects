from Operation import *

g = Graph()
g.set_as_default()
A = Variable(10)
b = Variable(1)
x = Placeholder()
y = multiply(A,x)
z = add(y,b)
sess = Session()
result = sess.run(operation=z,feed_dict={x:10})
print(result)
g = Graph()

g.set_as_default()

A = Variable([[10,20],[30,40]])
b = Variable([1,1])

x = Placeholder()

y = matmul(A,x)

z = add(y,b)
sess = Session()
result = sess.run(operation=z,feed_dict={x:10})
print(result)
x = np.linspace(0,11,10)
y = -x + 5
g = Graph()
g.set_as_default()
x = Placeholder()
w = Variable([1,1])
b = Variable(-5)
z = add(matmul(w,x),b)
a = Sigmoid(z)
sess = Session()
print(sess.run(operation=a,feed_dict={x:[8,10]}))
print(sess.run(operation=a,feed_dict={x:[0,-10]}))
