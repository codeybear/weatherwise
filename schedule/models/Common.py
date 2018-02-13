import pymysql

def getconnection():
    return pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='weather',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)