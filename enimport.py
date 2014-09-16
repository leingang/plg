#!/opt/local/bin/python
#
# script to take a CSV list of filenames/NetID/name pairs and import to Evernote
#
# Usage: if mfst.csv is of the form
#
# filename,NetID,LastName__FirstNames
#
# then 
#
# $ ./enimport.py [options] < mfst.csv 
#
# will import into Evernote all the specified files

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import argparse
import ConfigParser
import logging
import csv
import sys
import mimetypes

parser = argparse.ArgumentParser()
# config file:
# FIXME: this method clobbers all the help in the later options.
# see http://stackoverflow.com/a/5826167/297797 for a fix
# TODO: multiple config files (e.g., ./.enimportrc, ~/enimport.rc, explicit files)
parser.add_argument("-c", "--config",
                    help="Specify config file", metavar="FILE")
args, remaining_argv = parser.parse_known_args()
defaults={}
if args.config:
    config = ConfigParser.SafeConfigParser()
    config.read([args.config])
    # TODO: jury-rig config.parser so it doesn't need a dummy section
    # http://stackoverflow.com/a/8657601/297797
    defaults = dict(config.items("defaults"))
parser.set_defaults(**defaults)
    
parser.add_argument('-d','--debug',
    help='Print lots of debugging statements',
    action="store_const",dest="loglevel",const=logging.DEBUG,
    default=logging.WARNING
)
parser.add_argument('-v','--verbose',
    help='Be verbose',
    action="store_const",dest="loglevel",const=logging.INFO
)
parser.add_argument('--dry-run',
	help='do not save any notes',
	action='store_true',dest='dry_run')
parser.add_argument('--auth-token',
	help='authentication token (visit https://sandbox.evernote.com/api/DeveloperToken.action)',
	action='store',dest='auth_token')
parser.add_argument('--sandbox',
	help='use the sandbox server',
	action='store_true',dest='sandbox',
	default=False)
parser.add_argument('-nb','--notebook',
	help="Store note in this notebook",
	action="store",dest="notebook",
	)
parser.add_argument('--docname',
	help="Name of the document",
	default="Untitled document",
	action="store", dest="doc_name")
parser.add_argument('--course',
	help="Name of the course",
	action="store", dest="course")
parser.add_argument('--term',
	help='term name',
	action='store',dest='term',
	default="Fall 2014")
# TODO: tag names (multiple optional argument)
parser.add_argument('--tag',metavar='TAG',
	help='Add tag to note (as many as you like)',
	action='append',dest='tags')
parser.add_argument('csvfile', nargs='?', 
	help="CSV file from which to read (default: standard input)",
	type=argparse.FileType('r'),default=sys.stdin)	
	
args = parser.parse_args(remaining_argv)    
logging.basicConfig(level=args.loglevel)

if not(args.auth_token):
    logging.error("Please fill in your developer token. To get a developer token, visit https://sandbox.evernote.com/api/DeveloperToken.action")
    exit(1)
client = EvernoteClient(token=args.auth_token, sandbox=args.sandbox)
user_store = client.get_user_store()
version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)
if (version_ok):
	logging.debug("Evernote API version up to date: %d",version_ok)
else:
	logging.error("Evernote API version NOT up to date")
	exit(1)

note_store = client.get_note_store()

## get the right notebook
if (args.notebook):
	logging.debug("Searching for notebook named '%s'",args.notebook)
	notebooks = note_store.listNotebooks()
	found=False
	for notebook in notebooks:
		logging.debug("Notebook: name='%s' guid=%s", notebook.name, notebook.guid)
		if (notebook.name == args.notebook):
			logging.debug("match")
			found=True
			break
	if (not(found)):
		logging.error("Notebook named '%s' not found", args.notebook)
else:
	logging.debug("Using default notebook")
	notebook = note_store.getDefaultNotebook()
logging.info("Using Notebook '%s' with guid %s", notebook.name, notebook.guid)

