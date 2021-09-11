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

class Animal: pass

class Fish( Animal ): pass

class Shark( Fish ):
    """
    A very cool fish!
    """

    SMALL, MEDIUM, LARGE = range(3)
    """A constant used to represent size."""
    
    class Type: White, Hammerhead, Mako = range(3)
    
    shark_counter=0
    """This is a static counter, keeping track of how many sharks exist."""
    
    _sleeping_counter=0
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
        """The name helps us to identify the particular animal."""
        
        self._protected_name=name+'-pro'
        self.__private_name=name+'-pri'
        
        self.favorite_food=None
        """
        The attribute `favorite_food` is optional.
        You may assign its value post construction.
        Example:
        
            man_eater = Shark( "Jaws" )
            man_eater.favorite_food = "humans"
        """
                
    def be_awesome(self):
        
        """
        Do what sharks do

        **Parameters**

        > **self:** `obj` -- Instance of `Shark`.
 
        **Returns**

        > `None`
        """
        
        # this comment should be the first line line in the docs source code 
        print("The shark is being awesome.")
        """
        This comment should remain visible the in docs source code too! 
        """

