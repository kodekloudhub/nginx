#! /usr/bin/env python3

import sys
import requests  # From https://pypi.org/project/requests/


def help():
    print(sys.argv[0] + f"[hostname [coef of expansion]]")
    return None


def long_url(host_url: str, expand_coef: float) -> None:
    len_url = 10
    iter_ctr = 0
    while True:
        iter_ctr += 1
        print(f"Iteration {iter_ctr} Working on  length {len_url}")
        uri = "x" * len_url
        url = host_url + "/" + uri
        r = requests.get(url)

        if r.status_code == 414:
            print(f"Your server can't handle URLs longer than {len_url}")
            break
        if r.status_code != 404:
            print(f"Strange.  I was expecting a status of 404, but got {r.status_code} instead.\n" +
                  r.reason, file=sys.stderr )
        len_url = int(len_url * expand_coef)

if "__main__" == __name__:
    if len(sys.argv) > 1:
        host_url = sys.argv[1]
        if host_url == "-h" or host_url == "--help":
            help()
            sys.exit(1)
        if len(sys.argv) > 2:
            expand_coef = sys.argv[2]
        else:
            expand_coef = input("How fast do you want the length of the URL to increase? (Enter a floating point "
                                "number > 1.0  ")
        expand_coef = float(expand_coef)
    else:
        host_url = input("Enter the host URL, including HTTP or HTTPS  ")
        expand_coef = float(input("How fast do you want the length of the URL to increase? (Enter a floating point "
                                  "number > 1.0  "))
    long_url(host_url, expand_coef)
