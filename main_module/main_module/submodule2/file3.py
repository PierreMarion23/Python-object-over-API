def hello(y, x, z=1, **kwargs):
    print('hello')
    print(kwargs)
    return x + 2*y + 3*z

def bonjour(x):
    print('bonjour')
    return x