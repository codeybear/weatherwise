from schedule.models import Common

class Schedule:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    Id = 0    
    Name = ""
    StartDate = ""
    WorkingDay0 = False
    WorkingDay1 = False
    WorkingDay2 = False
    WorkingDay3 = False
    WorkingDay4 = False
    WorkingDay5 = False
    WorkingDay6 = False
    WorkingDays = []   # Represents the above information in an array for convenience

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
                return schedule

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