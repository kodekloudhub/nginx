#! /bin/bash
#
#
# Test the nginx web server on jeffs-latitudee7240
PREFIX="jeffs-e7240-"

for P in "4" "6"; do		# protocol: IPv4 and IPv6
	echo "Working on protocol IPv${P}"
        for I in 170 171 172; do
	        IPADDR=${PREFIX}${I}
	        echo $IPADDR
	        if ! curl -${P} --silent http://$IPADDR > temp.txt; then
		        echo "curl failed at url $IPADDR exit status is $?"
		        exit 1
	        fi
	        if ! fgrep --color "subdirectory $I" temp.txt; then
		        echo "Test string 'subdirectory $I' not found in temp.txt"
		        cat temp.txt
		        exit 1
	        fi
	        URL=$IPADDR/page_header.js
		if ! curl -${P} --silent http://$URL > temp.txt; then
			echo "curl failed at url $URL exit status is $?"
		exit 1
		fi
		if ! fgrep --color "last modified" temp.txt; then
			echo "In $URL, test string 'last modified' not found in temp.txt"
			cat temp.txt
                exit 1
		fi
		echo "$IPADDR passed all tests: IPv${P}"
	done
	echo "Completed IPv${P}"
done
echo "All addresses all protocols passed all tests"
rm temp.txt

  


