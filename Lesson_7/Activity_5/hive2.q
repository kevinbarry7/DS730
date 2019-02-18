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
		id as id,
		max_count_id as max_count_id
	FROM
		(
		SELECT
			sub.id as id,
			max(sub.count_id) as max_count_id
		FROM
			(
			SELECT
				year,
				id,
				COUNT(id) as count_id
			FROM
				batting
			GROUP BY
				year,
				id
			) sub
		GROUP BY
			sub.id
		) sub2
	ORDER BY
		max_count_id DESC
	) sub3
LIMIT 1