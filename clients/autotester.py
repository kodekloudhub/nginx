#! /usr/bin/env python3
#
# autotester.py
# A very crude but still very effective testing program for websites
# This program uses an external tab separated variable (TSV) file to read the tests.  Each line has several fields,
# separated by tabs.
# Field values      meaning
# 1     4,6, or b   IP version number.  4=> IPv4 only, 6=> IPv6 only, b=>both (stretch goal: u for unix)
# 2     URL         Fully qualified URL, either HTTP or HTTPS, hostname, port number (if needed) and the rest of the URI
# 3     request     the method, usually GET (the current default)
# 4     headers     Any additional headers in the form of key:value[,key:value...]
# 5-n   string(s)   All the strings that must be in the output.  If any string is missing, then that is a FAIL.

# This is getting complicated enough to where I am thinking about changing from TSV to JSON

import csv  # https://www.tutorialstonight.com/read-tsv-file-python says that this is fastest.  It is the easiest
import sys
from typing import List

import colorama
import httpx

YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
BLUE = colorama.Fore.BLUE
GRAY = colorama.Fore.LIGHTWHITE_EX
MAGENTA = colorama.Fore.MAGENTA
GREEN = colorama.Fore.GREEN
RESET = colorama.Fore.RESET
all_pass: bool = True


def run_test(protocol: str, url: str, request: str, headers: dict, strings: List[str]) -> None:
    """
    Run the test on URL using the protocol.  Expect ALL strings in the result.
    :param protocol: str values are "4","6", or "b" for IPv4, IPv6, or both
    :param url: str The URL to test
    :param request: GET, POST, PUT, HEAD or similar
    :param strings: A list of strings that the website should return
    :param headers: a (possibly empty) dictionary with additional headers
    :return: a string, suitable for logging
    """
    global all_pass

    if len(headers) > 0:
        report_error(f"{MAGENTA} headers are not supported in this version of the autotester{RESET}")
    # For now, to force the use IPv4, bind the local address to an IPv4 address, like so:
    # httpx.Client(transport=httpx.HTTPTransport(local_address="0.0.0.0"))
    # This is from https://www.python-httpx.org/advanced/#usage_1
    protocol = "6"

    try:
        r: httpx.Response = httpx.get(url)
    except httpx.ConnectError:
        report_error(f"{RED}httpx raised an httpxConnectError on URL {url}.")
    except Exception as e:
        report_error(f"{RED}httpx raised an {e.__class__.__name__} on URL {url}.")
    else:
        print(f"{MAGENTA}The type of r is {type(r)}. {RESET}")
        for s in strings:
            if s not in r.text:
                report_error(f"{YELLOW} the string '{s}' does not appear in the output of {url}{RESET}\n" +
                             GRAY + r.text + RESET)
                all_pass = False


def report_error(message: str) -> str:
    """

    :type message: object
    :param message: str A string with a message.  If the string contains RED, YELLOW, GREEN, or BLUE that indicates
                    that the message is warning, an error, a success, or informational
    :return: str    So that in the future, if this method wants to modify the message, it can
    """
    print(message)
    return message


if "__main__" == __name__:
    if len(sys.argv) > 1:
        tsv_filename = sys.argv[1]
    else:
        tsv_filename = input("Enter the name of the TSV file: ")
    with open(file=tsv_filename, mode="r") as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')
        for row in tsv_reader:
            print(f"{MAGENTA}The type of row is {type(row)}, its {len(row)} and is {row}.{RESET}")
            # run_test might clear all_pass
            run_test(protocol=row[0], url=row[1], request="GET", headers={}, strings=row[2:])
    print(f"{GREEN} all tests PASS {RESET}" if all_pass else f"{RED} at least one test FAILED{RESET}")
