SELECT * FROM activity
WHERE ScheduleId = 2 AND 
activity.Pos < (SELECT pos FROM activity WHERE activity.Id = 12)

SELECT activity.*, (SELECT MAX(Pos) + 1 FROM activity WHERE scheduleId = 1) AS NewPos FROM activity WHERE Id = 17

SET SQL_SAFE_UPDATES = 0;

SET @rank:=0;

UPDATE activity
SET Pos=@rank:=@rank+1
where ScheduleId = 2
order by Pos

SELECT * FROM activity where ScheduleId = 3