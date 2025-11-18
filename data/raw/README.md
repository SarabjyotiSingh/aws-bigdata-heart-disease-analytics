# Raw Data

This directory contains the original, unprocessed datasets.

## Heart Disease Dataset

**Filename**: `heart.csv`

**Source**: [UCI Machine Learning Repository - Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/heart+disease)

### How to Add Your Dataset

1. Download the Heart Disease UCI dataset from Kaggle or UCI Repository
2. Save it as `heart.csv` in this directory
3. Upload to this folder using one of these methods:
   - GitHub web interface: Click "Add file" > "Upload files"
   - Git command line:
     ```bash
     git add data/raw/heart.csv
     git commit -m "Add heart disease dataset"
     git push
     ```
   - Or upload directly to S3:
     ```bash
     aws s3 cp heart.csv s3://your-bucket-name/raw-data/heart-disease/
     ```

### Dataset Information

- **Format**: CSV (Comma-separated values)
- **Size**: ~15 KB
- **Rows**: 303 patient records
- **Columns**: 14 attributes

### Column Descriptions

| Column | Description | Type |
|--------|-------------|------|
| age | Age in years | Integer |
| sex | Gender (1=male, 0=female) | Binary |
| cp | Chest pain type (0-3) | Integer |
| trestbps | Resting blood pressure (mm Hg) | Integer |
| chol | Serum cholesterol (mg/dl) | Integer |
| fbs | Fasting blood sugar > 120 mg/dl | Binary |
| restecg | Resting ECG results (0-2) | Integer |
| thalach | Maximum heart rate achieved | Integer |
| exang | Exercise induced angina | Binary |
| oldpeak | ST depression | Float |
| slope | Slope of peak exercise ST segment | Integer |
| ca | Number of major vessels (0-3) | Integer |
| thal | Thalassemia (1-3) | Integer |
| target | Heart disease (1=yes, 0=no) | Binary |

### Important Notes

- **Do not commit large datasets (>100MB)** to GitHub
- For large files, use Git LFS or store them in S3 only
- This dataset is small enough (<1MB) to be stored in GitHub
- Always verify data integrity after upload
