from schedule.models import Common

class Location:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    Id = ""
    Lat = 0.0
    Long = 0.0

class LocationService:
    @classmethod
    def GetByScheduleId(self, ScheduleId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM location WHERE ScheduleId=%s"
                cursor.execute(sql, (str(ScheduleId)))
                results = cursor.fetchall()
                locationList = [Location(**result) for result in results]
                return locationList

        finally:
            connection.close()

    @classmethod
    def GetById(self, Id):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM location WHERE Id=%s"
                cursor.execute(sql, (str(uid)))
                result = cursor.fetchone()
                location = None if result is None else Location(**result)
                return location

        finally:
            connection.close()

    @classmethod
    def Add(self, location):
        connection = Common.getconnection()
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `location` (`ScheduleId`, `Lat`, `Long`) \
                       VALUES (%s, %s, %s)"
                cursor.execute(sql, (location.ScheduleId, location.Lat, location.Long))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Update(self, location):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `location` SET `ScheduleId` = %s, `Lat` = %s, `Long` = %s
                       WHERE Id = %s"
                
                cursor.execute(sql, (location.ScheduleId, location.Lat, location.Long, location.Id))
                connection.commit()
        finally:
            connection.close()
