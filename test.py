list = [ 'abcd', 786 , 2.23, 'john', 70.2 ]

print(list[1:3])

dict = {}
dict['one'] = 1
dict[2] = "two"

print(dict)
print(dict.keys())
print(dict.values())

print(1 in dict)
print(2 in dict)

a = 60
b = 13

print(a&b)
print(~b)

a = 'asjdbawabr'
b = a
c = 'asjdbawabr'

print(a is c)
print(a is b)
print(id(a),id(b),id(c))

a = 3
mystr = f"{a:02d}"
print(mystr)

b = 3.14253
print(f"asdasd : {b:.7f}")
a,b,c = [1,2,3]

print(a,b,c)

data = {}

ret = data.setdefault('a', 0)    # key로 'a'를 추가학 value 0을 설정함, setdefault는 현재 value 값을 리턴
print(ret, data)

ret = data.setdefault('a', 1)   # 이미 key가 있는 경우 setdefault 현재 value 값을 리턴
print(ret, data)

def hello():
    print("hello")

f = hello()
f

def foo(a, b, c):
    print(a, b, c)



a = lambda x : 5 * x
print(a(2))

def outer():
    num = 3
    def inner():
        print(num)
    return inner

f = outer()
f()

print(type(f.__closure__))    # 튜플
print(type(f.__closure__[0]))   # cell
#print(dir(f.__closure__[0]))

print("==========")

def outer(num):
    def inner():
        print(num)
    return inner

#f = outer()
#f(3)

outer(3)



class Stock:
    def __getattribute__(self, item):
        print(item, "객체에 접근하셨습니다.")


s = Stock()
s.hello

from abc import *


class Car(metaclass=ABCMeta):
    @abstractmethod
    def drive(self):
        pass


class K5(Car):
    def drive(self):
        print("k5 drive")

k5 = K5()
k5.drive()

print("hello")

print("a")
