# include <iostream>
#include<windows.h>

using namespace std;

class Book {
    public:
        string title;   // atributy knihy
        string author;
        int pages;
        // vytvoření dvou contructor fukcí, aby měl uživatel možnost zadat více způsoby
        Book (){
            title = "no title";
            author = "no author";
            pages  = 0;
        }
        //Tohle je constructor function, která bude vždy zavolána při využití té class
        Book(string par1, string par2, int par3){ // mohu mu nastavit i vstupn9 veličiny, které zadává uživatel!!
            title = par1;   // přiřadím ten parametr constructor funkce pro atribut class knihy, kterou jsem vytvořil.
            author = par2;
            pages = par3;
        }

};

int main()
{
    // musím první vytvořit knihu, kterou jsem si nadefinoval jako nový data type!
    Book book1("Cripled god", "Erickson", 800 ); //Book je zde právě ten data type, který vyvářím a navíc mu dávám parameter pro constructor function!
    cout << book1.title;    // zdeuž si právě vypisuji atribut class, který byl nastaven jako title.
    return 0;
}
