#! /usr/bin/env python3
import sys
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

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
        try:
            print(f"The user agent is {environ['HTTP_USER_AGENT']}")
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            # I am having problems with httpx, which I think is passing ill-formed queries, specifically
            # explicitly setting the content length to 0.  This happens when I invoke httpx from the command line.
            # I have not tested httpx when called programmatically. (as of 2024-02-28)
            if content_length > 0:
                print(f"Content length is {content_length}")
            else:
                query_str = environ.get("QUERY_STRING")
                query_string_len = len(query_str)
                print (f"Replacing CONTENT-LENGTH, which is 0, with the length of the query string, which is {query_string_len}")
            post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
            if len(post_data) == 0:
                post_data = query_str
            print(f"post_data is {post_data}\n", file=sys.stdout)
            data = parse_post_data(post_data)
            num1 = int(data['num1'])
            num2 = int(data['num2'])
            result = num1 + num2
        except (KeyError, ValueError):
            result = f'Error: Please enter valid numbers. <b>post_data</b> is {post_data} '
            # <b>environ</b> is "' \
            #         f'{environ}'
    else:
        result = ''

    return [html.format(result=result).encode('utf-8')]


def parse_post_data(post_data):
    pairs = post_data.split('&')
    data = {}
    for pair in pairs:
        key, value = pair.split('=')
        data[key] = value
    return data


# Creating a server
with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    # Serve until process is killed
    httpd.serve_forever()