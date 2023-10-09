##python 类和对象
class Cat:
   def __init__(self, name, age):
       self.name = name
       self.age = age
       print("初始化")

   def eat(self):
    print(self.name + "吃东西")

##类的方法相当于java的静态方法,但是拿不到self
   def work():
    print("11111")

   # def test():
   #  print(self.name)


########################

test1 = Cat("小黄",2)
test1.eat()
Cat.work()
#Cat.test()

## 设置属性
a = test1.name
print(a)
test1.name = "小黑"
b= test1.name
print(b)

