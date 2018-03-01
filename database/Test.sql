SELECT activity.*, (SELECT MAX(Pos) + 1 FROM activity WHERE scheduleId = 1) AS NewPos FROM activity WHERE Id = 17

SET @rank:=0;

UPDATE activity
SET Pos=@rank:=@rank+1
where ScheduleId = 5
order by Pos

SELECT if(@a, @a:=@a+1, @a:=1), pos as rownum
FROM activity
WHERE scheduleId = 5

/* Need to test this, will it carry on? */
UPDATE activity
SET Pos=if(@a, @a:=@a+1, @a:=1)
where ScheduleId = 5
order by Pos

select * from activity where scheduleId = 5

IF (SELECT MAX(Pos) + 1 FROM activity WHERE scheduleId = 5) = null, 1, 0)