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
	weight
FROM
	(
	SELECT
		weight,
		count_weight,
		row_number() over(order by count_weight DESC) as row_num
	FROM
		(
		SELECT
			weight,
			count(weight) count_weight
		FROM
			master
		WHERE
			weight IS NOT NULL
		GROUP BY
			weight
		) sub
	ORDER BY
		count_weight DESC
	) sub2
WHERE
	row_num = 2