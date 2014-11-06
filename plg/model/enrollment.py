#!/usr/bin/env python
"""
PLG data model for students and courses
"""
import datetime

class Student:
    """A student"""
    def __init__(self,last_name,first_name,other_names=None,phone_number=None,email_address=None):
        """ constructor """
        self.last_name = last_name
        self.first_name = first_name
        self.other_names = other_names
        self.phone_number = phone_number
        self.email_address = email_address
        
    @property
    def preferred_first_name(self):
        """ Get the student's preferred first name.  If there is no preferred first name recorded, return the default first name.
        
        
        >>> student = Student('Kennedy','John')
        >>> student.preferred_first_name
        'John'
        >>> student.preferred_first_name = 'Jack'
        >>> student.preferred_first_name
        'Jack'
        """
        try:
            return self._preferred_first_name
        except AttributeError:
            return self.first_name
    
    @preferred_first_name.setter
    def preferred_first_name(self,value):
        self._preferred_first_name = value
    
    @property
    def formatted_full_name(self):
        """ 
        The formatted name as it might appear on a class list. 
        
        >>> student = Student('Kennedy','John')
        >>> student.formatted_full_name
        'Kennedy, John'
        >>> student.other_names = 'Fitzgerald'
        >>> student.formatted_full_name
        'Kennedy, John Fitzgerald'
        """
        value = '%s, %s' % (self.last_name, self.first_name)
        if self.other_names:
            value += ' ' + self.other_names
        return value
        
    @property
    def formatted_contact_name(self):
        """ The formatted name as it might appear on an envelope. 
        
        >>> student = Student('Kennedy','John')
        >>> student.formatted_contact_name
        'John Kennedy'
        >>> student.other_names = 'Fitzgerald'
        >>> student.formatted_contact_name
        'John Fitzgerald Kennedy'
        """
        names = [self.first_name]
        if self.other_names:
            names.append(self.other_names)
        names.append(self.last_name)
        return " ".join(names)             
                        

class Course:
    """A body of knowledge taught by a school."""
    
    def __init__(self,name,description):
        self.name = name
        self.description = description
    

class CourseOffering:
    """An offering of a course in a particular session"""
    
    def __init__(self,course,session):
        self.course = course
        self.session = session
    

class CourseSection:
    """
    one section of a course in a session
    
    >>> course_section = CourseSection(
    ...    offering=CourseOffering(
    ...        course=Course(
    ...            name='Calculus III',
    ...            description='Multivariable Calculus'),
    ...        session=AcademicSession(
    ...            name='Regular Academic Session',
    ...            start_date=datetime.date(2014,9,2),
    ...            end_date=datetime.date(2014,12,19),
    ...            term=AcademicTerm('Fall',2014))))
    >>> course_section.course_name
    'Calculus III'
    >>> course_section.course_description
    'Multivariable Calculus'
    >>> course_section.session_name
    'Regular Academic Session'
    >>> course_section.session_start_date.strftime('%Y-%m-%d')
    '2014-09-02'
    >>> course_section.session_end_date.strftime('%Y-%m-%d')
    '2014-12-19'
    >>> course_section.term_name
    'Fall'
    >>> course_section.term_year
    2014
    """
    
    def __init__(self,offering,name=None):
        self.offering = offering
        self.name = name
    
    @property
    def course_name(self):
        return self.offering.course.name
        
    @property
    def course_description(self):
        return self.offering.course.description
        
    @property
    def session_name(self):
        return self.offering.session.name
    
    @property
    def session_start_date(self):
        return self.offering.session.start_date
    
    @property
    def session_end_date(self):
        return self.offering.session.end_date
        
    @property
    def term_name(self):
        return self.offering.session.term.name
        
    @property
    def term_year(self):
        return self.offering.session.term.year
    
    
class AcademicSession:
    """A period within a term during which courses are offered"""
    
    def __init__(self,term,start_date,end_date,name=None):
        """constructor
        """
        if (name is not None):
            self.name=name
        else:
            raise ValueError("'name' is a required attribute")
        self.start_date = start_date
        self.end_date = end_date
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
            

class Roster:
    """ The list of students in a section of a course.
    
    >>> roster = Roster()
    >>> roster.add_student(Student('Kennedy','John',
    ...     email_address='jfk35@harvard.edu'))
    >>> roster.add_student(Student('Adams','John','Quincy',
    ...     email_address='jqa6@harvard.edu'))
    >>> student = roster.lookup_student('email_address','jqa6@harvard.edu')
    >>> student.other_names
    'Quincy'
    """
    
    def __init__(self,section=None,students=None):
        self.section = section
        if students is None:
            self.students = []
        else:
            self.students = students
        self._index = {}
        
    def add_student(self,student):
        """
        Add a student to the roster.  
        
        For each indexed field, add an entry to the index on that field.
        """
        self.students.append(student)
        for field in self._index:
            self._index[field][getattr(student,field)] = student
        
    def add_index(self,field):
        """
        Add an index on the field given.
        """
        if not (field in self._index):
            self._index[field] = {}
        for student in self.students:
            self._index[field][getattr(student,field)] = student
                
    def lookup_student(self,field,value):
        if not (field in self._index):
            self.add_index(field)
        return self._index[field][value]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
