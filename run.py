#!/usr/bin/env python
# -*- coding:utf-8 -*-

import models

def main():
    models.init_db()
    session = models.Session()
    users = session.query(models.User)
    user = users.filter_by(username="winning").first()
    user.password = "degang"
    session.flush()
    session.commit()
    asdf
    shit
    asdfas
    henahao 
    asdfasdf

if __name__ == "__main__":
    main()
