from schedule.models import Common

class Schedule:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    Id = 0    
    Name = ""
    StartDate = ""
    StartDateDisplay = ""
    StatusTypeId = 0
    StatusDate = ""
    WorkingDay0 = False
    WorkingDay1 = False
    WorkingDay2 = False
    WorkingDay3 = False
    WorkingDay4 = False
    WorkingDay5 = False
    WorkingDay6 = False
    WorkingDays = []   # Represents the above information in an array for convenience

class StatusType:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    Id = ""
    Name = ""


class ScheduleService:
    @classmethod
    def GetById(self, uid):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM schedule WHERE Id=%s"
                cursor.execute(sql, (str(uid)))
                result = cursor.fetchone()
                schedule = None if result is None else Schedule(**result)
                schedule = self.__GetWorkingDays(schedule)
                schedule.StartDateDisplay = schedule.StartDate.strftime("%d/%m/%Y")

                # if schedule.StatusDate is not None:
                #     schedule.StatusDateDisplay = schedule.StatusDate.strftime("%d/%m/%Y")

                return schedule

        finally:
            connection.close()

    @classmethod
    def GetAll(self):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM schedule"
                cursor.execute(sql)
                results = cursor.fetchmany(cursor.rowcount)
                scheduleList = [Schedule(**result) for result in results]
                return scheduleList

        finally:
            connection.close()

    @classmethod
    def Add(self, schedule):
        connection = Common.getconnection()
        
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `schedule` (`Name`, `StartDate`, `WorkingDay0`, `WorkingDay1`, `WorkingDay2`, `WorkingDay3`, `WorkingDay4`, `WorkingDay5`, `WorkingDay6`) \
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (schedule.Name, schedule.StartDate, schedule.WorkingDay0, schedule.WorkingDay1, schedule.WorkingDay2, schedule.WorkingDay3, schedule.WorkingDay4, schedule.WorkingDay5, schedule.WorkingDay6))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Update(self, schedule):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `schedule` SET `Name` = %s, `StartDate` = %s, `WorkingDay0` = %s, `WorkingDay1` = %s, `WorkingDay2` = %s, `WorkingDay3` = %s, `WorkingDay4` = %s, `WorkingDay5` = %s, `WorkingDay6` = %s \
                       WHERE Id = %s"
                
                cursor.execute(sql, (schedule.Name, schedule.StartDate, schedule.WorkingDay0, schedule.WorkingDay1, schedule.WorkingDay2, schedule.WorkingDay3, schedule.WorkingDay4, schedule.WorkingDay5, schedule.WorkingDay6, schedule.Id))
                connection.commit()
        finally:
            connection.close()

    @classmethod
    def Delete(self, schedule_id):
        connection = Common.getconnection()
        
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM schedule WHERE Id = %s"
                cursor.execute(sql, (schedule_id))
                connection.commit()                
        finally:
            connection.close()

    @classmethod
    def __GetWorkingDays(self, schedule):
        schedule.WorkingDays = [schedule.WorkingDay0, 
                                schedule.WorkingDay1, 
                                schedule.WorkingDay2, 
                                schedule.WorkingDay3, 
                                schedule.WorkingDay4, 
                                schedule.WorkingDay5, 
                                schedule.WorkingDay6]
        return schedule

    @classmethod
    def GetStatusTypes(self):
        connection = Common.getconnection()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT Id, Name FROM status_type"
                cursor.execute(sql)
                results = cursor.fetchmany(cursor.rowcount)
                # Convert list of dicts to list of classes
                statusTypeList = [StatusType(**result) for result in results]

                return statusTypeList

        finally:
            connection.close()