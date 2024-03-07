#! /usr/bin/env python3

PORT = 8000
def application(environ, start_response):
    # Set content type to HTML
    headers = [('Content-type', 'text/html')]
    # Get query parameters from the URL
    query_string = environ.get('QUERY_STRING', '')
    # Parse query parameters
    params = parse_query_string(query_string)

    # Extract integers from query parameters
    num1 = int(params.get('num1', 0))
    num2 = int(params.get('num2', 0))

    # Calculate sum
    total = num1 + num2

    # HTML response body
    response_body = f"""
    <html>
    <head>
        <title>Sum of Two Integers</title>
    </head>
    <body>
        <h1>Sum of {num1} and {num2} is {total}</h1>
    </body>
    </html>
    """

    # Convert response body to bytes
    response_body = response_body.encode('utf-8')

    # Send response with HTTP status code 200 OK
    start_response('200 OK', headers)

    return [response_body]


def parse_query_string(query_string):


# Parse query string and return dictionary of key - value pairs
    params = {}
    if query_string:
        pairs = query_string.split('&')
    for pair in pairs:
        key, value = pair.split('=')

    params[key] = value
    return params

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    # Create a WSGI server
    with make_server('', PORT, application) as httpd:
        print(f"Serving on port {PORT}...")

        # Serve requests indefinitely
        httpd.serve_forever()
