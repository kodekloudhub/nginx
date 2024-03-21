#! /bin/bash
#
#
TEMP="/tmp/REST_TEST"
rm $TEMP

function my_test {
  # First arg is the httpx command, second arg is a string to search for (or search for absense)
  # third arg either -v or nothing fourth arg is a unique string to mark which test is being run
  echo "Testing the command $1 step $4"
  if $1; then echo "$1 worked"; else echo "FAILED FAILED FAILED"; cat $TEMP; exit $?; fi
  httpx -m GET http://e7240/api/items| tee $TEMP
  # If you add any options to the fgrep command, then make sure $3 is the last option but before $2 
  fgrep $3 $2 $TEMP
  STATUS=$?
  echo -n "Test : $4 : "		# -n suppresses the line feed at the end 
  if [ $STATUS -eq 0 ]; then
    echo "The command $1 succeeded"
  else
    echo "The command $1 FAILED - output is"
    cat $TEMP
  fi
  return $STATUS
} 
my_test "httpx -m POST -d key key_7007 -d value value_7007 http://e7240/api/items" "key_7007" "--" "Posting 7006"
my_test "httpx -m GET http://e7240/api/items" "key_7007" "--" "Is 7007 present?"
my_test "httpx -m GET http://e7240/api/items" "value_7007" "--" "Is 7007's value value_7007?"   # Automated testing found this bug!
my_test "httpx -m DELETE -p key key_7007 http://e7240/api/items/" "value_7006" "-v" "Deleting 7006"
my_test "httpx -m GET http://e7240/api/items" "key_7007" "--" "Is 7006 gone?"
my_test "httpx -m POST -d key key_7008 -d value value_7008 http://e7240/api/items" "value_7008" "--" "Posting 7008"
my_test "httpx -m POST -d key key_7009 -d value value_7009 http://e7240/api/items" "key_7009" "--" "Posting 7009"
my_test "httpx -m PUT -d key key_7009 -d value value_7009_U_01 http://e7240/api/items/" "value_7009_U_01" "--" "Updating 7009"
my_test "httpx -m DELETE -p key key_7008 http://e7240/api/items/" "value_7008" "-v" "Deleting 7008"
my_test "httpx -m GET http://e7240/api/items" "key_7009" "--" "Is key 7009 present?"
exit 0

