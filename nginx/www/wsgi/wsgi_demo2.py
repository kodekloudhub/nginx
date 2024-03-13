#! /usr/bin/env python3
#
#
from wsgiref.simple_server import make_server
PORT = 8023


# application is called by the WSGI middleware
def application(environ, start_response):
    headers = [('Content-type', 'text/html; charset=utf-8')]
    if "GET" == environ['REQUEST_METHOD']:
        html = """
        <html>
        <head>
            <title>Addition Form</title>
        </head>
        <body>
            <h1>Addition Form</h1>
            <form action="" method="POST">
                <label for="num1">Enter the first number:</label><br>
                <input type="text" id="num1" name="num1"><br>
                <label for="num2">Enter the second number:</label><br>
                <input type="text" id="num2" name="num2"><br><br>
                <input type="submit" value="Calculate Sum">
            </form>
        <p>Thank you</p>
        </body>
        </html>
        """
        status = "200 OK"
    elif "POST" == environ['REQUEST_METHOD']:
        query_string = environ['QUERY_STRING']
        num1 = num2 = None
        try:
            num1 = int(query_string.split('&')[0].split('=')[1])
            num2 = int(query_string.split('&')[1].split('=')[1])
            sum_result = num1 + num2
            html = "<html><head><title>Addition results</title></head>" \
                   f"<body><p>Sum of {num1} and {num2} is {sum_result}</p></body></html>"
            status = '200 OK'

        except ValueError:
            status = "400 Bad Request"
            html = "<html><head><title>Addition results</title></head>" \
                   f"<p>Error: Please enter valid integer values for both numbers {num1} {num2}.</p></body></html>"
    else:
        status = "405 Method not allowed"
        html = "<html><head><title>Addition results</title></head>" \
               f"<p>Error: The only methods allowed are GET and POST.  You entered {environ['REQUEST_METHOD']}</p>" \
               "</body> </html>"
        print(html, "\n\n")
# calling start_response should be done only when the response is complete.  Otherwise, one runs the risk of calling
# start_response twice, and that raises an exception within wsgiref.  Also, calling it is DRY.
    start_response(status, headers)
    return [html.encode()]


if __name__ == '__main__':
    with make_server('', PORT, application) as httpd:
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()
