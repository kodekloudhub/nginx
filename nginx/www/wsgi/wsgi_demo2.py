#! /usr/bin/env python3
#
#
from wsgiref.simple_server import make_server

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, headers)

    html = """
    <html>
    <head>
        <title>Addition Form</title>
    </head>
    <body>
        <h1>Addition Form</h1>
        <form action="" method="get">
            <label for="num1">Enter the first number:</label><br>
            <input type="text" id="num1" name="num1"><br>
            <label for="num2">Enter the second number:</label><br>
            <input type="text" id="num2" name="num2"><br><br>
            <input type="submit" value="Calculate Sum">
        </form>
        {}
    </body>
    </html>
    """

    if environ['QUERY_STRING']:
        query_string = environ['QUERY_STRING']
        try:
            num1 = int(query_string.split('&')[0].split('=')[1])
            num2 = int(query_string.split('&')[1].split('=')[1])
            sum_result = num1 + num2
            result_html = "<p>Sum of {} and {} is {}</p>".format(num1, num2, sum_result)
            return [html.format(result_html).encode()]
        except ValueError:
            error_html = "<p>Error: Please enter valid integer values for both numbers.</p>"
            return [html.format(error_html).encode()]
    else:
        return [html.format("").encode()]

if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()


