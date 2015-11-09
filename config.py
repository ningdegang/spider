#!/usr/bin/env python
# -*- coding:utf-8 -*-
config ={
    "sqlalchemy":
    { 
        "url":"mysql+pymysql://root:root@localhost/spider",
        "pool_size":10,
        "max_overflow": 20,
        "pool_recycle":600,
        "echo":1,
    }
}
