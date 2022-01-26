# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 16:12:27 2022

@author: lisicky
"""
# ============================== inheritance =================================
class Person():
    def __init__(self, jmeno):
        self.jmeno = jmeno
class child(Person):
    
    def __init__(self, jmeno): 
        Person.jmeno = jmeno
    def display(self):
        print(Person.jmeno)

vla = child("nečum")
vla.display()


class Person():
    def __init__(self, jmeno):
        self.jmeno = jmeno
class child(Person):
    
    def __init__(self, jmeno): 
        super(child, self).__init__(jmeno)
    def display(self):
        print(self.jmeno)

vla = child("nečum")
vla.display()



# Driver Code
obj = child("Interviewbit")
obj.display()


x = person()
print(x.print_name("Ondřej", "Lisický"))
print(x.name_inverted())