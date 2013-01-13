# -*- coding: utf-8 -*-
"""
Counter Shard Utilities.

@copyright: 2012 by Tatsuya Koyama
            (www.tatsuya-koyama.com)
"""

import random

from google.appengine.api import memcache
from google.appengine.ext import db

"""
See: https://developers.google.com/appengine/articles/sharding_counters
-----
* While App Engine's datastore scales to support a huge number of entities,
  it is important to note that you can only expect to update any single entity
  or entity group about five times a second.
"""


class GeneralCounterShardConfig(db.Model):
    """Tracks the number of shards for each named counter."""
    name       = db.StringProperty(required=True)
    num_shards = db.IntegerProperty(required=True, default=20)


class GeneralCounterShard(db.Model):
    """Shards for each named counter"""
    name  = db.StringProperty(required=True)
    count = db.IntegerProperty(required=True, default=0)


def get_count(name):
    """
    Retrieve the value for a given sharded counter.
    Parameters:
      name: The name of the counter
    """
    total = memcache.get(name)
    if total is None:
        total = 0
        for counter in GeneralCounterShard.all().filter('name = ', name):
            total += counter.count
        memcache.add(name, str(total), 60)
    return total


def get_all_count():
    """
    Retrieve the values for all sharded counter.
    """
    count_list = []
    for config in GeneralCounterShardConfig.all():
        count_list.append({
            'name' : config.name,
            'count': get_count(config.name)
            })
    return count_list


def increment(name):
    """
    Increment the value for a given sharded counter.
    Parameters:
      name: The name of the counter
    """
    config = GeneralCounterShardConfig.get_or_insert(name, name=name)
    def txn():
        index      = random.randint(0, config.num_shards - 1)
        shard_name = name + "_" + str(index)
        counter    = GeneralCounterShard.get_by_key_name(shard_name)
        if counter is None:
            counter = GeneralCounterShard(key_name=shard_name, name=name)
        counter.count += 1
        counter.put()
    db.run_in_transaction(txn)
    memcache.incr(name)


def increase_shards(name, num):
    """
    Increase the number of shards for a given sharded counter.
    Will never decrease the number of shards.

    Parameters:
      name: The name of the counter
      num : How many shards to use
    """
    config = GeneralCounterShardConfig.get_or_insert(name, name=name)
    def txn():
        if config.num_shards < num:
            config.num_shards = num
            config.put()
    db.run_in_transaction(txn)
