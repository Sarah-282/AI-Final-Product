class Student:
    def __init__(self, name: str, age: int) -> None:
        self.__name = name
        self.__age = age

    def display(self) -> None:
        print(f"Name: {self.__name}")
        print(f"Age: {self.__age}")


if __name__ == "__main__":
    student = Student("Alice", 20)
    student.display()
