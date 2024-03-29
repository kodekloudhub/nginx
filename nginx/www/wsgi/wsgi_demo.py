#! /usr/bin/env python3
#
# Last modified 2024-03-07 4:13
# This is a simple WSGI application.  It should be started under a web server such as gunicorn, preferably before nginx starts.
#
import sys
from wsgiref.simple_server import make_server
import time
import os       # for the call to os.getpid()

# For reasons I do not understand, output to stderr does not appear.  If I figure out the reason and can fix it, then
# change ERROR_OUT to sys.stderr
ERROR_OUT = sys.stdout
PORT = 8000  # Listen on this port.  Traditionally, somewhere between 8000 and 8999.
# It is a bad idea to use a port number less than 1024, because that requires root privileges
# and if you need root, then you are doing something wrong.

MAX_START_FAILS = 5     # If the server fails to start, then try again, up to MAX_START_FAILS times.
# The hypothesis is that a previous run has left the TCP in a finalizing state.
# ( FIN-WAIT-1, FIN-WAIT-2, CLOSE-WAIT, CLOSING, LAST-ACK, or TIME-WAIT ).  Since the socket isn't closed
# yet, wait until it will be.


def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)

    html = """
    <html>
    <head><title>Addition</title></head>
    <body>
        <h1>Addition</h1>
        <form method="post">
            <label for="num1">Enter first number:</label>
            <input type="number" id="num1" name="num1"><br><br>
            <label for="num2">Enter second number:</label>
            <input type="number" id="num2" name="num2"><br><br>
            <input type="submit" value="Add">
        </form>
        <br>
        <h2>Result: {result}</h2>
    </body>
    </html>
    """

    if environ['REQUEST_METHOD'] == 'POST':
        print(f"The user agent is {environ['HTTP_USER_AGENT']}", file=ERROR_OUT)
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            print(f"environ['CONTENT_LENGTH'] exists but is not a valid integer {environ['CONTENT_LENGTH']}.  Using 0",
                  file=ERROR_OUT )
            content_length = 0
        # I am having problems with httpx and curl, which I think is passing ill-formed queries, specifically
        # explicitly setting the content length to 0.  This happens when I invoke httpx from the command line.
        # I have not tested httpx when called programmatically. (as of 2024-02-28).  This is not an issue with
        # Google Chrome or chromium.
        if content_length > 0:
            print(f"Content length is {content_length}")
            post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
        else:
            post_data = environ["QUERY_STRING"]
            content_length = len(post_data)
            print(f"Replacing CONTENT-LENGTH, which is 0, with the length of QUERY_STRING, which is {content_length}")
        if len(post_data) == 0:
            print(f"The length of post_data is 0, should be longer.  Query_str is {post_data}"
                  f"content_length is {content_length}, environ is: ", file=ERROR_OUT)
            for key in environ:
                print(f"{key}: {environ[key]}", file=ERROR_OUT)
            raise AssertionError  # This seems overly draconian
        print(f"post_data is {post_data}\n", file=ERROR_OUT)
        data = parse_post_data(post_data)
        try:
            num1 = int(data['num1'])
            num2 = int(data['num2'])
        except (KeyError, ValueError):
            result = f'Error: Please enter valid numbers. <b>post_data</b> is {post_data} '
        else:
            result = num1 + num2
    # This is really a shortcut.  Should be if environ['REQUEST_METHOD'] != 'GET'` then return 405,  Method Not Allowed
    else:
        result = html

    return [html.format(result=result).encode('utf-8')]


def parse_post_data(post_data):
    pairs = post_data.split('&')
    data = {}
    for pair in pairs:
        key, value = pair.split('=')
        data[key] = value
    return data


# Creating a server that listens on TCP port.
# When a web client makes a query, the server will call
# application which then does whatever is needed.
fail_ctr = 0
while fail_ctr < MAX_START_FAILS:
    try:
        with make_server('', PORT, application) as httpd:
            print(f"Serving on port {PORT}...")
            # Serve until process is killed
            httpd.serve_forever()
            # If the process is killed, then why are you here?
        print("IF YOU GET HERE, THEN SOMETHING IS VERY, VERY, WRONG", file=ERROR_OUT)
        exit(2)
    except OSError as ox:
        fail_ctr += 1
        print(f"Tried to the start server on port {PORT} and that failed {fail_ctr} times. {MAX_START_FAILS -fail_ctr} attempts left.  PID={os.getpid()}  Probably waiting for TCP socket to close Waiting 30 seconds.", file=ERROR_OUT)
        time.sleep(30)
print("Too many failures.  Exiting abnormally", file=ERROR_OUT)
exit(1)
