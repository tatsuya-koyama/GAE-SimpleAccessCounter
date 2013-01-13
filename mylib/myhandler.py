# -*- coding: utf-8 -*-
"""
Base handler class.

@copyright: 2012 by Tatsuya Koyama
            (www.tatsuya-koyama.com)
"""

from django.utils import simplejson
from google.appengine.ext import webapp


class MyHandler(webapp.RequestHandler):
    def write(self, str):
        self.response.out.write(str)

    def respondJSON(self, obj):
        json = simplejson.dumps(obj, ensure_ascii=False)
        self.response.content_type = 'application/json'
        self.response.out.write(json)

    def respondJSONP(self, obj, callback):
        json = simplejson.dumps(obj, ensure_ascii=False)
        self.response.content_type = 'application/json'
        self.response.out.write('%s(%s)' % (callback, json))
