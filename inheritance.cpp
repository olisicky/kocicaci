# include <iostream>
#include<windows.h>

using namespace std;

// První class, která mi něco definuje.
class Chef {
    public:
        void makeChicken(){
            cout << "The chef makes chicken" << endl;
        }
        void makeSalad(){
            cout << "The chef makes salad" << endl;
        }
        void makeSpecialDish(){
            cout << "The chef makes bbq ribs" << endl;
        }

};

class ItalianChef : public Chef{    // Tady právě využívám inheritance, protože říkám, kterou class může využít!

};
int main(){
    Chef chef;
    chef.makeChicken();
    ItalianChef italianChef;
    italianChef.makeChicken();  // jelikož jsem tu class ItalianChef propojil, tak mohu využívat její atribiuty, i když nejsou nadefinovány!!!
    return 0;
}
