DROP TABLE IF EXISTS oshkosh_tbl;
CREATE EXTERNAL TABLE IF NOT EXISTS oshkosh_tbl(year INT, month INT,
day INT, time STRING, temperature FLOAT, dewpoint FLOAT, humidity INT, sea_level_pressure FLOAT, visibility FLOAT, wind_direction STRING, wind_speed FLOAT, gust_speed FLOAT, precip FLOAT, events STRING, conditions STRING, wind_degrees INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/final/Oshkosh/';


SELECT
	year,
	month,
	week,
	avg_temp
FROM 
	(
	SELECT
		year,
		month,
		CASE
			WHEN day >= 1 and day <= 7 THEN 'week_1'
			WHEN day >= 8 and day <= 14 THEN 'week_2'
			WHEN day >= 15 and day <= 21 THEN 'week_3'
			WHEN day >= 22 and day <= 28 THEN 'week_4'
			WHEN day >= 29 and day <= 31 THEN 'week_5'
		END as week,
		sum(temperature)/count(temperature) as avg_temp
	FROM 
		oshkosh_tbl o
	WHERE
		temperature IS NOT NULL AND 
		temperature != -9999
	GROUP BY
		year,
		month,
		CASE
			WHEN day >= 1 and day <= 7 THEN 'week_1'
			WHEN day >= 8 and day <= 14 THEN 'week_2'
			WHEN day >= 15 and day <= 21 THEN 'week_3'
			WHEN day >= 22 and day <= 28 THEN 'week_4'
			WHEN day >= 29 and day <= 31 THEN 'week_5'
		END
	) sub
ORDER BY
	avg_temp DESC
LIMIT 1