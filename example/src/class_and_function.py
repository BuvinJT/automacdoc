#import numpy as np


def maxi(x: int, y: int = 5):
    """
    Take the max between two numbers

    **Parameters**

    > **x:** `float` -- Description of parameter `x`.

    > **y:** `float` -- Description of parameter `y`.

    **Returns**

    > `float` -- Description of returned object.
    """
    #return np.max(x, y)
    return x


def maxi2pourvoir(x, y):
    """
    Take the max between two numbers

    **Parameters**

    > **x:** `float` -- Description of parameter `x`.

    > **y:** `float` -- Description of parameter `y`.

    **Returns**

    > `float` -- Description of returned object.
    """
    #return np.max(x, y)
    return x

class Shark:

    SMALL, MEDIUM, LARGE = range(3)
    
    class Type: White, Hammerhead, Mako = range(3)
    
    _counter=0
    __current=None

    @staticmethod
    def swimstatic(a):
        """
        Teach them how to swim

        **Parameters**

        > **a:** `obj` -- Instance of `Shark`.

        **Returns**

        > `bool` -- Did they succeed.
        """
        print('prout')
        print("The shark is swimming.")
        for i in range(2):
            print("lololo")
        return

    @classmethod
    def swimclass(cls, lessons):
        """
        Teach them how to swim

        **Parameters**

        > **lessons:** `list` -- `Lessons` to take teach.

        **Returns**

        > `bool` -- Did they succeed.
        """
        print('prout')
        print("The shark is swimming.")
        for i in range(2):
            print("lololo")
        return

    def __init__(self, name:str="?"):
        """
        Initialize a Shark

        **Parameters**

        > **name:** `str` -- Name of the Shark.

        """
        self.name=name
        self._protected_name=name+'-pro'
        self.__private_name=name+'-pri'
        self.favorite_food=None
                
    def be_awesome(self):
        """
        Do what sharks do

        **Parameters**

        > **self:** `obj` -- Instance of `Shark`.
 
        **Returns**

        > `None`
        """
        print("The shark is being awesome.")
