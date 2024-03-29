#!/usr/bin/env python
"""
Process a roster downloaded from Albert and generate a list of fields for an Acrobat combo box.

To create the source file:

  * login to Albert, choose a course, and select "class roster"
  * select "view photos in list"
  * select "view all"
  * save this page, including the frames and photos.  In Chrome, use
    the "Webpage, complete" option when saving to do this.
  * change to the created directory (it will likely end in `_files`) and locate the roster file.
    It will probably be called "SA_LEARNING_MANAGEMENT.SS_CLASS_ROSTER.html"
  
Then run this script on that file.  

"""

from HTMLParser import HTMLParser
from htmlentitydefs import entitydefs
import re
import vobject # http://vobject.skyhouseconsulting.com/

import logging
import argparse

class AlbertHTMLParser(HTMLParser,object):
	student_keys_dict={
		'CLASS_ROSTER_VW_EMPLID'     : 'id',
		'HCR_PERSON_NM_I_NAME'       : 'name',
		'DERIVED_SSSMAIL_EMAIL_ADDR' : 'email',
		'SCC_PREF_PHN_VW_PHONE'      : 'phone',
		'PROGPLAN'                   : 'progplan',
		'PROGPLAN1'                  : 'level',
		'PSXLATITEM_XLATLONGNAME'    : 'status'
	}
	course_keys_dict={
		'DERIVED_SSR_FC_SSR_CLASSNAME_LONG' : 'code',
		'DERIVED_SSR_FC_SSS_PAGE_KEYDESCR2' : 'description',
		'DERIVED_SSR_FC_DESCR254'           : 'name',
		'MTG_INSTR$0'                       : 'instructor',
		'MTG_SCHED$0'                       : 'schedule',
		'MTG_LOC$0'                         : 'room',
		'MTG_DATE$0'                        : 'dates'
	}

	def __init__(self):
		HTMLParser.__init__(self)
		self.course_data={}
		self.student_data={}
		# parsing state variables
		self.current_key=""
		self.current_index=0
		self.data=""
		self.state='SEEKING_ID'
		self.data_dest=''

	def handle_starttag(self,tag,attrs):
		for attr in attrs:
			(name,value) = attr
			if name == 'id':
				logging.debug("parsing id %s" % value)
				match=re.match("([^$]*)\$(\d+)$",value)
				if (value in self.course_keys_dict):
					logging.debug("key %s is in course dictionary",value)
					self.current_key=self.course_keys_dict[value]
					self.state='SEEKING_DATA'
					self.data_dest='COURSE'
				elif match:
					(key,index)=match.group(1,2)
					logging.debug("key=%s",key)
					if (key in self.student_keys_dict):
						logging.debug("key %s is in student dictionary",key)
						self.current_key=self.student_keys_dict[key]
						self.current_index=int(index)
						self.state='SEEKING_DATA'
						self.data_dest='STUDENT'
					elif key == 'win0divEMPL_PHOTO_EMPLOYEE_PHOTO':
						self.current_index=int(index)
						self.state='SEEKING_STUDENT_IMG'
					else:
						logging.debug("ignoring key %s",key)
				else:
					logging.debug("id doesn't match, moving on")
		if (tag == 'img' and self.state=='SEEKING_STUDENT_IMG'):
			for attr in attrs:
				(name,value)=attr
				if name=='src':
					try:
						self.student_data[self.current_index]
					except KeyError:
						self.student_data[self.current_index] = {}
					self.student_data[self.current_index]['photo'] = value
			self.current_index=0					
			self.state='SEEKING_ID'
	
	def handle_data(self,data):
		if self.state == 'SEEKING_DATA':
			self.data += data
	
	def handle_charref(self,name):
		logging.debug("character ref: %s",name)
		
	def handle_entityref(self,name):
		# logging.debug("entity ref: %s",name)
		if (self.state == 'SEEKING_DATA'):
			if (name in entitydefs):
				self.data += entitydefs[name]
			
	def handle_endtag(self,tag):
		if self.state == 'SEEKING_DATA':
			# we're done
			if self.data_dest=='STUDENT':
				logging.debug("self.current_key=%s, self.current_index=%d",self.current_key,self.current_index)
				try:
					self.student_data[self.current_index]
				except KeyError:
					self.student_data[self.current_index] = {}
				self.student_data[self.current_index][self.current_key] = self.data
			elif self.data_dest=='COURSE':
				self.course_data[self.current_key] = self.data
			else:
				logging.error("Unknown data destination %s",self.data_dest)
			self.current_index=0
			self.current_key=""
			self.data=""
			self.data_dest=''
			self.state='SEEKING_ID'
			
	def parse(self,file):
		data = open(file, 'r').read()
		self.feed(data)
		return (self.course_data,self.student_data)

argparser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawTextHelpFormatter)
argparser.add_argument('--verbose',help='be verbose',
                    action='store_const',const=logging.INFO,dest='debug_level',
                    default=logging.WARNING)
argparser.add_argument('--debug',help='show debugging statements',
                    action='store_const',const=logging.DEBUG,dest='debug_level',
                    default=logging.WARNING)
argparser.add_argument('file',help='HTML file downloaded from Albert',
					action='store',
					default='Self Service Class Roster.html')
argparser.add_argument('--save',help='save vCards',
					action='store_const',const=True,dest='save',default=False)
argparser.add_argument('--print',help='pretty-print vCards',
					action='store_const',const=True,dest='bprint',default=True)
args = argparser.parse_args()
logging.basicConfig(level=args.debug_level)


parser=AlbertHTMLParser()
(course,students)=parser.parse(args.file)
# logging.debug('students: %s',repr(students))

# course info
logging.debug('course: %s',repr(course))
(term,session,org,level) = course['description'].split(' | ')
logging.debug('term: %s',term)
logging.debug('session: %s',session)
logging.debug('org: %s',org)
logging.debug('level: %s',level)


str=""
for key in students:
	student = students[key]
	    # first and last names
	(family_name,given_names) = student['name'].split(',')
	(username,domain) = student['email'].split('@')
	str+="[(%s)(%s %s)]" % (username, given_names, family_name)

print str
