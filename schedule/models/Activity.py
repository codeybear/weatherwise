import Common

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
    StartDate = ""  # temp field not store in the database
    EndDate = ""    # temp field not store in the database
    NewDuration = 0 # temp field not store in the database

class ActivityService:
    @classmethod
    def GetById(self, uid):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM activity WHERE Id=%s"
                cursor.execute(sql, (str(uid)))
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
                sql = "SELECT * FROM activity WHERE ScheduleId=%s"
                cursor.execute(sql, (str(scheduleId)))
                results = cursor.fetchall()
                # Convert list of dicts to list of classes
                activityList = [Activity(**result) for result in results]

                return activityList

        finally:
            connection.close()

    @classmethod
    def Update(self, activity):
            try:
            with connection.cursor() as cursor:
                sql = "UPDATE `activity` SET `ScheduleId` = %s, `LocationId` = %s, `ActivityTypeId` = %s, `DependencyTypeId` = %s, `DependencyLength` = %s, `Name` = %s, `Duration` = %s) \
                      "WHERE Id = %s"
                      
                cursor.execute(sql, (activity.ScheduleId, activity.LocationId, activity.ActivityTypeId, activity.DependencyTypeId, activity.DependencyLength, activity.Name, activity.Duration))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Add(self, schedule):
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `activity` (`Name`, `Duration`, 'ScheduleId', 'LocationId', 'ActivityTypeId') VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (activity.Name, activity.Duration, activity.ScheduleId, activity.LocationId, activity.ActivityTypeId))
                connection.commit()
        finally:
            connection.close()

