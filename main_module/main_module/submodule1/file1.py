def hello(y, x, z=1, **kwargs):
    print('hello')
    print(kwargs)
    return x + 2*y + 3*z

def bonjour(x):
    print('bonjour')
    return x

class Hallo():
    def __init__(self, name):
        self.name = name

        self.polite('!')

    def __repr__(self):
        return "My name is " + self.name

    def polite(self, toto, t=3, **kwargs):
        self.sentence = "Hallo " + self.name + " " + toto
        return "Welcome to my nice hotel, Mr " + toto
    
    def test(self):
        return self.name