from Variable01 import Variable
import numpy as np

class Function:
    def __call__(self, input):
        x = input.data
        y = x**2
        output = Variable(y)
        return output


if __name__ == "__main__":
    x = Variable(np.array(10))
    f = Function()
    y = f(x)
    print(type(y))
    print(y.data)