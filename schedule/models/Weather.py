import math
import datetime
import functools
import random
import copy
from operator import itemgetter
from enum import Enum

from schedule.models import Schedule, ScheduleService, Activity, ActivityService, Location, LocationService, Parameter, ParameterService, Dependency, DependencyService 

class ReportType(Enum):
    NORMAL = 1
    WEATHER_AWARE = 2
    STOCHASTIC = 3
    REVERSE = 4

class Weather:
    @classmethod
    def __init__(self, scheduleId):
        scheduleService = ScheduleService
        self.schedule = scheduleService.GetById(scheduleId)
        self.activityList = ActivityService.GetByScheduleId(scheduleId)
        self.locationList = LocationService.GetByScheduleId(scheduleId)
        self.dependencyList = DependencyService.GetByScheduleId(scheduleId)
        self.activityTypeList = ActivityService.GetActivityTypes()

    #@functools.lru_cache(maxsize=None)
    def CalcCRC(K, A, P, dayOfYear, stochastic=False):
        result = 2*math.pi*(dayOfYear/365-P)
        result =  K + A*math.cos(result)

        if stochastic == False:
            return result
        else:
            randomNum = random.random()
            if randomNum < result:
                return 1
            else: 
                return 0 

    def ProcessNewDuration(activity, activityStartDay, activityEndDay, duration):
        activity.StartDate = activityStartDay
        activity.EndDate = activityEndDay
        activity.NewDuration = duration

    @classmethod
    def CalcDaysOfYear(self):
        day = datetime.datetime(2018, 1, 1)
        durationList = []
        endDateList = []

        for dayNum in range(1, 365):
            result = self.CalcScheduleDuration(day, calcType=ReportType.WEATHER_AWARE)
            durationList.append(result[1])
            endDateList.append(result[2])
            day += datetime.timedelta(days=1)

        return (durationList, endDateList);

    @classmethod
    def CalcStochastic(self, iterCount, reportType, duration = 0):
        durationList = []

        if reportType == ReportType.REVERSE:
            # Get the weather aware durations and set these as the start durations for the reverse report
            resultWA = self.CalcScheduleDuration(calcType = ReportType.WEATHER_AWARE)
        
            for counter in range(1, iterCount):
                for idx, activity in enumerate(self.activityList):
                    self.activityList[idx].Duration = resultWA[0][idx].NewDuration

                # Get the planned durations from the weather aware durations with stochastic variations
                result = self.CalcScheduleDuration(calcType = ReportType.REVERSE, stochastic=True)

                for idx, activity in enumerate(self.activityList):
                    self.activityList[idx].Duration = result[0][idx].NewDuration

                result = self.CalcScheduleDuration(startDate=None, calcType=ReportType.NORMAL)
                durationList.append((0, result[1]))  
        else:        
            for counter in range(1, iterCount):
                result = self.CalcScheduleDuration(startDate=None, calcType=reportType, stochastic=True)
                durationList.append((0, result[1]))         

        # Add the extra point to be marked on the chart
        if duration > 0:
            if duration < max(durationList, key=itemgetter(1))[1]:
                durationList.append((0, duration))
                iterCount += 1

        durationList.sort(key=itemgetter(1))

        prevDuration = 0
        thisIndex = 0

        for counter in range(0, iterCount - 1):
            index = ((counter - 0.5) / iterCount) * 100
            listItem = durationList[counter]

            if prevDuration != listItem[1]:    # this makes sure to points with the same duration are plotted in the same place
                thisIndex = index

            durationList[counter] = (thisIndex, listItem[1])
            prevDuration = listItem[1]

        return durationList

    @classmethod
    def CalcScheduleDuration(self, startDate=None, calcType=ReportType.WEATHER_AWARE, stochastic=False):
        if startDate == None:
            startDate = self.schedule.StartDate

        currentDay = self.GetAdjustedDate(startDate, self.schedule.WorkingDays, 0) # adjust the first day to make sure its a working day

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

                    if activity.ActivityTypeId != 7 and calcType != ReportType.NORMAL:
                        dayCoeff = Weather.CalcCRC(float(parameter.K), float(parameter.A), float(parameter.P), currentDayNum, stochastic)
                        #if dayCoeff == 0: raise ValueError("Zero coefficient value occurred, exiting")

                    if calcType == ReportType.REVERSE:
                        actualDuration += 1
                        actualDurationDays += dayCoeff
                    else:
                        actualDuration += dayCoeff
                        actualDurationDays += 1
                    
                    if actualDuration >= activity.Duration:
                        actualDurationDays = math.floor(actualDurationDays)
                        activity.NewDuration = actualDurationDays

                        Weather.ProcessNewDuration(activity, activityStartDay, currentDay, actualDurationDays)
                        currentDay += datetime.timedelta(days=1)
                        break  
                
                currentDay += datetime.timedelta(days=1)

        currentDay -= datetime.timedelta(days=1)
        newScheduleDuration = self.CalcDuration()
        print(f"New schedule duration: {newScheduleDuration} Last day Num: {currentDayNum} Last day {currentDay}") # TODO might need to be -1 here
        self.CreateReportingVariables()
        returnList = copy.deepcopy(self.activityList)
        return (returnList, newScheduleDuration, currentDay.strftime("%d-%m-%Y"))
    
    @classmethod
    def CreateReportingVariables(self):
        for activity in self.activityList:
            activity.FormattedStartDate = activity.StartDate.strftime("%d-%m-%Y")
            activity.FormattedEndDate = activity.EndDate.strftime("%d-%m-%Y")
            activityType = [x for x in self.activityTypeList if activity.ActivityTypeId == x.Id]
            activity.Initial = activityType[0].Initial 

        for dependency in self.dependencyList:
            dependency.FormattedDependencyType = int(dependency.DependencyTypeId) - 1

    @classmethod
    def GetActivityStartDate(self, activity, parameter, currentDay):
        dependencies = [x for x in self.dependencyList if x.ActivityId == activity.Id]
        if len(dependencies) == 0: return currentDay

        # get this activity's predecessors
        dateList = []

        for dependency in dependencies:
            predActivity = [x for x in self.activityList if dependency.PredActivityId == x.Id][0]

            if dependency.DependencyTypeId == 1:
                startDate = predActivity.EndDate + datetime.timedelta(days=1) 
                startDate = self.GetAdjustedDate(startDate, self.schedule.WorkingDays, dependency.DependencyLength)                
                dateList.append(startDate)
            if dependency.DependencyTypeId == 2:
                startDate = predActivity.StartDate
                startDate = self.GetAdjustedDate(startDate, self.schedule.WorkingDays, dependency.DependencyLength)
                dateList.append(startDate)
                
        maxDate = max(dateList)        
        return maxDate

    @classmethod
    def CalcDuration(self):
        startDate = min(activity.StartDate for activity in self.activityList)
        endDate = max(activity.EndDate for activity in self.activityList)
        currentDate = startDate
        duration = 1

        while currentDate != endDate:
            if self.schedule.WorkingDays[currentDate.weekday()]:
                duration += 1

            currentDate += datetime.timedelta(days=1)

        return duration


    @classmethod
    def calcActivityEndDate(self, activityStartDay, actualDurationDays):
        calcDay = activityStartDay
        workingdayCounter = 0

        for daysCounter in range(1, 999999):
            if self.schedule.WorkingDays[calcDay.weekday()]:
                workingdayCounter += 1

            if workingdayCounter == actualDurationDays:
                break

            calcDay += datetime.timedelta(days=1)

        return calcDay

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