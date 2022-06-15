# I was not sure about the use of generators so I am trying it here as an example. As I understand, they are used like 
# iterators but the are not stored in memory. Therefore, one can acess some data or do something with them in a loop but 
# the data is generated at use and not stored in memory.

def generator(data):
    for ix, item in enumerate(data):
        item = f'{ix}th item vstupu je:' + item
        yield item

data = ['Ahoj', 'jak', 'se', 'máš', '?']


if __name__ == '__main__':
    for item in generator(data):
        print(item)
