#! /usr/bin/env python3

import os
from http.server import HTTPServer, SimpleHTTPRequestHandler


class SimpleHTTP404RequestHandler(SimpleHTTPRequestHandler):
    """
    Overrides the default request handler to handle custom 404 pages as 404.html
    (i.e. a 404.html page located in the root). Good for:
        GitHub:     https://help.github.com/articles/custom-404-pages/
    """

    def do_GET(self):
        self.directory = "docs"
        if "CSCA20F19/" == self.path[:10]:
            self.path = self.path[10:]
        path = self.translate_path(self.path)

        # If the path doesn't exist, fake it to be the 404 page.
        if not os.path.exists(path):
            self.path = '404.html'

        # Call the superclass methods to actually serve the page.
        SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
    with HTTPServer(('', 8000), SimpleHTTP404RequestHandler) as server:
        server.serve_forever()
