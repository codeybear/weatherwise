"""Main reporting functionality"""

import copy
import datetime
import math
import random
from enum import Enum
from operator import itemgetter

from schedule.models import ScheduleService, ActivityService, LocationService, ParameterService, DependencyService


class ReportType(Enum):
    NORMAL = 1
    WEATHER_AWARE = 2
    STOCHASTIC = 3
    REVERSE = 4


class Weather:
    def __init__(self, scheduleId):
        scheduleService = ScheduleService
        self.schedule = scheduleService.GetById(scheduleId)
        self.activityList = ActivityService.GetByScheduleId(scheduleId)
        self.locationList = LocationService.GetByScheduleId(scheduleId)
        self.dependencyList = DependencyService.GetByScheduleId(scheduleId)
        self.activityTypeList = ActivityService.GetActivityTypes()

    @classmethod
    def CalcCRC(cls, K, A, P, dayOfYear, stochastic=False):
        """Get the work effectiveness coefficient for this day of the year"""
        result = 2 * math.pi * (dayOfYear / 365 - P)
        result = K + A * math.cos(result)

        if not stochastic:
            return result
        else:
            randomNum = random.random()
            if randomNum < result:
                return 1
            else:
                return 0

    @classmethod
    def ProcessNewDuration(cls, activity, activityStartDay, activityEndDay, duration):
        """An activity duration has been calculated so store the key information"""
        activity.StartDate = activityStartDay
        activity.EndDate = activityEndDay
        activity.NewDuration = duration

    def CalcDaysOfYear(self):
        """Calculate the weather aware duration for a given schedule for every day of the year"""
        day = datetime.date(2100, 1, 1)
        durationList = []
        endDateList = []

        for _ in range(365):
            result = self.CalcScheduleDuration(day, calcType=ReportType.WEATHER_AWARE)
            durationList.append(result[1])
            endDateList.append(result[2])
            day += datetime.timedelta(days=1)

        return (durationList, endDateList);

    def CalcStochastic(self, iterCount, reportType, duration=0):
        """"Calculate a series of weather aware reports with random variations.
        
        Effectively a monte carlo simulation that will produce the probability of a given project duration occuring."""
        durationList = []

        if reportType == ReportType.REVERSE:
            # Get the weather aware durations and set these as the start durations for the reverse report
            resultWA = self.CalcScheduleDuration(calcType=ReportType.WEATHER_AWARE)

            for _ in range(iterCount):
                for idx, _ in enumerate(self.activityList):
                    self.activityList[idx].Duration = resultWA[0][idx].NewDuration

                # Get the planned durations from the weather aware durations with stochastic variations
                _, duration, _ = self.CalcScheduleDuration(calcType=ReportType.REVERSE, stochastic=True)
                durationList.append((0, duration))
        else:
            for _ in range(iterCount):
                result = self.CalcScheduleDuration(startDate=None, calcType=reportType, stochastic=True)
                durationList.append((0, result[1]))

        # Add the extra point to be marked on the chart
        if duration > 0:
            if duration < max(durationList, key=itemgetter(1))[1]:
                durationList.append((0, duration))
                iterCount += 1

        durationList.sort(key=itemgetter(1))
        durationList = Weather.CalcStochasticProbabilities(iterCount, durationList)

        return durationList

    @classmethod
    def CalcStochasticProbabilities(cls, iterCount, durationList):
        """Calculate the probabity of each schedule duration as a percentage"""
        prevDuration = 0
        thisIndex = 0

        for counter in range(0, iterCount - 1):
            index = ((counter - 0.5) / iterCount) * 100
            index = round(index, 2)
            listItem = durationList[counter]

            # this makes sure that points with the same duration are plotted in the same place
            if prevDuration != listItem[1]:
                thisIndex = index

            durationList[counter] = (thisIndex, listItem[1])
            prevDuration = listItem[1]

        return durationList

    def CalcScheduleDuration(self, startDate=None, calcType=ReportType.WEATHER_AWARE, stochastic=False):
        """Calculate the extended weather affected activity durations"""
        if startDate == None:
            startDate = self.schedule.StartDate

        # adjust the first day to make sure its a working day
        currentDay = Weather.GetAdjustedDate(startDate, self.schedule.WorkingDays, 0)

        for activity in self.activityList:
            location = next(l for l in self.locationList if l.Id == activity.LocationId)
            parameter = ParameterService.GetByLatLong(activity.ActivityTypeId, location.Lat, location.Long)
            activityStartDay = self.GetActivityStartDate(activity, currentDay)
            currentDay = self.CalcActivityExtension(activity, activityStartDay, calcType, parameter, stochastic)
        
        currentDay -= datetime.timedelta(days=1)

        if calcType == ReportType.REVERSE: 
            self.FindReversedReportDates()

        newScheduleDuration = self.CalcDuration()
        self.CreateReportingVariables()
        returnList = copy.deepcopy(self.activityList)  # ensure deep copy as it is manipulated outside of this function

        return (returnList, newScheduleDuration, currentDay.strftime("%d-%m-%Y"))

    def CalcActivityExtension(self, activity, activityStartDay, calcType, parameter, stochastic):
        """Get an activities weather aware extension to its duration."""
        currentDay = activityStartDay
        actualDuration = 0 
        actualDurationDays = 0

        while True:
            if self.schedule.WorkingDays[currentDay.weekday()]:
                currentDayNum = currentDay.timetuple().tm_yday
                dayCoeff = 1
                stageCompleted = self.CheckProjectState(currentDay)

                if activity.ActivityTypeId != 7 and calcType != ReportType.NORMAL and not stageCompleted:
                    dayCoeff = Weather.CalcCRC(float(parameter.K), float(parameter.A), float(parameter.P),
                                                currentDayNum, stochastic)

                if calcType == ReportType.REVERSE:
                    actualDuration += 1
                    actualDurationDays += dayCoeff
                else:
                    actualDuration += dayCoeff
                    actualDurationDays += 1

                if actualDuration >= activity.Duration:
                    actualDurationDays = math.floor(actualDurationDays)
                    self.ProcessNewDuration(activity, activityStartDay, currentDay, actualDurationDays)
                    currentDay += datetime.timedelta(days=1)

                    return currentDay

            currentDay += datetime.timedelta(days=1)

    def FindReversedReportDates(self):
        '''This method fixes the dates created by CalcScheduleDuration() when using
        calcType=REVERSE, this method needs to find the reversed durations
        first then run this method to find the correct dates'''
        savedList = copy.deepcopy(self.activityList)

        # run the normal report on the new reverse activity durations
        for activity in self.activityList:
            activity.Duration = activity.NewDuration

        activities, _, _ = self.CalcScheduleDuration(calcType=ReportType.NORMAL)

        # now restore the original durations to continue
        for idx, activity in enumerate(activities):
            self.activityList[idx].Duration = savedList[idx].Duration

    def CreateReportingVariables(self):
        """Create additional activity fields for reporting purposes"""
        for activity in self.activityList:
            activity.FormattedStartDate = activity.StartDate.strftime("%d-%m-%Y")
            activity.FormattedEndDate = activity.EndDate.strftime("%d-%m-%Y")
            activityType = [x for x in self.activityTypeList if activity.ActivityTypeId == x.Id]
            activity.Initial = activityType[0].Initial

        for dependency in self.dependencyList:
            dependency.FormattedDependencyType = int(dependency.TypeId) - 1

    def GetActivityStartDate(self, activity, currentDay):
        """Find an activity's start date based on its predecessors dependencies."""
        dependencies = [x for x in self.dependencyList if x.ActivityId == activity.Id]
        if len(dependencies) == 0: return currentDay

        # get this activity's predecessors
        dateList = []

        for dependency in dependencies:
            predActivity = [x for x in self.activityList if dependency.PredActivityId == x.Id][0]

            if dependency.TypeId == 1:
                startDate = predActivity.EndDate + datetime.timedelta(days=1)
                startDate = self.GetAdjustedDate(startDate, self.schedule.WorkingDays, dependency.Length)
                dateList.append(startDate)
            if dependency.TypeId == 2:
                startDate = predActivity.StartDate
                startDate = self.GetAdjustedDate(startDate, self.schedule.WorkingDays, dependency.Length)
                dateList.append(startDate)

        maxDate = max(dateList)
        return maxDate

    def CalcDuration(self):
        """Calculate the length of the current schedule in working days"""
        startDate = min(activity.StartDate for activity in self.activityList)
        endDate = max(activity.EndDate for activity in self.activityList)
        currentDate = startDate
        duration = 1

        while currentDate != endDate:
            if self.schedule.WorkingDays[currentDate.weekday()]:
                duration += 1

            currentDate += datetime.timedelta(days=1)

        return duration

    def calcActivityEndDate(self, activityStartDay, actualDurationDays):
        """Calculate the end date for an activity"""
        calcDay = activityStartDay
        workingdayCounter = 0

        while True:
            if self.schedule.WorkingDays[calcDay.weekday()]:
                workingdayCounter += 1

            if workingdayCounter == actualDurationDays:
                break

            calcDay += datetime.timedelta(days=1)

        return calcDay

    @classmethod
    def GetAdjustedDate(cls, date, workingDays, adjustment, parameter=None):
        """Move forward or backwards by a given number of working days"""
        currentDate = date
        dayCount = 0

        if adjustment != 0:  # searching forwards or backwards
            while True:
                if adjustment > 0:  # count forwards or backwards in days depending on the adjustment
                    currentDate += datetime.timedelta(days=1)
                else:
                    currentDate -= datetime.timedelta(days=1)

                if parameter:  # if there are parameters then we are incrementing by weather affected days
                    dayCoeff = Weather.CalcCRC(float(parameter.K), float(parameter.A), float(parameter.P),
                                               currentDate.timetuple().tm_yday)
                else:
                    dayCoeff = 1

                if workingDays[currentDate.weekday()]: dayCount += dayCoeff
                if dayCount >= abs(adjustment): break
        else:  # No adjustment just find the first working day
            while True:
                if workingDays[currentDate.weekday()]: break
                currentDate += datetime.timedelta(days=1)

        return currentDate

    def CheckProjectState(self, currentDay):
        """ Check to see if this stage on the project has been completed """
        status = False

        if self.schedule.StatusTypeId == 2:
            if self.schedule.StatusDate is not None:
                if currentDay < self.schedule.StatusDate:
                    status = True
        elif self.schedule.StatusTypeId == 3:
            status = True

        return status
