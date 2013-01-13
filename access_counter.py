# -*- coding: utf-8 -*-
"""
Simple access counter service.

@copyright: 2012 by Tatsuya Koyama
            (www.tatsuya-koyama.com)
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from myhandler.count import CountHandler
from myhandler.view_stat import ViewStatHandler


def main():
    application = webapp.WSGIApplication(
        [
            ('/'    , CountHandler),
            ('/stat', ViewStatHandler)
        ],
        debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
