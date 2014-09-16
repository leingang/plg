#!/bin/bash
# Stamp a "grade form" on top of a set of scanned quizzes or exams.
USAGE="Usage: $0 FORM (FILE)+"

# TODO
# [ ] Configurable destination directory
# [ ] Configurable output file name template
# [ ] dry run option?

if [ "$#" == "0" ]
then
	echo $USAGE
	exit 1
fi

form=$1
shift
for file in "$@"
do
	pdftk $form multibackground $file output `basename $file .pdf`_form.pdf
done