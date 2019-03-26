DROP TABLE IF EXISTS oshkosh_tbl;
CREATE EXTERNAL TABLE IF NOT EXISTS oshkosh_tbl(year STRING, month STRING,
day STRING, time STRING, temperature FLOAT, dewpoint FLOAT, humidity INT, sea_level_pressure FLOAT, visibility FLOAT, wind_direction STRING, wind_speed FLOAT, gust_speed FLOAT, precip FLOAT, events STRING, conditions STRING, wind_degrees INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/final/Oshkosh/';

SELECT
	hour_d
FROM
	(
	SELECT
		hour_d,
		occurrences
	FROM
		(
		SELECT
			hour_d,
			count(hour_d) as occurrences
		FROM
			(
			SELECT
				date_d,
				hour_d,
				rank() over(partition by date_d order by avg_temp) as ranking
			FROM
				(
				SELECT
					to_date(concat_ws('-', year, month, day)) as date_d,
					concat(split(time, ":")[0],split(time," ")[1]) as hour_d,
					avg(temperature) as avg_temp
				FROM 
					oshkosh_tbl o
				WHERE
					temperature IS NOT NULL AND
					temperature != -9999
				GROUP BY
					to_date(concat_ws('-', year, month, day)),
					concat(split(time, ":")[0],split(time," ")[1])
				) sub
			) sub2
		WHERE
			ranking == 1
		GROUP BY
			hour_d
		) sub3
	ORDER BY
		occurrences DESC
	LIMIT 1
	) sub4