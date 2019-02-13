fielding_data = LOAD 'hdfs:/user/maria_dev/pigtest/Fielding.csv' using PigStorage(',');
fielding_table = FOREACH fielding_data GENERATE $0 AS id, $1 AS year, $2 AS team, $10 AS errors;
fielding_table = FILTER fielding_table BY year > 1950 AND errors IS NOT NULL;
ft_group = GROUP fielding_table BY (id, team);
sum_player_errors = FOREACH ft_group GENERATE group, SUM(fielding_table.errors) AS sum_errors;
ordered = ORDER sum_player_errors BY sum_errors DESC;
top_1 = LIMIT ordered 1;
result = FOREACH top_1 GENERATE group;
DUMP result;