# -*- coding: utf-8 -*-
"""
Handler class of simple access counter service.

@copyright: 2012 by Tatsuya Koyama
            (www.tatsuya-koyama.com)
"""

from google.appengine.ext import webapp
from myshard import counter_shard
from mylib.myhandler import MyHandler

import os
import re
from google.appengine.ext.webapp import template


class ViewStatHandler(MyHandler):
    def get(self):
        count_list = counter_shard.get_all_count()
        count_list = sorted(
            count_list,
            key=lambda a:int(a.get('count')),
            reverse=True)

        type_count_list = self.get_counts_separated_by_type(count_list)
        template_values = {
            'count_list': count_list,
            'type_count_list': type_count_list
        }
        path = os.path.join(os.path.dirname(__file__), '../page/view_stat.html')
        self.write(template.render(path, template_values))

    def get_counts_separated_by_type(self, count_list):
        """
        INPUT:
          [
            {name: "pv::hoge", count: 2},
            {name: "pv::fuga", count: 3},
            {name: "dl::piyo", count: 5}
          ]

        OUTPUT:
          [
            pv: {
              {name: "hoge", count: 2},
              {name: "fuga", count: 3}
            },
            dl: {
              {name: "piyo", count: 5}
            }
          ]
        """
        result = {}
        for count in count_list:
            pattern = '(.*?)::(.*)'
            if re.search(pattern, count['name']):
                groups = re.search(pattern, count['name']).groups()
                type = groups[0]
                id   = groups[1]
                if not type in result:
                    result[type] = []
                result[type].append({
                    'name' : id,
                    'count': count['count']
                })
        return result
