DROP TABLE IF EXISTS oshkosh_tbl;
CREATE EXTERNAL TABLE IF NOT EXISTS oshkosh_tbl(year INT, month INT,
day INT, time STRING, temperature FLOAT, dewpoint FLOAT, humidity INT, sea_level_pressure FLOAT, visibility FLOAT, wind_direction STRING, wind_speed FLOAT, gust_speed FLOAT, precip FLOAT, events STRING, conditions STRING, wind_degrees INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/final/Oshkosh/';
DROP TABLE IF EXISTS iowacity_tbl;
CREATE EXTERNAL TABLE IF NOT EXISTS iowacity_tbl(year INT, month INT,
day INT, time STRING, temperature FLOAT, dewpoint FLOAT, humidity INT, sea_level_pressure FLOAT, visibility FLOAT, wind_direction STRING, wind_speed FLOAT, gust_speed FLOAT, precip FLOAT, events STRING, conditions STRING, wind_degrees INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/final/IowaCity/';


SELECT
	oshkosh.season as season,
	round(oshkosh.avg_temp - iowacity.avg_temp, 2) as avg_temp_diff
FROM
	(
	SELECT
		CASE 
			WHEN month IN (12, 1, 2) THEN 'Winter'
			WHEN month IN (3, 4, 5) THEN 'Spring'
			WHEN month IN (6, 7, 8) THEN 'Summer'
			WHEN month IN (9, 10, 11) THEN 'Fall'
			else 'NA'
		END AS season,
		sum(temperature)/count(temperature) as avg_temp
	FROM 
		oshkosh_tbl o
	WHERE
		temperature IS NOT NULL AND
		temperature != -9999
	GROUP BY
		CASE 
			WHEN month IN (12, 1, 2) THEN 'Winter'
			WHEN month IN (3, 4, 5) THEN 'Spring'
			WHEN month IN (6, 7, 8) THEN 'Summer'
			WHEN month IN (9, 10, 11) THEN 'Fall'
			else 'NA'
		END
	) oshkosh
JOIN
	(
	SELECT
		CASE 
			WHEN month IN (12, 1, 2) THEN 'Winter'
			WHEN month IN (3, 4, 5) THEN 'Spring'
			WHEN month IN (6, 7, 8) THEN 'Summer'
			WHEN month IN (9, 10, 11) THEN 'Fall'
			else 'NA'
		END AS season,
		sum(temperature)/count(temperature) as avg_temp
	FROM 
		iowacity_tbl i
	WHERE
		temperature IS NOT NULL AND
		temperature != -9999
	GROUP BY
		CASE 
			WHEN month IN (12, 1, 2) THEN 'Winter'
			WHEN month IN (3, 4, 5) THEN 'Spring'
			WHEN month IN (6, 7, 8) THEN 'Summer'
			WHEN month IN (9, 10, 11) THEN 'Fall'
			else 'NA'
		END
	) iowacity
ON
	oshkosh.season = iowacity.season