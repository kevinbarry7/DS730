sql("SET spark.sql.orc.enabled=true")

val data = spark.read.format("org.apache.spark.sql.execution.datasources.orc").load("s3a://cornell-eas-data-lake/v1/ncep/ndfd-ndgd/")

data.createOrReplaceTempView("ccd")

val updated_view = spark.sqlContext.sql("""
	SELECT
		concat(reference_year, reference_month),
		avg(temp)
	FROM
		ccd
	WHERE
		reference_month = 6 or
		reference_month = 12 and
		reference_year >= 2019 and
		element = 'temp'
	GROUP BY
		concat(reference_year, reference_month)
	""")