for rec in csv.reader(args.csvfile):
	logging.debug("rec: %s", repr(rec))
	filename,student_netid,student_fname_rev = rec
	# check if the first field is a valid file (it might be a header)
	try:
		file = open(filename, 'rb').read()
	except IOError:
		logging.info("Skipping %s as it does not seem to be a file",filename)
		continue

	student_lname,student_gnames=student_fname_rev.split('__')
	student_gnames = student_gnames.replace('_',' ')
	student_fname = "%s %s" % (student_gnames,student_lname)
	logging.debug("student_fname: '%s'",student_fname)
	student_tagname="student: %s; %s <%s@nyu.edu>" % (student_lname, student_gnames, student_netid)
	logging.debug("student_tagname: '%s'",student_tagname)

	# To create a new note, simply create a new Note object and fill in
	# attributes such as the note's title.
	note = Types.Note()
	note.notebookGuid=notebook.guid
	note.title = "%s for %s from %s" % (args.doc_name,student_fname,args.course)
	note.tagNames=list(args.tags)
	note.tagNames.append('student work')
	note.tagNames.append(student_tagname)
	if (args.term):
		note.title += ", " + args.term
		note.tagNames.append('term: ' + args.term)
	note.tagNames.append('course: ' + args.course)
	logging.info("note.title: '%s'", note.title)
	logging.info("note.tags: %s",repr(note.tagNames))
	## TODO: add some more note attributes
	# created - exam date/time (Timestamp) # parse ISO 8601!
	# updated - now, obvs (Timestamp)
	## TODO: add some more attributes with the NoteAttributes type
	# https://dev.evernote.com/doc/reference/Types.html#Struct_NoteAttributes
	# latitude
	# longitude
	# altitude
	# author - student <email>
	# source - progname
	# placeName - "CIMS"? "Work"?


	# To include an attachment such as an image in a note, first create a Resource
	# for the attachment. At a minimum, the Resource contains the binary attachment
	# data, an MD5 hash of the binary data, and the attachment MIME type.
	# It can also include attributes such as filename and location.
	md5 = hashlib.md5()
	md5.update(file)
	hash = md5.digest()
	logging.debug("hash: %s", hash)

	data = Types.Data()
	data.size = len(file)
	data.bodyHash = hash
	data.body = file

	resource = Types.Resource()
	(resource.mime,encoding) = mimetypes.guess_type(filename)
	logging.debug("resource.mime: %s",resource.mime)
	resource.data = data
	
	# adding a file name to the resource with a ResourceAttributes type.
	resource_attributes=Types.ResourceAttributes()
	resource_attributes.fileName=note.title + mimetypes.guess_extension(resource.mime)
	resource.attributes=resource_attributes
	
	# Now, add the new Resource to the note's list of resources
	note.resources = [resource]
	
	# To display the Resource as part of the note's content, include an <en-media>
	# tag in the note's ENML content. The en-media tag identifies the corresponding
	# Resource using the MD5 hash.
	hash_hex = binascii.hexlify(hash)

	# The content of an Evernote note is represented using Evernote Markup Language
	# (ENML). The full ENML specification can be found in the Evernote API Overview
	# at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
	note.content = '<?xml version="1.0" encoding="UTF-8"?>'
	note.content += '<!DOCTYPE en-note SYSTEM ' \
		'"http://xml.evernote.com/pub/enml2.dtd">'
	note.content += '<en-note>'
	note.content += '<en-media type="' + resource.mime + '" hash="' + hash_hex + '"/>'
	note.content += '</en-note>'

	# Finally, send the new note to Evernote using the createNote method
	# The new Note object that is returned will contain server-generated
	# attributes such as the new note's unique GUID.
	if (args.dry_run):
		logging.info("If this were not a dry run, would save a note here")
	else:
		logging.info("Adding note to note_store")
		created_note = note_store.createNote(note)
		logging.info("Successfully created a new note with GUID: %s", created_note.guid)




