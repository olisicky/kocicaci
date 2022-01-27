# include <iostream>
#include<windows.h>

using namespace std;

class Student {
    private:    // tohle je privátní  nemohu se k tomu dostat ve zbytku dódu jako k atributu!
        string gender;  // normálně to může át vstup pro constructor!
    public: // vše co je pod public je veřejné a mohu se k tomu dostat!! Student.name() !!
        string name;   // atributy studenta
        string major;
        double gpa;
        // vytvoření constructor function
        Student (string aName, string aMajor, double aGPA, string aGender){
            name = aName;
            major = aMajor;
            gpa = aGPA;
        }
        // Vytvoření object function naší class Student
        bool hasHonors(){
            if (gpa >= 3.5){
                return true;
            }
            return false;
        }
        // vytvořil jsem jenom zbytečnou funkci, kam mi ale půjde právě ten nastavená atribut a tím jej mohu řídit! Ten vstup je
        // private, takže se k němu nedostanu, ale mohu pomocí této funkce kontrolovat jaké vstupy jsou validní!
        void setGender(string aGender){
            if (aGender == "male" || aGender =="female"){   // takhle jsem podmínil možné vstupy pro parametr gender
                gender = aGender;
            } else {
                gender = "No proper gender";
            }
        }
        // jenom kontrolní funkce, abych si ověřil gender, protože se k tomu atributu nedostanu!
        string printGender(){
            return gender;
        }

};

int main(){
    Student student1("Ondra Lisický", "Engineering", 1.0, "male");
    student1.setGender("bisexual");
    cout <<student1.name<< endl;
    cout << student1.hasHonors()<< endl;   //zde aplikuji object function na náš objekt studenta
    cout << student1.printGender();

    return 0;
}
