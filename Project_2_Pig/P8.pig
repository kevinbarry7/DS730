batters_data = LOAD 'hdfs:/user/maria_dev/pigtest/Batting.csv' using PigStorage(',');
master_data = LOAD 'hdfs:/user/maria_dev/pigtest/Master.csv' using PigStorage(',');
batters_table = FOREACH batters_data GENERATE $0 AS id, (int)$5 AS AB, (int)$7 AS H;
batters_table = FILTER batters_table BY AB IS NOT NULL AND H IS NOT NULL;
masters_table = FOREACH master_data GENERATE $0 AS id, $5 AS birthstate, $2  AS birthmonth;
masters_table = FILTER masters_table BY birthstate IS NOT NULL AND birthmonth IS NOT NULL;
joined_tables = JOIN masters_table BY id, batters_table BY id;
joined_tables_exp = FOREACH joined_tables GENERATE batters_table::id AS id, birthmonth, birthstate, AB, H AS H;
grouped_tables = GROUP joined_tables_exp BY (birthmonth, birthstate);
summary = FOREACH grouped_tables {
		AB = SUM(joined_tables_exp.AB);
		H = SUM(joined_tables_exp.H);
        id = joined_tables_exp.id;
        distinct_id = DISTINCT id;
        GENERATE group AS month_state, COUNT(distinct_id) AS count, AB AS AB, H AS H, (float)H/(float)AB AS calc;
    };
filtered = FILTER summary BY count >= 10 AND AB > 1500;
ordered = ORDER filtered BY calc ASC;
output_combo = FOREACH ordered GENERATE month_state;
top_1 = LIMIT output_combo 1;
DUMP top_1;