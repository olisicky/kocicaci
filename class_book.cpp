# include <iostream>
#include<windows.h>

using namespace std;

class Book {
    public:
        string title;   // atributy knihy
        string author;
        int pages;
        //Tohle je constructor function, která bude vždy zavolána při využití té class
        Book(string name){ // mohu mu nastavit i vstupn9 veličiny, které zadává uživatel!!
            cout << "NEčum, tohle je constructor" << name << endl;
        }

};

int main()
{
    // musím první vytvořit knihu, kterou jsem si nadefinoval jako nový data type!
    Book book1("šlompa"); //Book je zde právě ten data type, který vyvářím a navíc mu dávám parameter pro constructor function!
    book1.title = "Harry Potter";
    book1.author = "JK Rowling";
    book1.pages = 500;

    cout << book1.title;
    return 0;
}
