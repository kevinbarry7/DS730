DROP TABLE IF EXISTS master;
CREATE EXTERNAL TABLE IF NOT EXISTS master(id STRING, byear INT,
bmonth INT, bday INT, bcountry STRING, bstate STRING, bcity
STRING, dyear INT, dmonth INT, dday INT, dcountry STRING, dstate
STRING, dcity STRING, fname STRING, lname STRING, name STRING,
weight INT, height INT, bats STRING, throws STRING, debut
STRING, finalgame STRING, retro STRING, bbref STRING) ROW FORMAT
DELIMITED FIELDS TERMINATED BY ',' LOCATION
'/user/maria_dev/hivetest/master';

SELECT
	month_day
FROM
	(
	SELECT
		month_day,
		count_bdays
	FROM
		(
		SELECT
			concat_ws('/', CAST(bmonth as STRING), CAST(bday AS STRING)) as month_day,
			count(id) as count_bdays
		FROM
			master
		WHERE
			bday IS NOT NULL AND bmonth IS NOT NULL
		GROUP BY
			concat_ws('/', CAST(bmonth as STRING), CAST(bday AS STRING))
		) sub
	ORDER BY
		count_bdays DESC
	) sub2
LIMIT 3