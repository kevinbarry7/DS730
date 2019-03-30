DROP TABLE IF EXISTS oshkosh_tbl;
CREATE EXTERNAL TABLE IF NOT EXISTS oshkosh_tbl(year INT, month INT,
day INT, time STRING, temperature FLOAT, dewpoint FLOAT, humidity INT, sea_level_pressure FLOAT, visibility FLOAT, wind_direction STRING, wind_speed FLOAT, gust_speed FLOAT, precip FLOAT, events STRING, conditions STRING, wind_degrees INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/final/Oshkosh/';


SELECT
	'cold' as temp,
	COUNT(DISTINCT concat_ws('/', CAST(month AS STRING), CAST(day AS STRING), CAST(year AS STRING))) as num_days
FROM 
	oshkosh_tbl o
WHERE
	temperature <= -10 AND
	temperature != -9999

UNION

SELECT
	'hot' as temp,
	COUNT(DISTINCT concat_ws('/', CAST(month AS STRING), CAST(day AS STRING), CAST(year AS STRING))) as num_days
FROM 
	oshkosh_tbl o
WHERE
	temperature >= 95 AND
	temperature != -9999