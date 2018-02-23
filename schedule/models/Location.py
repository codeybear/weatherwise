from schedule.models import Common

class Location:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    Id = 0
    ScheduleId = 0
    Name = ''
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
                results = cursor.fetchmany(cursor.rowcount)
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
                cursor.execute(sql, (str(Id)))
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
                sql = "INSERT INTO `location` (`ScheduleId`, `Name`, `Lat`, `Long`) \
                       VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (location.ScheduleId, location.Name, location.Lat, location.Long))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Update(self, location):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `location` SET `Name` = %s, `ScheduleId` = %s, `Lat` = %s, `Long` = %s \
                       WHERE Id = %s"
                
                cursor.execute(sql, (location.Name, location.ScheduleId, location.Lat, location.Long, location.Id))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Delete(self, location_id):
        connection = Common.getconnection()
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM location WHERE Id = %s"
                cursor.execute(sql, (location_id))
                connection.commit()
        finally:
            connection.close()
        