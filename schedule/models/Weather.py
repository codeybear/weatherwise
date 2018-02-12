import math
import datetime
from Schedule import *
from Activity import *
from Location import *
from Parameter import *
from Dependency import *

class Weather:
    @classmethod
    def __init__(self, scheduleId):
        scheduleService = ScheduleService
        self.schedule = scheduleService.GetById(scheduleId)
        self.activityList = ActivityService.GetByScheduleId(scheduleId)
        self.locationList = LocationService.GetByScheduleId(scheduleId)
        self.dependencyList = DependencyService.GetByScheduleId(scheduleId)

    def CalcCRC(K, A, P, dayOfYear):
        result = 2*math.pi*(dayOfYear/365-P)
        return K + A*math.cos(result)

    def ProcessNewDuration(activity, activityStartDay, activityEndDay, duration):
        activity.StartDate = activityStartDay
        activity.EndDate = activityEndDay
        activity.NewDuration = duration

    @classmethod
    def CalcScheduleDuration(self):
        currentDay = self.GetAdjustedDate(self.schedule.StartDate, self.schedule.WorkingDays, 0) # adjust the first day to make sure its a working day
        newScheduleDuration = 0

        for activity in self.activityList:
            actualDuration = 0
            actualDurationDays = 0

            location = next(l for l in self.locationList if l.Id == activity.LocationId)
            parameter = ParameterService.GetByLatLong(activity.ActivityTypeId, location.Lat, location.Long)
            activityStartDay = self.GetActivityStartDate(activity, parameter, currentDay)
            currentDay = activityStartDay            

            for counter in range(1, 9999):
                if self.schedule.WorkingDays[currentDay.weekday()]:
                    currentDayNum = currentDay.timetuple().tm_yday
                    dayCoeff = 1

                    if activity.ActivityTypeId != 7:
                        dayCoeff = Weather.CalcCRC(float(parameter.K), float(parameter.A), float(parameter.P), currentDayNum)
                        if dayCoeff == 0: raise ValueError("Zero coefficient value occurred, exiting")

                    actualDuration += dayCoeff
                    actualDurationDays += 1

                    if actualDuration >= activity.Duration:
                        activity.NewDuration = actualDurationDays
                        newScheduleDuration += actualDurationDays
                        Weather.ProcessNewDuration(activity, activityStartDay, currentDay, actualDurationDays)
                        currentDay += datetime.timedelta(days=1)
                        break  
                
                currentDay += datetime.timedelta(days=1)

        print(f"New schedule duration: {newScheduleDuration} Last day Num: {currentDayNum} Last day {currentDay}") # TODO might need to be -1 here
        return self.activityList

    @classmethod
    def GetActivityStartDate(self, activity, parameter, currentDay):
        dependencies = [x for x in self.dependencyList if x.ActivityId == activity.Id]
        if len(dependencies) == 0: return currentDay

        # get this activity predessesors
        predActivities = [x for x in self.activityList for y in dependencies if x.Id == y.PredActivityId]

        # Changes:
        # go through the dates get start or end accordingly
        # Adjust the dates add this to a new list
        # Choose the max from this new list

        if activity.DependencyTypeId == 1:
            predActivity = max(predActivities, key=lambda item: item.EndDate)
            startDate = predActivity.EndDate + datetime.timedelta(days=1)

            if activity.DependencyLength > 0:   # A finish to start relationship with a negative length should be a weather aware adjustment (else statement)
                startDate = self.GetAdjustedDate(startDate, self.schedule.WorkingDays, activity.DependencyLength)
            else:
                startDate = self.GetAdjustedDate(startDate, self.schedule.WorkingDays, activity.DependencyLength, parameter)

            return startDate
        if activity.DependencyTypeId == 2:
            predActivity = min(predActivities, key=lambda item: item.StartDate)
            startDate = predActivity.StartDate

            if activity.DependencyLength < 0:   # A start to start relationship with a positive length should be a weather aware adjustment (else statement)
                startDate = self.GetAdjustedDate(startDate, self.schedule.WorkingDays, activity.DependencyLength)
            else:
                startDate = self.GetAdjustedDate(startDate, self.schedule.WorkingDays, activity.DependencyLength, parameter)

            return startDate
        else:
            return currentDay        # is this how we should setup the default relationship?

    def GetAdjustedDate(date, workingDays, adjustment, parameter = None):
        currentDate = date
        dayCount = 0

        if adjustment != 0:          # searching forwards or backwards
            while True:
                if adjustment > 0:   # count forwards or backwards in days depending on the adjustment
                    currentDate += datetime.timedelta(days=1)
                else:
                    currentDate -= datetime.timedelta(days=1)

                if parameter:        # if there are parameters then we are incrementing by weather affected days
                    dayCoeff = Weather.CalcCRC(float(parameter.K), float(parameter.A), float(parameter.P), currentDate.timetuple().tm_yday)
                else:
                    dayCoeff = 1

                if workingDays[currentDate.weekday()]: dayCount += dayCoeff
                if dayCount >= abs(adjustment): break
        else:                        # No adjustment just find the first working day
            while True:
                if workingDays[currentDate.weekday()]: break
                currentDate += datetime.timedelta(days=1)
                
        return currentDate