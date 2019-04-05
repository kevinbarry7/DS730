import sqlContext.implicits._
import org.apache.spark.sql.expressions.Window
spark.conf.set("spark.sql.session.timeZone", "UTC")

val oshkosh_weather = spark.read.format("csv").option("header", true).option("inferSchema", true).load("/user/maria_dev/final/Oshkosh/OshkoshWeather.csv")

oshkosh_weather.createOrReplaceTempView("okw")

// val updated_view = spark.sqlContext.sql("SELECT to_timestamp(CONCAT(Year,'-',Month,'-',Day,' ',TimeCST), 'yyyy-MM-dd h:m a') as date_time, to_timestamp(CONCAT(Year,'-',Month,'-',Day,' ',TimeCST), 'yyyy-MM-dd h:m a') + INTERVAL 24 HOURS as dt_24, TemperatureF as temp FROM okw LIMIT 500")

// val updated_view = spark.sqlContext.sql("SELECT to_date(CONCAT(Year,'-',Month,'-',Day), 'yyyy-MM-dd') as dt, date_format(to_timestamp(TimeCST, 'h:m a'), 'h:m a') as time, TemperatureF as temp FROM okw LIMIT 3")

val updated_view = spark.sqlContext.sql("SELECT to_timestamp(CONCAT(Year,'-',Month,'-',Day,' ',TimeCST), 'yyyy-MM-dd h:m a') as date_time, TemperatureF as temp FROM okw LIMIT 500")

val results = updated_view.groupBy(window($"date_time", "24 hours")).agg(min("temp") as "min_temp")
def printWindow(windowDF:DataFrame, aggCol:String) ={
    windowDF.sort("window.start").
    select("window.start","window.end",s"$aggCol").
    show(truncate = false)
 }

printWindow(results,"min_temp")

