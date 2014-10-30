#!/usr/bin/env python
"""
PLG data model for students and courses
"""

class Student:
    """A student"""
    pass
    

class Course:
    """A body of knowledge taught by a school."""
    pass
    

class CourseOffering:
    """An offering of a course in a particular session"""
    pass
    

class CourseSection:
    """one section of a course in a session"""
    pass
    
    
class AcademicSession:
    """A period within a term during which courses are offered"""
    
    def __init__(self,term,name=None):
        """constructor
        
        >>> term=AcademicTerm(name='Fall',year=2014)
        >>> session=AcademicSession(name="Regular Academic Session",term=term)
        >>> session.name
        'Regular Academic Session'
        >>> isinstance(session.term,AcademicTerm)
        True
        
        >>> session=AcademicSession(name="Regular Academic Session",term="Fall 2014")
        Traceback (most recent call last):
        TypeError: 'term' must be an instance of type AcademicTerm
        
        >>> session=AcademicSession(term=term)
        Traceback (most recent call last):
        ValueError: 'name' is a required attribute
        
        """
        if (name is not None):
            self.name=name
        else:
            raise ValueError("'name' is a required attribute")
        if (isinstance(term,AcademicTerm)):
            self.term=term
        else:
            raise TypeError("'term' must be an instance of type AcademicTerm")
        


class AcademicTerm:
    """The largest portion of the academic calendar"""
    
    def __init__(self,name=None,year=None):
        """constructor
        
        >>> term=AcademicTerm("Fall",2014)
        >>> term.name
        'Fall'
        >>> term.year
        2014
        
        >>> term2=AcademicTerm(year=2014)
        Traceback (most recent call last):
        ValueError: 'name' is a required attribute
        
        >>> term3=AcademicTerm(2014,"Fall")
        Traceback (most recent call last):
        TypeError: 'year' must be an integer: Fall
        """
        if (name is not None):
            self.name=name
        else:
            raise ValueError("'name' is a required attribute")
        if (isinstance(year,int)):
            self.year=year
        else:
            raise TypeError("'year' must be an integer: %s" % year)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
