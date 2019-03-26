DROP TABLE IF EXISTS oshkosh_tbl;
CREATE EXTERNAL TABLE IF NOT EXISTS oshkosh_tbl(year INT, month INT,
day INT, time STRING, temperature FLOAT, dewpoint FLOAT, humidity INT, sea_level_pressure FLOAT, visibility FLOAT, wind_direction STRING, wind_speed FLOAT, gust_speed FLOAT, precip FLOAT, events STRING, conditions STRING, wind_degrees INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/final/Oshkosh/';
DROP TABLE IF EXISTS iowacity_tbl;
CREATE EXTERNAL TABLE IF NOT EXISTS iowacity_tbl(year INT, month INT,
day INT, time STRING, temperature FLOAT, dewpoint FLOAT, humidity INT, sea_level_pressure FLOAT, visibility FLOAT, wind_direction STRING, wind_speed FLOAT, gust_speed FLOAT, precip FLOAT, events STRING, conditions STRING, wind_degrees INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/final/IowaCity/';


SELECT
	o.month_d,
	o.hour_d,
	i.hour_d,
	o.avg_temp,
	i.avg_temp
FROM
	(
	SELECT
		month as month_d,
		concat(split(time, ":")[0],split(time," ")[1]) as hour_d,
		'Oshkosh' as city,
		avg(temperature) as avg_temp,
		abs(avg(wind_speed)-50) as avg_wind
	FROM 
		oshkosh_tbl o
	WHERE
		temperature IS NOT NULL AND
		temperature != -9999 AND 
		wind_speed IS NOT NULL AND 
		wind_speed != -9999 AND
		wind_speed != 'Calm'
	GROUP BY
		month,
		concat(split(time, ":")[0],split(time," ")[1]),
		'Oshkosh'
	) o
FULL OUTER JOIN
	(
	SELECT
		month as month_d,
		concat(split(time, ":")[0],split(time," ")[1]) as hour_d,
		'IowaCity' as city,
		avg(temperature) as avg_temp,
		abs(avg(wind_speed)-50) as avg_wind
	FROM 
		iowacity_tbl i
	WHERE
		temperature IS NOT NULL AND
		temperature != -9999 AND 
		wind_speed IS NOT NULL AND 
		wind_speed != -9999 AND
		wind_speed != 'Calm'
	GROUP BY
		month,
		concat(split(time, ":")[0],split(time," ")[1]),
		'IowaCity'
	) i
ON
	o.month_d = i.month_d AND
	o.hour_d = i.hour_d