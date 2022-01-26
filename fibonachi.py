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