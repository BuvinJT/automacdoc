#import numpy as np

#from six import add_metaclass
#from abc import ABCMeta, abstractmethod 

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

#@add_metaclass(ABCMeta)
class _Animal: 
    """Protected base class"""
    _instance_counter=0
    
    def __init__(self):
        _Animal._instance_counter += 1
        
    #@abstractmethod
    def _live( self ): """ABSTRACT"""                

    #@abstractmethod
    def _die( self ): """ABSTRACT"""                

class Fish( _Animal ):
    """An animal which lives under water..."""

    def __init__(self, name:str="?"):
        """Initialize a Fish

        **Parameters**

        > **name:** `str` -- Name of the Fish.

        """
        self.name=name
        """The name helps us to identify the particular animal."""
 
    def breathe_h2o( self ):
        """This is a big part of what a fish does."""
        print("I'm trying to breathe here!")    

    def _live( self ): 
        """Fish definition"""
        self.breathe_h2o()                

    def _die( self ):                 
        """Fish definition"""
        self.name=None                
 
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
        Fish.__init__( self, name )
            
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

