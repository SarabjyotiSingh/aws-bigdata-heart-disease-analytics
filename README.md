# AWS Big Data Heart Disease Analytics Pipeline

![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20Glue%20%7C%20Athena-orange)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Project Overview

This project demonstrates an end-to-end Big Data analytics pipeline built on AWS cloud infrastructure for analyzing the Heart Disease UCI dataset. It showcases modern data engineering practices including data ingestion, ETL (Extract, Transform, Load) processing, and serverless querying capabilities.

### Key Features
- ☁️ **Cloud-Native Architecture**: Fully serverless AWS infrastructure
- 🔄 **Automated ETL Pipeline**: AWS Glue for data transformation
- 📊 **Scalable Storage**: Amazon S3 for raw and processed data
- 🔍 **SQL Analytics**: Amazon Athena for interactive querying
- 🎯 **Real-World Dataset**: UCI Heart Disease dataset analysis

---
```
---

## 📁 Repository Structure

```
aws-bigdata-heart-disease-analytics/
│
├── data/
│   ├── raw/                    # Original CSV dataset
│   │   └── heart.csv
│   └── processed/              # Transformed data (Parquet/optimized)
│
├── scripts/
│   ├── glue_etl_job.py        # AWS Glue PySpark ETL script


![AWS Big Data Pipeline Architecture](docs/Untitled diagram-2025-11-18-034613.png)

### Data Pipeline Flow

Our Big Data pipeline follows these key stages:

1. **📤 Data Ingestion**
   - Upload `heart.csv` dataset to S3 Raw Bucket
   - Source: UCI Heart Disease dataset (303 records, 14 features)

2. **🔍 Schema Detection**
   - AWS Glue Crawler scans S3 raw data
   - Automatically detects schema and creates table in Data Catalog
   - Metadata stored for downstream processing

3. **⚙️ ETL Processing** 
   - AWS Glue ETL Job (PySpark) performs:
     - Data quality checks (nulls, duplicates)
     - Data cleaning and deduplication
     - Feature engineering (age_group, sex_label, risk_category)
     - Data validation and statistics

4. **💾 Processed Storage**
   - Transformed data written to S3 Processed Bucket
   - Format: Parquet (optimized for analytics)
   - Partitioned by: `age_group` and `sex_label`

5. **📊 SQL Analytics**
   - Amazon Athena for serverless SQL queries
   - Interactive data exploration
   - Generate insights and aggregations

6. **📈 Visualization**
   - Power BI connects to Athena
   - Interactive dashboards and reports
   - Visual analytics for stakeholders

### Key AWS Services

| Service | Purpose | Configuration |
|---------|---------|---------------|
| **Amazon S3** | Object storage for raw and processed data | 2 buckets (raw + processed) |
| **AWS Glue Crawler** | Automatic schema detection | Scans S3, populates Data Catalog |
| **AWS Glue Data Catalog** | Centralized metadata repository | Stores table schemas |
| **AWS Glue ETL** | Serverless data transformation | PySpark job with 6 processing steps |
| **Amazon Athena** | Serverless SQL query engine | Queries Parquet data in S3 |
| **Power BI** | Business intelligence visualization | Connects via Athena connector |│   ├── create_glue_crawler.py # Automated crawler setup
│   └── athena_queries.sql     # Sample Athena SQL queries
│
├── config/
│   ├── aws_config.json        # AWS service configurations
│   └── glue_job_config.json   # Glue job parameters
│
├── docs/
│   ├── setup_guide.md         # Step-by-step setup instructions
│   ├── architecture.md        # Detailed architecture documentation
│   └── troubleshooting.md     # Common issues and solutions
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

1. **AWS Account** with appropriate permissions:
   - S3 (Full Access)
   - Glue (Full Access)
   - Athena (Full Access)
   - IAM (User/Role creation)

2. **AWS CLI** installed and configured:
   ```bash
   aws configure
   ```

3. **Python 3.8+** (for local development/testing)

4. **Dataset**: Heart Disease UCI dataset (included in `/data/raw/`)

### Installation Steps

#### Step 1: Clone the Repository
```bash
git clone https://github.com/SarabjyotiSingh/aws-bigdata-heart-disease-analytics.git
cd aws-bigdata-heart-disease-analytics
```

#### Step 2: Create S3 Buckets
```bash
# Create bucket for raw data
aws s3 mb s3://your-bucket-name-raw-data

# Create bucket for processed data
aws s3 mb s3://your-bucket-name-processed-data
```

#### Step 3: Upload Dataset to S3
```bash
aws s3 cp data/raw/heart.csv s3://your-bucket-name-raw-data/heart-disease/
```

#### Step 4: Set Up IAM Role for Glue
Create an IAM role with the following policies:
- `AWSGlueServiceRole`
- `AmazonS3FullAccess`

#### Step 5: Create Glue Database
```bash
aws glue create-database --database-input '{"Name": "heart_disease_db"}'
```

#### Step 6: Create and Run Glue Crawler
```bash
# Using AWS Console or CLI
aws glue create-crawler --name heart-disease-crawler \
  --role YourGlueServiceRole \
  --database-name heart_disease_db \
  --targets '{"S3Targets": [{"Path": "s3://your-bucket-name-raw-data/heart-disease/"}]}'

# Start the crawler
aws glue start-crawler --name heart-disease-crawler
```

#### Step 7: Create Glue ETL Job
Upload the `scripts/glue_etl_job.py` to S3 and create a Glue job:
```bash
aws glue create-job --name heart-disease-etl \
  --role YourGlueServiceRole \
  --command '{"Name": "glueetl", "ScriptLocation": "s3://your-scripts-bucket/glue_etl_job.py"}'
```

