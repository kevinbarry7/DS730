master_data = LOAD 'hdfs:/user/maria_dev/pigtest/Master.csv' using PigStorage(',');
master_table = FOREACH master_data GENERATE $0 AS id, $17 AS height, CONCAT($13,' ',$14) AS name;
master_table = FILTER master_table BY height IS NOT NULL;
grouped_heights = GROUP master_table BY height;
count_table = FOREACH grouped_heights GENERATE group AS height, master_table.name AS name, COUNT(master_table.id) AS num_heights;
filtered_table = FILTER count_table BY num_heights == 1 AND height != 'height';
result = FOREACH filtered_table GENERATE name;
DUMP result;