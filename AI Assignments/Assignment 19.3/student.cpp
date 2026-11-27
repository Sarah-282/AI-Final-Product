#include <iostream>
#include <string>

class Student {
private:
    std::string name;
    int age;

public:
    Student(const std::string& studentName, int studentAge)
        : name(studentName), age(studentAge) {}

    void display() const {
        std::cout << "Name: " << name << '\n';
        std::cout << "Age: " << age << '\n';
    }
};

int main() {
    const Student student("Alice", 20);
    student.display();
    return 0;
}
