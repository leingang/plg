#!/usr/bin/awk -f 

# script to take a CSV list of filenames/NetID pairs and move them into an NYU Classes drop box.
#
# Usage: if mfst.csv is of the form
#
# filename,Student ID,Student_Name
# quiz_030_form.pdf,maa699,Amoa-Asare__Maame_F
# quiz_031_form.pdf,mb5039,Basith__Masrour
# quiz_009_form.pdf,jb3129,Berenzon__Julius_S
# quiz_006_form.pdf,hc1324,Cao__Haoyun
# ,aac465,Chen__Alana_A
# quiz_021_form.pdf,mbd315,Davish__Maxwell_B
# quiz_013_form.pdf,wd481,Deng__Wenyu
# quiz_025_form.pdf,cf1201,Flynn__Courtney
# quiz_001_form.pdf,mg3602,Golyan__Matthew
#
# then 
#
# $ ./mv.awk < mfst.csv | bash -v
#  
# TODO: 
# [X] skip blank records 
# [X] skip first line (we just look for ".pdf" in the first field)
# [X] configure destination directory
#     use -v destdir=DIR on the awk command line.
# * write in python. :-D

BEGIN {
	FS=","
	# siteid="255b3c0d-8ff3-4e46-acc5-b9225d7e47a0"
	# docstem="quiz2"
	if (destdir=="")
		destdir="../returned"
	print "if [ ! -d \"" destdir "\" ]; then mkdir \"" destdir "\"; fi || exit 1"
} 
{
	oldfile=$1
	username=$2
	fn=$3
	if (index($1,".pdf") == 0) 
		next
	else
		newfile = fn "_" docstem ".pdf"
		newurl = "https://newclasses.nyu.edu/dav/group-user/" siteid "/" username "/" newfile
		print "gs -sDEVICE=pdfwrite -dPDFSETTINGS=/default -dNOPAUSE -dQUIET -dBATCH -sOutputFile=" newfile , oldfile
		# print "curl --netrc -T", newfile, newurl, "&& mv", newfile, destdir
		# curl was not working so I did it the old way
		print "cp", newfile, "/Volumes/" siteid "/" username "/", "&& mv", newfile, destdir
}
