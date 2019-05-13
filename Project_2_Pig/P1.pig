batters_data = LOAD 'hdfs:/user/maria_dev/pigtest/Batting.csv' using PigStorage(',');
master_data = LOAD 'hdfs:/user/maria_dev/pigtest/Master.csv' using PigStorage(',');
player_table = FOREACH batters_data GENERATE $0 AS id, $11 AS rbi;
master_table = FOREACH master_data GENERATE $0 AS id, $6 AS birthcity;
joined_data = JOIN player_table BY id, master_table BY id;
joined_data2 = FOREACH joined_data GENERATE $0 AS id, $3 AS birthcity, $1 AS rbi;
filtered_joined_data = FILTER joined_data2 BY rbi > 0;
joined_grouped = GROUP filtered_joined_data BY id;
player_sum_rbi =
    FOREACH joined_grouped {
        b = filtered_joined_data.birthcity;
        s = DISTINCT b;
        GENERATE group, FLATTEN(s), SUM(filtered_joined_data.rbi) AS sum_rbi;
    };
max_rbi_grouped = GROUP player_sum_rbi ALL;
total_max_rbi = FOREACH max_rbi_grouped GENERATE MAX(player_sum_rbi.sum_rbi) AS max_rbi_hits;
filter_player = FILTER player_sum_rbi BY sum_rbi == total_max_rbi.max_rbi_hits;
birth_city = FOREACH filter_player GENERATE birthcity;
limit_data = LIMIT birth_city 4;
DUMP limit_data;