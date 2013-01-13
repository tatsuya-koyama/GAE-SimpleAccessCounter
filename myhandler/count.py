# -*- coding: utf-8 -*-
"""
Handler class of simple access counter service.

@copyright: 2012 by Tatsuya Koyama
            (www.tatsuya-koyama.com)
"""

import re
from google.appengine.ext import webapp
from config.config import Config
from myshard import counter_shard
from mylib.myhandler import MyHandler


class CountHandler(MyHandler):
    def get(self):
        referer  = self.request.headers.get('Referer')
        callback = self.request.get('callback')
        type     = self.request.get('type')
        id       = self.request.get('id')
        url = type + '::' + id

        #----- guard
        success = True if not url == '::' else False
        config  = Config
        if not config.debug_mode:
            is_allowed = self.is_allowed_referer(referer, config.allowed_domains)
            if not is_allowed:
                success = False

        obj = {'success': success}
        if not success:
            self.respondJSONP(obj, callback)
            return

        #----- counting
        count = counter_shard.get_count(url)
        obj['count'] = int(count) + 1
        counter_shard.increment(url)

        self.respondJSONP(obj, callback)

    def is_allowed_referer(self, referer, allowed_domains):
        if not isinstance(referer, str):
            return False

        pattern = 'http://www\.(.*?)/'
        if re.search(pattern, referer):
            domain = re.search(pattern, referer).groups()[0]
            if domain in allowed_domains:
                return True
        return False
