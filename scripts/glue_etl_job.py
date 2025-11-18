import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col, when, isnan, count

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_OUTPUT_PATH', 'DATABASE_NAME', 'TABLE_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

print("========================================")
print("Starting Heart Disease ETL Job")
print("========================================")

# Step 1: Read data from Glue Data Catalog
print("\n[STEP 1] Reading data from Glue Data Catalog...")
datasource = glueContext.create_dynamic_frame.from_catalog(
    database=args['DATABASE_NAME'],
    table_name=args['TABLE_NAME'],
    transformation_ctx="datasource"
)

print(f"Total records loaded: {datasource.count()}")

# Convert to Spark DataFrame for easier manipulation
df = datasource.toDF()

print("\nSchema of input data:")
df.printSchema()

# Step 2: Data Quality Checks
print("\n[STEP 2] Performing data quality checks...")

# Check for null values
print("\nNull value counts:")
df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()

# Check for duplicate rows
original_count = df.count()
duplicate_count = original_count - df.dropDuplicates().count()
print(f"\nDuplicate rows found: {duplicate_count}")

# Step 3: Data Cleaning
print("\n[STEP 3] Cleaning data...")

# Remove duplicates
df_clean = df.dropDuplicates()
print(f"Records after removing duplicates: {df_clean.count()}")

# Handle missing values (if any)
# For this dataset, we'll drop rows with any null values
df_clean = df_clean.na.drop()
print(f"Records after removing nulls: {df_clean.count()}")

# Step 4: Data Transformation
print("\n[STEP 4] Transforming data...")

# Create age groups for better analysis
df_transformed = df_clean.withColumn(
    "age_group",
    when(col("age") < 40, "20-39")
    .when((col("age") >= 40) & (col("age") < 50), "40-49")
    .when((col("age") >= 50) & (col("age") < 60), "50-59")
    .otherwise("60+")
)

# Add descriptive labels for binary columns
df_transformed = df_transformed.withColumn(
    "sex_label",
    when(col("sex") == 1, "Male").otherwise("Female")
)

df_transformed = df_transformed.withColumn(
    "target_label",
    when(col("target") == 1, "Disease").otherwise("No Disease")
)

# Add risk category based on multiple factors
df_transformed = df_transformed.withColumn(
    "risk_category",
    when(
        (col("target") == 1) & (col("age") >= 60) & (col("chol") > 240),
        "High Risk"
    ).when(
        (col("target") == 1) & ((col("age") >= 50) | (col("chol") > 200)),
        "Medium Risk"
    ).otherwise("Low Risk")
)

print("\nTransformed schema:")
df_transformed.printSchema()

print("\nSample transformed data:")
df_transformed.show(5, truncate=False)

# Step 5: Data Validation
print("\n[STEP 5] Validating transformed data...")

# Verify record count
final_count = df_transformed.count()
print(f"Final record count: {final_count}")

# Check value distributions
print("\nTarget distribution:")
df_transformed.groupBy("target_label").count().show()

print("\nAge group distribution:")
df_transformed.groupBy("age_group").count().orderBy("age_group").show()

print("\nRisk category distribution:")
df_transformed.groupBy("risk_category").count().show()

# Step 6: Write processed data to S3
print("\n[STEP 6] Writing processed data to S3...")

# Convert back to DynamicFrame
output_dynamic_frame = DynamicFrame.fromDF(df_transformed, glueContext, "output_dynamic_frame")

# Write to S3 in Parquet format with partitioning
glueContext.write_dynamic_frame.from_options(
    frame=output_dynamic_frame,
    connection_type="s3",
    connection_options={
        "path": args['S3_OUTPUT_PATH'],
        "partitionKeys": ["age_group", "sex_label"]
    },
    format="parquet",
    transformation_ctx="output"
)

print("\n========================================")
print("ETL Job completed successfully!")
print(f"Processed {final_count} records")
print(f"Output location: {args['S3_OUTPUT_PATH']}")
print("========================================")

job.commit()
