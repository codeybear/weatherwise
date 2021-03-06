"""All functionality related to dependencies"""

from schedule.models import Common


class Dependency:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    Id = 0
    ActivityId = 0
    PredActivityId = 0
    TypeId = 0
    Length = 0


class DependencyType:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    Id = ""
    Name = ""


class DependencyService:
    @classmethod
    def GetById(cls, dependencyId):
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
    def GetByScheduleId(cls, scheduleId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = """SELECT dependency.* FROM dependency
                       INNER JOIN activity ON activity.id = dependency.ActivityId
                       WHERE activity.ScheduleId = %s"""

                cursor.execute(sql, (str(scheduleId)))
                results = cursor.fetchmany(cursor.rowcount)
                dependencyList = [Dependency(**result) for result in results]

                return dependencyList

        finally:
            connection.close()

    @classmethod
    def GetPredByActivityId(cls, activityId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = """SELECT *
                       FROM dependency
                       WHERE dependency.PredActivityId = %s"""

                cursor.execute(sql, (str(activityId)))
                results = cursor.fetchmany(cursor.rowcount)
                dependencyList = [Dependency(**result) for result in results]

                return dependencyList

        finally:
            connection.close()

    @classmethod
    def GetByActivityId(cls, activityId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = """SELECT dependency.*, dependency_type.Name AS DependencyName, activity.Name AS PredessesorName
                       FROM dependency
                       INNER JOIN dependency_type ON dependency.TypeId = dependency_type.Id
                       INNER JOIN activity ON dependency.PredActivityId = activity.Id
                       WHERE dependency.ActivityId = %s"""

                cursor.execute(sql, (str(activityId)))
                results = cursor.fetchmany(cursor.rowcount)
                dependencyList = [Dependency(**result) for result in results]

                return dependencyList

        finally:
            connection.close()

    @classmethod
    def GetDependencyTypes(cls):
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
    def Add(cls, dependency):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO `dependency` (`ActivityId`, `PredActivityId`, `TypeId`, `Length`) VALUES (%s, 
                      %s, %s, %s) """

                cursor.execute(sql, (dependency.ActivityId, dependency.PredActivityId, dependency.TypeId,
                                     dependency.Length))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Update(cls, dependency):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = """UPDATE `dependency` SET `ActivityId` = %s, `PredActivityId` = %s, `TypeId` = %s, `Length` = %s
                       WHERE Id = %s"""
                cursor.execute(sql, (dependency.ActivityId, dependency.PredActivityId, dependency.TypeId,
                                     dependency.Length, dependency.Id))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Delete(cls, dependency_id):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM dependency WHERE Id = %s"
                cursor.execute(sql, (dependency_id))
                connection.commit()
        finally:
            connection.close()
