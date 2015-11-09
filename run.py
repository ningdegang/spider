#!/usr/bin/env python
# -*- coding:utf-8 -*-

import models

def main():
    models.init_db()
    user = models.User(username="winning", password="asdfafd")
    session = models.Session()
    session.add(user)
    session.flush()
    session.commit()

if __name__ == "__main__":
    main()
