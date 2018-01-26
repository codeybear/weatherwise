import Common

class Parameter:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    Uid = 0
    ActivityId = 0
    Lat = 0.0
    Long = 0.0
    K = 0.0
    A = 0.0
    P = 0.0

class ParameterService:
    @classmethod
    def GetByLatLong(self, ActivityTypeId, lat, long):
        latRounded = round(lat, 1)
        longRounded = round(long, 1)

        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM parameter WHERE ActivityTypeId=%s AND Lat=%s AND parameter.Long=%s"
                cursor.execute(sql, (str(ActivityTypeId), str(latRounded), str(longRounded)))
                result = cursor.fetchone()
                parameter = None if result is None else Parameter(**result)
                return parameter

        finally:
            connection.close()