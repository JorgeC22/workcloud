import mariadb

def DB():
    return mariadb.connect(host='localhost',
                            user='root',
                            password='12345',
                            db='workflow',
                            port=3307)
