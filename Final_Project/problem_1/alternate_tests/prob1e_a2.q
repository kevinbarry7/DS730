DROP TABLE IF EXISTS oshkosh_tbl;
CREATE EXTERNAL TABLE IF NOT EXISTS oshkosh_tbl(year STRING, month STRING,
day STRING, time STRING, temperature FLOAT, dewpoint FLOAT, humidity INT, sea_level_pressure FLOAT, visibility FLOAT, wind_direction STRING, wind_speed FLOAT, gust_speed FLOAT, precip FLOAT, events STRING, conditions STRING, wind_degrees INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/final/Oshkosh/';


SELECT
	concat(hour, ':', minute, ' ', am_pm) as time,
	curr_date,
	prev_date,
	(SELECT 
		min(oo.temperature)
	FROM 
		oshkosh_tbl oo
	WHERE
		to_date(concat_ws('-', oo.year, oo.month, oo.day)) >= sub.prev_date AND 
		to_date(concat_ws('-', oo.year, oo.month, oo.day)) <= sub.curr_date AND 
		cast(split(oo.time, ":")[0] AS int) >= sub.hour AND 
		cast(split(split(oo.time, ":")[1], " ")[0] AS int) >= sub.minute AND 
		split(oo.time, " ")[1] == sub.am_pm AND
		oo.temperature != -9999) AS min_temp
FROM
	(
	SELECT
		cast(split(time, ":")[0] AS int) as hour,
		cast(split(split(time, ":")[1], " ")[0] AS int) as minute,
		split(time, " ")[1] as am_pm,
		to_date(concat_ws('-', year, month, day)) as curr_date,
		date_sub(to_date(concat_ws('-', year, month, day)), 1) as prev_date
	FROM 
		oshkosh_tbl o
	WHERE
		temperature IS NOT NULL AND
		temperature != -9999
	) sub




SELECT
	date_d,
	hour_d,
	min(avg_temp) over(ORDER BY hour_d RANGE BETWEEN CURRENT ROW AND 23 FOLLOWING)
FROM
	(
	SELECT
		to_date(concat_ws('-', year, month, day)) as date_d,
		concat(split(time, ":")[0],split(time," ")[1]) as hour_d,
		24 as counted,
		avg(temperature) as avg_temp
	FROM 
		oshkosh_tbl o
	WHERE
		temperature IS NOT NULL AND
		temperature != -9999
	GROUP BY
		to_date(concat_ws('-', year, month, day)),
		concat(split(time, ":")[0],split(time," ")[1]),
		24
	) sub
