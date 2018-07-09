#!/usr/bin/env python
# coding=utf-8

import random

import redis

from .redis_config import (
    REDIS_KEY,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_HOST,
    REDIS_MAX_CONNECTION,
)


class RedisClient:
    """
    edis 数据库，使用了其`有序集合`的数据结构
    （可按分数排序，key 值不能重复）
    """

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        conn_pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=password,
            max_connections=REDIS_MAX_CONNECTION,
        )
        self.redis = redis.Redis(connection_pool=conn_pool)

