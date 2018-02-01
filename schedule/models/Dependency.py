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


    @classmethod
    def Add(self, dependency):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `dependency` (`ActivityId`, `PredActivityId`) VALUES (%s, %s)"
                cursor.execute(sql, (dependency.ActivityId, dependency.PredActivityId))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Update(self, schedule):
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `dependency` SET `ActivityId` = %s, `PredActivityId` = %s \
                       WHERE Id = %s"
                cursor.execute(sql, (schedule.Id,  schedule.Name, schedule.StartDate, schedule.WorkingDay0))
                connection.commit()
        finally:
            connection.close()
    