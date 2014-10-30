#!/usr/bin/env python

import logging

def debug_entry(f):
    """
    debug the entry into a function
        
    >>> import sys
    >>> import logging
    
    The stream configuration is just to make doctests work.  
    In practice, you'd probably want the default stream sys.stderr.
    >>> logging.basicConfig(level=logging.DEBUG,stream=sys.stdout)

    >>> @debug_entry
    ... def f(x):
    ...     return x*x
    ...
    >>> f(2)
    DEBUG:f:Entering: arguments=(2,), keyword arguments={}
    4
    """
    def new_f(*args,**kwargs):
        logger=logging.getLogger(f.__name__)
        logger.debug("Entering: arguments=%s, keyword arguments=%s",args,kwargs)
        return f(*args,**kwargs)
    new_f.__name__ = f.__name__
    return new_f
    
def debug_result(f):
    """
    Debug the result of a function
    
    >>> import sys
    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG,stream=sys.stdout)
    >>> @debug_result
    ... def f(x):
    ...     return x*x
    ...
    >>> f(2)+10
    DEBUG:f:Result: 4
    14
    
    Decorators can be chained (that's kind of the point!).
    
    >>> @debug_entry
    ... @debug_result
    ... def g(x):
    ...    return 2*x
    ...
    >>> g(3)+17
    DEBUG:g:Entering: arguments=(3,), keyword arguments={}
    DEBUG:g:Result: 6
    23
    """
    def new_f(*args,**kwargs):
        logger=logging.getLogger(f.__name__)
        result=f(*args,**kwargs)
        logger.debug("Result: %s",repr(result))
        return result
    new_f.__name__ = f.__name__
    return new_f
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # from decorators import *
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    # @debug_result
    # @debug_entry
    # def f(x):
    #    return x*x 
    #    
    #f(2)