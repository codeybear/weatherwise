import Common

class Dependency:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    
    Id = 0
    ActivityId = 0
    PredActivityId = 0

class DependencyService:
    @classmethod
    def GetByScheduleId(self, scheduleId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT dependency.* FROM dependency \
                       INNER JOIN activity ON activity.id = dependency.ActivityId \
                       WHERE activity.ScheduleId = %s"
                cursor.execute(sql, (str(scheduleId)))
                results = cursor.fetchall()
                # Convert list of dicts to list of classes
                activityList = [Dependency(**result) for result in results]

                return activityList

        finally:
            connection.close()