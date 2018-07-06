from django.conf import settings
import pymysql

def getconnection():
    return pymysql.connect(host=settings.DATABASES['default']['HOST'],
                           user=settings.DATABASES['default']['USER'],
                           password=settings.DATABASES['default']['PASSWORD'],
                           db=settings.DATABASES['default']['NAME'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)