import sys

class Person():
    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname
    def give_name(self):
        return print(f'You are {self.name}')
    def give_lastname(self):
        return print(f'Your last name is {self.lastname}')

class Child(Person):
    ''' Nová třída, která dědí vlastnosti ze třídy Person. Zde to je hlavně attribut name a lastname '''
    def __init__(self, name, lastname, age):
        super().__init__(name, lastname)    # zde nesmí být self, protože dědím z jiné třídy! Navíc zde musím specifikovat, které attributy chci dědit. U metod to není třeba.
        self._age = age
    @property    # Tohle je getter pro třeba attribut, který by neměl být veřejný
    def age(self):
        return self._age
    @age.setter    # zde vytvořím setter (mohu jej tedy nastavit přes object.age = xx) + Navíc kontroluji správnost toho zadání
    def age(self, newage):
        if newage >0:
            self._age = newage
        else:
            raise ValueError('Age should be a positive value only.')
    def give_age(self):
        return print(f'You are {self._age} years old')
    # Zkouška využití staticmethod. Výhoda je asi, že je to nějak spjato s tím objektem a nemusí to ležet mimo, takže je to "uspořádanější" ?
    @staticmethod
    def static():
        print('Print something')
 
if __name__ == '__main__':
    neco = Child(sys.argv[1], sys.argv[2], sys.argv[3])
    neco.give_name()
    neco.give_lastname()
    neco.give_age()
    neco.age = -25
    neco.give_age()
    neco.static()
    Child.static()    # Nemusím vytvořit objekt, abych využil tu metodu, která byla dekorována pomocí @staticmethod