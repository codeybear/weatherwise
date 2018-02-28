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
    Pos = 0
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
    def GetByLocationId(self, locationId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM activity WHERE LocationId=%s"
                cursor.execute(sql, (str(locationId)))
                results = cursor.fetchmany(cursor.rowcount)
                activityList = [Activity(**result) for result in results]
                return activityList

        finally:
            connection.close()

    @classmethod
    def GetPredecessors(self, activityId, scheduleId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM activity \
                       WHERE ScheduleId = %s AND \
                       activity.Pos < (SELECT pos FROM activity WHERE activity.Id = %s)"
                cursor.execute(sql, (str(scheduleId), str(activityId)))
                results = cursor.fetchmany(cursor.rowcount)
                activityList = [Activity(**result) for result in results]
                return activityList

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
                      WHERE activity.ScheduleId=%s \
                      ORDER BY pos"

                cursor.execute(sql, (str(scheduleId)))
                results = cursor.fetchmany(cursor.rowcount)
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
                results = cursor.fetchmany(cursor.rowcount)
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
    def Add(self, activity, scheduleId):
        connection = Common.getconnection()
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT @rownum:= (SELECT MAX(Pos) + 1 FROM activity WHERE scheduleId = %s)"
                cursor.execute(sql, (scheduleId))
                id = cursor.lastrowid

                sql = "INSERT INTO `activity` (`Name`, `Duration`, `ScheduleId`, `LocationId`, `ActivityTypeId`, `Pos`) VALUES (%s, %s, %s, %s, %s, @rownum)"
                cursor.execute(sql, (activity.Name, activity.Duration, activity.ScheduleId, activity.LocationId, activity.ActivityTypeId))
                connection.commit()
        finally:
            connection.close()

    @classmethod 
    def UpdatePositions(self, scheduleId):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                # sql = ""
                # cursor.execute(sql)                

                sql = "UPDATE activity \
                       SET Pos=if(@a, @a:=@a+1, @a:=1) \
                       where ScheduleId = %s \
                       order by Pos"
                cursor.execute(sql, (scheduleId))
                connection.commit()
        finally:
            connection.close()

    @classmethod 
    def SetNewPos(self, activityId):
        newPos = 0

        if activityId != 0:
            activity = self.GetById(activityId)
            newPos = activity.Pos + 0.5

        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE activity SET Pos=%s where activityId = %s"
                cursor.execute(sql, (activityId, newPos))
                connection.commit()
        finally:
            connection.close()    

        self.UpdatePositions()    
        
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