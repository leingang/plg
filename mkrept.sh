#!/bin/bash

files=$@
progname=`basename $0`
tempheaderfile=`mktemp /tmp/${progname}.XXXXXX` || exit 1
temprecfile=`mktemp /tmp/${progname}.XXXXXX` || exit 1
pdftk=/opt/local/bin/pdftk
# assume the first file has the right fields
firstfile=$1

# make the header file
echo filename,`$pdftk $firstfile dump_data_fields \
	| grep FieldName: \
	| cut -d ' ' -f 2- \
	| tr '\n' , \
	| sed -e 's/,$//'` >> $tempheaderfile
# make the records 
for file in $files
do
	values=`$pdftk $file dump_data_fields \
		| grep FieldValue: \
		| cut -d ' ' -f 2 \
		| tr '\n' , \
		| sed -e 's/,$//'`
	echo $file,$values
done >> $temprecfile
cat $tempheaderfile $temprecfile


# cleanup
rm $tempheaderfile $temprecfile
	
