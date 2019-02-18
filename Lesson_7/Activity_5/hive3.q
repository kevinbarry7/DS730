DROP TABLE IF EXISTS batting;
CREATE EXTERNAL TABLE IF NOT EXISTS batting(id STRING, year INT,
team STRING, league STRING, games INT, ab INT, runs INT, hits
INT, doubles INT, triples INT, homeruns INT, rbi INT, sb INT, cs
INT, walks INT, strikeouts INT, ibb INT, hbp INT, sh INT, sf
INT, gidp INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION '/user/maria_dev/hivetest/batting';

SELECT
	id
FROM
	(
	SELECT
		id,
		count_id
	FROM
		(
		SELECT
			id,
			SUM(doubles + triples + homeruns) as count_id
		FROM
			batting
		WHERE
			year >= 1980 AND 
			year <= 1989
		GROUP BY
			id
		) sub
	ORDER BY
		count_id DESC
	) sub2
LIMIT 1