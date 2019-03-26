DROP TABLE IF EXISTS oshkosh_tbl;
CREATE EXTERNAL TABLE IF NOT EXISTS oshkosh_tbl(year STRING, month STRING,
day STRING, time STRING, temperature FLOAT, dewpoint FLOAT, humidity INT, sea_level_pressure FLOAT, visibility FLOAT, wind_direction STRING, wind_speed FLOAT, gust_speed FLOAT, precip FLOAT, events STRING, conditions STRING, wind_degrees INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/final/Oshkosh/';


SELECT
	full_date,
	time,
	temperature,
	min(temperature) over(ORDER BY full_date ROWS BETWEEN 1 preceding AND CURRENT ROW) as min_temp,
	max(temperature) over(ORDER BY full_date ROWS BETWEEN 1 preceding AND CURRENT ROW) as max_temp		
FROM
	(
	SELECT
		to_date(concat_ws('-', year, month, day)) as full_date,
		case 
			when length(split(time, ":")[0]) == 1 AND split(time, " ")[1] == 'AM' THEN lpad(split(time, ":")[0],2,'0')
			when split(time, " ")[1] == 'PM' AND split(time, ":")[0] != '12' THEN CAST(CAST(split(time, ":")[0] as int) + 12 AS STRING)
			else split(time, ":")[0]
		end as hour,
		temperature
	FROM
		oshkosh_tbl
	WHERE
		temperature IS NOT NULL
	) sub
