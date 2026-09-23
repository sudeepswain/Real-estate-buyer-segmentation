# Real Estate Buyer Segmentation & Investment Profiling

## Project Overview

This project develops a machine learning based buyer segmentation and investment profiling system for real estate market intelligence.

The objective is to identify buyer segments based on demographic characteristics, acquisition behavior, financing behavior, property purchasing activity, spending patterns, and geographic information.

## Business Objectives

- Understand different types of real estate buyers.
- Analyze investment versus personal-use purchasing behavior.
- Identify geographic differences in buyer segments.
- Analyze financing and loan behavior.
- Understand property purchasing and spending patterns.
- Create buyer profiles using machine learning.
- Provide an interactive dashboard for business analysis.

## Machine Learning Methodology

### Data Cleaning

- Missing-value checks
- Duplicate checks
- Categorical data preparation
- Data type conversion
- Property transaction aggregation at buyer level

### Feature Engineering

- Age
- Satisfaction score
- Total properties purchased
- Total spending
- Average property price
- Maximum property price
- Total property area
- Average property area
- Average spending per property
- Client type
- Gender
- Country
- Region
- Acquisition purpose
- Loan application
- Referral channel

### Feature Preprocessing

Numerical features were standardized using StandardScaler.

Categorical features were transformed using OneHotEncoder.

### Clustering

- K-Means Clustering
- Hierarchical Clustering
- Elbow Method
- Silhouette Score

The final K-Means model used 3 clusters.

### Cluster Validation

K-Means silhouette score: approximately 0.217

Hierarchical clustering silhouette score: approximately 0.191

The relatively modest silhouette scores indicate that the clusters should be interpreted as behavioral profiles rather than completely distinct populations.

## Buyer Segments

### High-Activity Investment-Oriented Buyers

- Smallest segment
- Highest purchasing activity
- Highest average total spending
- Higher investment-oriented share
- Higher average age

### Mainstream Lower-Value Buyers

- Largest segment
- Lower average property price
- Lower average total spending
- Moderate purchasing activity

### Higher-Value Property Buyers

- Higher average property price
- Larger average property area
- Higher total spending than the mainstream segment
- Similar property purchasing activity to the mainstream segment

## Key Findings

- The mainstream segment represents the largest share of buyers.
- Higher-value property buyers represent another large portion of the buyer base.
- The high-activity investment-oriented segment is comparatively small.
- The United States represents the majority of buyers in the dataset.
- Investment behavior differs across clusters.
- Loan usage varies across segments but is not the primary segmentation factor.
- Corporate buyers represent a relatively small share of each segment.

## Business Applications

- Targeted communication strategies for different buyer profiles.
- Portfolio-oriented recommendations for highly active buyers.
- Affordability and financing information for mainstream buyers.
- Higher-value property recommendations for higher-value buyers.
- Combining buyer segment with acquisition purpose for targeted analysis.
- Geographic analysis of buyer composition.

## Project Structure

real-estate-buyer-segmentation/
├── data/
│   └── buyer_segments_public.csv
├── notebooks/
│   └── buyer_segmentation.ipynb
├── outputs/
│   └── segment_profile.csv
├── app.py
├── requirements.txt
├── .gitignore
└── README.md

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Streamlit
- Google Colab
- GitHub

## Project Status

### Completed

- Data preparation
- Feature engineering
- Feature preprocessing
- K-Means clustering
- Hierarchical clustering
- Cluster validation
- Segment profiling
- Exploratory analysis
- Public-safe dataset preparation

### In Progress

- Interactive Streamlit dashboard
- Dashboard deployment

## Data Privacy

The public repository uses a sanitized buyer dataset and does not include direct personal fields such as first name, last name, or date of birth.

The original raw datasets are intentionally excluded from the public repository.