from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, trim

spark = SparkSession.builder \
    .appName("UniversityKnowledgeAssistant") \
    .getOrCreate()

input_file = "data/silver/andhra_university_cse_syllabus_clean.txt"
output_path = "data/gold/syllabus_processed"

df = spark.read.text(input_file)

df = df.withColumn("text", trim(col("value")))

df = df.filter(length(col("text")) > 20)

df = df.select("text")

df.write.mode("overwrite").parquet(output_path)

print("PySpark processing completed!")
print(f"Saved to: {output_path}")

spark.stop()