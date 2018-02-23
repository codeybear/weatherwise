from schedule.models import Common

class Dependency:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    
    Id = 0
    ActivityId = 0
    PredActivityId = 0
    DependencyTypeId = 0
    DependencyLength = 0

class DependencyType:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    Id = ""
    Name = ""

class DependencyService:
    @classmethod
    def GetById(self, dependencyId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM dependency WHERE Id=%s"
                cursor.execute(sql, (str(dependencyId)))
                result = cursor.fetchone()
                dependency = None if result is None else Dependency(**result)
                return dependency

        finally:
            connection.close()

    @classmethod
    def GetByScheduleId(self, scheduleId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT dependency.* FROM dependency \
                       INNER JOIN activity ON activity.id = dependency.ActivityId \
                       WHERE activity.ScheduleId = %s"
                cursor.execute(sql, (str(scheduleId)))
                results = cursor.fetchmany(cursor.rowcount)
                # Convert list of dicts to list of classes
                activityList = [Dependency(**result) for result in results]

                return activityList

        finally:
            connection.close()

    @classmethod 
    def GetByActivityId(self, activityId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT dependency.*, dependency_type.Name AS DependencyName, activity.Name AS PredessesorName  \
                       FROM Dependency \
                       INNER JOIN dependency_type ON dependency.DependencyTypeId = dependency_type.Id \
                       INNER JOIN activity ON dependency.PredActivityId = activity.Id \
                       WHERE dependency.ActivityId = %s"
                       
                cursor.execute(sql, (str(activityId)))
                results = cursor.fetchmany(cursor.rowcount)
                # Convert list of dicts to list of classes
                activityList = [Dependency(**result) for result in results]

                return activityList

        finally:
            connection.close()

    @classmethod
    def GetDependencyTypes(self):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM dependency_type"
                cursor.execute(sql)
                results = cursor.fetchmany(cursor.rowcount)
                dependencyTypeList = [DependencyType(**result) for result in results]

                return dependencyTypeList

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