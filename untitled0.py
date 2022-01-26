# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 16:12:27 2022

@author: lisicky
"""

def bla ():
    pass


class Person():
    def __init__(self, jmeno):
        self.jmeno = jmeno
class child(Person):
    
    def _init__(self, jmeno): 
        Person.jmeno = jmeno
        
    def display(self):
        print(Person.jmeno)

vla = child("nečum")
vla.display()


class Parent():
    def __init__(self, jmeno):
        self.jmeno = jmeno
class child(Parent): 
   # Constructor
   def __init__(self, jmeno):
       Parent.jmeno = jmeno
 
   def display(self):
       print(Parent.jmeno)
 
# Driver Code
obj = child("Interviewbit")
obj.display()


x = person()
print(x.print_name("Ondřej", "Lisický"))
print(x.name_inverted())


a,b, = 0,1

for i in range(10):
    print(a)
    a,b = b, a+b
    
    
for i in range(101):
    if i % 3 ==0:
        print ("fizz")
    elif i % 5 == 0 :
        print("Buzz")
    elif i % 3 == 0 and i % 5 == 0:
        print("Fizz Buzz")
    else:
        print(i)