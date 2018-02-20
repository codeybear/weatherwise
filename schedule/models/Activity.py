from schedule.models import Common

class Activity:
    def __init__(self, **entries):
        self.__dict__.update(entries)
    
    Id = ""
    Name = ""
    Duration = 0
    ScheduleId = 0
    LocationId = 0
    ActivityTypeId = 0
    DependencyTypeId = 0
    DependencyLength = 0
    StartDate = ""      # temp field not stored in the database
    EndDate = ""        # temp field not stored in the database
    NewDuration = 0     # temp field not stored in the database

class ActivityType:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    Id = ""
    Name = ""

class ActivityService:
    @classmethod
    def GetById(self, activityId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM activity WHERE Id=%s"
                cursor.execute(sql, (str(activityId)))
                result = cursor.fetchone()
                activity = None if result is None else Activity(**result)
                return activity

        finally:
            connection.close()

    @classmethod
    def GetByScheduleId(self, scheduleId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql= "SELECT activity.*, activity_type.Name AS ActivityTypeName, location.Name AS LocationName \
                      FROM activity \
                      INNER JOIN activity_type ON activity.ActivityTypeId = activity_type.Id \
                      INNER JOIN location ON activity.LocationId = location.Id \
                      WHERE activity.ScheduleId=%s"

                #sql = "SELECT * FROM activity WHERE ScheduleId=%s"
                cursor.execute(sql, (str(scheduleId)))
                results = cursor.fetchall()
                # Convert list of dicts to list of classes
                activityList = [Activity(**result) for result in results]

                return activityList

        finally:
            connection.close()

    @classmethod
    def GetActivityTypes(self):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM activity_type"
                cursor.execute(sql)
                results = cursor.fetchall()
                # Convert list of dicts to list of classes
                activityTypeList = [ActivityType(**result) for result in results]

                return activityTypeList

        finally:
            connection.close()        

    @classmethod
    def Update(self, activity):
        connection = Common.getconnection()
        
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `activity` SET `ScheduleId` = %s, `LocationId` = %s, `ActivityTypeId` = %s, `Name` = %s, `Duration` = %s \
                       WHERE Id = %s"
                      
                cursor.execute(sql, (activity.ScheduleId, activity.LocationId, activity.ActivityTypeId, activity.Name, activity.Duration, activity.Id))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Add(self, activity):
        connection = Common.getconnection()
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `activity` (`Name`, `Duration`, `ScheduleId`, `LocationId`, `ActivityTypeId`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (activity.Name, activity.Duration, activity.ScheduleId, activity.LocationId, activity.ActivityTypeId))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Delete(self, activity_id):
        connection = Common.getconnection()
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM dependency WHERE ActivityId = %s"
                cursor.execute(sql, (activity_id))
                connection.commit()                

                sql = "DELETE FROM activity WHERE Id = %s"
                cursor.execute(sql, (activity_id))
                connection.commit()
        finally:
            connection.close()
        