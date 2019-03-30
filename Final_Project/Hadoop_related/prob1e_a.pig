oshkosh_data = LOAD 'hdfs:/user/maria_dev/final/Oshkosh/OshkoshWeather.csv' using PigStorage(',');
oshkosh_data = rank oshkosh_data;
oshkosh_data = Filter oshkosh_data by ((int)$0 > 1);
ot_raw = FOREACH oshkosh_data GENERATE ToDate(CONCAT((chararray)$1,'-',(chararray)$2,'-',(chararray)$3, ' ',(chararray)$4), 'yyyy-MM-dd h:m a') as date_time, (float)$5 AS temp;
ot_raw = FILTER ot_raw BY temp IS NOT NULL;
ot = FOREACH oshkosh_data GENERATE ToDate(CONCAT((chararray)$1,'-',(chararray)$2,'-',(chararray)$3, ' ',(chararray)$4), 'yyyy-MM-dd h:m a') as min_dt, AddDuration(ToDate(CONCAT((chararray)$1,'-',(chararray)$2,'-',(chararray)$3, ' ',(chararray)$4), 'yyyy-MM-dd h:m a'), 'P1D') as max_dt, (float)$5 AS temp;
ot = FILTER ot BY temp IS NOT NULL;
ot_grouped = GROUP ot BY min_dt;

period_temps = FOREACH ot_grouped {
	filtered_data = FILTER ot BY min_dt <= ot_grouped.group AND max_dt >= ot_grouped.group;
	min_temp = MIN(filtered_data.temp);
	max_temp = MAX(filtered_data.temp);
	GENERATE filtered_data, min_temp, max_temp;
	};
r = LIMIT period_temps 15;
DUMP r;