#### Step 8: Query with Athena
Open Amazon Athena console and run queries from `scripts/athena_queries.sql`

---

## 📊 Dataset Information

**Source**: [UCI Machine Learning Repository - Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/heart+disease)

**Description**: This dataset contains 303 patient records with 14 attributes related to heart disease diagnosis.

### Features:
- `age`: Age in years
- `sex`: Gender (1 = male, 0 = female)
- `cp`: Chest pain type (0-3)
- `trestbps`: Resting blood pressure (mm Hg)
- `chol`: Serum cholesterol (mg/dl)
- `fbs`: Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)
- `restecg`: Resting ECG results (0-2)
- `thalach`: Maximum heart rate achieved
- `exang`: Exercise induced angina (1 = yes, 0 = no)
- `oldpeak`: ST depression induced by exercise
- `slope`: Slope of peak exercise ST segment
- `ca`: Number of major vessels colored by fluoroscopy (0-3)
- `thal`: Thalassemia (1 = normal, 2 = fixed defect, 3 = reversible defect)
- `target`: Heart disease presence (1 = disease, 0 = no disease)

---

## 🔧 ETL Pipeline Details

### Data Transformation Steps:

1. **Data Ingestion**:
   - Load CSV from S3 raw bucket
   - Schema validation

2. **Data Cleaning**:
   - Handle missing values
   - Remove duplicates
   - Data type conversions

3. **Data Transformation**:
   - Feature engineering
   - Categorical encoding
   - Normalization

4. **Data Loading**:
   - Write to S3 in Parquet format
   - Partition by relevant columns
   - Update Glue Data Catalog

---

## 📈 Sample Athena Queries

### Query 1: Count of Patients by Age Group
```sql
SELECT 
    CASE 
        WHEN age < 40 THEN '20-39'
        WHEN age BETWEEN 40 AND 49 THEN '40-49'
        WHEN age BETWEEN 50 AND 59 THEN '50-59'
        ELSE '60+'
    END AS age_group,
    COUNT(*) as patient_count
FROM heart_disease_db.heart_disease_table
GROUP BY 1
ORDER BY 1;
```

### Query 2: Heart Disease Prevalence by Gender
```sql
SELECT 
    CASE WHEN sex = 1 THEN 'Male' ELSE 'Female' END AS gender,
    SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) as with_disease,
    SUM(CASE WHEN target = 0 THEN 1 ELSE 0 END) as without_disease,
    ROUND(AVG(target) * 100, 2) as disease_percentage
FROM heart_disease_db.heart_disease_table
GROUP BY sex;
```

---

## 💰 Cost Estimation

**AWS Free Tier Usage**:
- S3: 5GB storage (first 12 months)
- Glue: 1 million objects stored in Data Catalog (always free)
- Athena: 5GB of data scanned per month (first 2 months)

**Expected Monthly Cost** (after free tier):
- S3 Storage: ~$0.10 (for <10GB)
- Glue Crawler: ~$0.44/hour (runs ~5 minutes = $0.04)
- Glue ETL Job: ~$0.44/hour (runs ~10 minutes = $0.07)
- Athena Queries: ~$5 per TB scanned (~$0.01 for this dataset)

**Total Estimated**: **< $1/month** for learning purposes

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|--------|
| **Amazon S3** | Scalable object storage for raw and processed data |
| **AWS Glue** | Serverless ETL service for data transformation |
| **AWS Glue Crawler** | Automatic schema discovery and cataloging |
| **AWS Glue Data Catalog** | Metadata repository |
| **Amazon Athena** | Serverless interactive query service |
| **Python/PySpark** | ETL scripting language |
| **SQL** | Data querying and analysis |

---

## 📚 Learning Outcomes

By completing this project, you will learn:

✅ How to build scalable data pipelines on AWS
✅ ETL best practices using AWS Glue
✅ Data cataloging and schema management
✅ Serverless architecture patterns
✅ Cost-effective big data processing
✅ SQL analytics on cloud data lakes
✅ IAM role and policy management

---

## 🐛 Troubleshooting

### Common Issues:

**Issue 1**: Glue Crawler fails to detect schema
- **Solution**: Check S3 bucket permissions and ensure CSV format is correct

**Issue 2**: Athena query fails with "HIVE_CANNOT_OPEN_SPLIT"
- **Solution**: Verify S3 path in Glue table definition

**Issue 3**: IAM permission errors
- **Solution**: Ensure Glue role has S3 read/write permissions

For more details, see [docs/troubleshooting.md](docs/troubleshooting.md)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Sarabjyoti Singh**
- GitHub: [@SarabjyotiSingh](https://github.com/SarabjyotiSingh)
- University: Chandigarh University (CUCHD)

---

## 🙏 Acknowledgments

- UCI Machine Learning Repository for the Heart Disease dataset
- AWS Documentation and tutorials
- Open-source community

---

## 📞 Support

If you have any questions or need help with the project:
- Open an issue on GitHub
- Check the [docs/](docs/) folder for detailed guides

---

## 🔮 Future Enhancements

- [ ] Add AWS Lambda for real-time processing
- [ ] Implement AWS Step Functions for workflow orchestration
- [ ] Create visualization dashboard using Amazon QuickSight
- [ ] Add machine learning model training using AWS SageMaker
- [ ] Implement data quality checks using AWS Glue DataBrew
- [ ] Add CI/CD pipeline using AWS CodePipeline

---

⭐ **If you found this project helpful, please give it a star!** ⭐
