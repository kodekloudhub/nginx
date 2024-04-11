#! /bin/bash
#
#
TEMP="/tmp/REST_TEST"
TEMP_1="/tmp/REST_TEST__1"
VERBOSE=0

trap "sleep 60" 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15


function my_test {
  # First arg is the httpx command, second arg is a string to search for (or search for absense)
  # third arg either -v or nothing fourth arg is a unique string to mark which test is being run
  echo "Testing the command $1 step $4"
  if [ $VERBOSE -eq 1 ] ; then
    $1 | tee $TEMP
  else
    $1 > $TEMP
  fi
  STATUS=$?
  # This checks for some gross failure in the httpx command, which is unlikely but not impossible
  if [ $STATUS -eq 0 ]; then echo "Step $4 worked"; else echo "Step $4 : $1 FAILED FAILED FAILED"; cat $TEMP; return $STATUS; fi
  # This checks that the desired change in state occurred or that an undesired change of state did not occur
  httpx -m GET http://e7240/api/wsgi/items| tee $TEMP_1
  # If you add any options to the fgrep command, then make sure $3 is the last option but before $2 
  fgrep $3 $2 $TEMP_1
  STATUS=$?
  echo -n "Test : $4 : "		# -n suppresses the line feed at the end 
  if [ $STATUS -eq 0 ]; then
    echo "The command $1 succeeded"
  else
    echo "The command $1 FAILED - output is"
    cat $TEMP_1
    echo "Sleeping 60 seconds - press control-S to pause, control-C to stop, do nothing to continue after 60 seconds"
    sleep 60
    return 1			# This seems draconian.  It gives you a change to stop and think about why this failed.
  fi
  return $STATUS
}
# The big difference between this version and the version in test_REST.sh is that this version uses the WSGI API
# It occurs to me that I could have modified test_REST.sh to handle either proxy or wsgi variants in the URL
my_test "httpx -m POST -d key key_7006 -d value value_7006 http://e7240/api/wsgi/items" "key_7006" "--" "Posting 7006"
my_test "httpx -m POST -d key key_7007 -d value value_7007 http://e7240/api/wsgi/items" "key_7007" "--" "Posting 7007"
my_test "httpx -m GET http://e7240/api/wsgi/items" "key_7007" "--" "Is key 7007 present?"
my_test "httpx -m GET http://e7240/api/wsgi/items" "value_7007" "--" "Is 7007's value value_7007?"   # Automated testing found this bug!

my_test "httpx -m GET http://e7240/api/wsgi/items" "key_7006" "--" "Is key 7006 present before deleting it?"
my_test "httpx -m DELETE -p key key_7006 http://e7240/api/wsgi/items/" "value_7006" "-v" "Deleting 7006"
my_test "httpx -m GET http://e7240/api/wsgi/items" "key_7006" "-v" "Is 7006 gone now that it was deleted?"

# I decided to take out the next two steps because I don't know how to handle something that returns an error
# in a specific case without complicating things in the general cases.
# my_test "httpx -m DELETE -p key key_7006 http://e7240/api/wsgi/items/" "value_7006" "-v" "Deleting 7006 again.  Testing idempotence"
# my_test "httpx -m GET http://e7240/api/wsgi/items" "key_7006" "-v" "Is 7006 still gone?"

my_test "httpx -m POST -d key key_7008 -d value value_7008 http://e7240/api/wsgi/items" "value_7008" "--" "Posting 7008"
my_test "httpx -m POST -d key key_7009 -d value value_7009 http://e7240/api/wsgi/items" "key_7009" "--" "Posting 7009"

my_test "httpx -m PUT -d key key_7009 -d value value_7009_U_01 http://e7240/api/wsgi/items/" "value_7009_U_01" "--" "Updating 7009"

my_test "httpx -m DELETE -p key key_7008 http://e7240/api/wsgi/items/" "value_7008" "-v" "Deleting 7008"
my_test "httpx -m GET http://e7240/api/wsgi/items" "key_7009" "--" "Is key 7009 present after deleting 7008?"

my_test "httpx -m GET http://e7240/api/wsgi/items" "key_7010" "-v" "Is key 7010 present BEFORE it was updated?"
my_test "httpx -m PUT -d key key_7010 -d value value_7010 http://e7240/api/wsgi/items/" "value_7010" "--" "Updating 7010, which did not exist"
my_test "httpx -m GET http://e7240/api/wsgi/items" "key_7010" "--" "Is key 7010 present after it was updated?"

# The tests for static content just do not work here.
# my_test "httpx -m GET http://e7240/welcome.html" "Evilcorp" "--" "testing static content (welcome.html)"
# my_test "httpx -m GET http://e7240/page_header.js" "pathname" "--" "testing static content (page_header.js)"
# my_test "httpx -m GET http://e7240/README.txt" "Contains" "--" "testing static content (README.txt)"


