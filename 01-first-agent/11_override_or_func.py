
class MySequence:
    def __init__(self, *args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)
    def __or__(self, other):
        self.sequence.append(other)
        return self
    def run(self):
        for arg in self.sequence:
            print(arg)

class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return f'name: {self.name} age: {self.age}'
    def __or__(self, other):
        return MySequence(self, other)

if __name__ == '__main__':
    a = MyClass("Iverson", 52)
    b = MyClass("wade", 45)
    c = MyClass("james", 42)

    d = a | b | c
    d.run()