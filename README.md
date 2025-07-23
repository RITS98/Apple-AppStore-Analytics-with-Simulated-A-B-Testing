# Apple AppStore Analytics with Simulated A/B Testing

## 📱 Project Overview

This project provides comprehensive analytics and insights into the Apple iOS App Store ecosystem. It analyzes app characteristics, user ratings, pricing strategies, genre distributions, and other key metrics to understand the mobile app market landscape. Additionally, it includes an advanced A/B testing simulation component that generates realistic user interaction data for app store optimization experiments.

Some diagrams of what to come

<img width="1678" height="832" alt="image" src="https://github.com/user-attachments/assets/cfb80c63-ac0f-43d9-9d54-54a795e37a2f" />

<img width="1683" height="847" alt="image" src="https://github.com/user-attachments/assets/25665597-6217-49a4-bd42-3da6a4f216b9" />


## 🎯 Project Objectives

The project aims to answer several key business questions:

### Original App Store Analysis:
1. **Price Distribution Analysis**: How are paid apps priced across different categories?
2. **Free vs Paid Apps**: What's the distribution and performance comparison between free and paid applications?
3. **App Quality Assessment**: Are paid apps generally better rated than free apps?
4. **Size-Price Correlation**: Does app size correlate with pricing?
5. **Genre Analysis**: How are apps distributed across different categories and what are the most popular genres?
6. **Language Support**: Which apps support multiple languages and how does this impact their success?
7. **Device Support**: How does device compatibility affect app popularity?

### A/B Testing Analysis:
8. **Conversion Rate Optimization**: Which app store elements drive higher download rates?
9. **User Experience Testing**: How do different UI elements affect user engagement?
10. **Demographic Segmentation**: Which user segments respond best to different variants?
11. **Geographic Performance**: How do test results vary across different countries?
12. **Statistical Significance**: Which test results are statistically reliable?

## 📊 Dataset Description

### Primary Dataset: `AppleStore.csv` (7,197 records)

The main dataset contains the following key features:

| Field | Description |
|-------|-------------|
| `id` | Unique App ID |
| `track_name` | Application Name |
| `size_bytes` | App Size in Bytes (converted to MB during analysis) |
| `currency` | Currency Type (USD) |
| `price` | App Price |
| `rating_count_tot` | Total User Rating Count (all versions) |
| `rating_count_ver` | User Rating Count (current version) |
| `user_rating` | Average User Rating (all versions) |
| `user_rating_ver` | Average User Rating (current version) |
| `ver` | Latest Version Code |
| `cont_rating` | Content Rating (4+, 12+, etc.) |
| `prime_genre` | Primary Genre Category |
| `sup_devices.num` | Number of Supporting Devices |
| `ipadSc_urls.num` | Number of Screenshots |
| `lang.num` | Number of Supported Languages |
| `vpp_lic` | VPP Device Based Licensing |

### Secondary Dataset: `appleStore_description.csv`

Contains detailed app descriptions and metadata that gets merged with the primary dataset for enhanced analysis.

### A/B Testing Datasets (Generated)

#### 1. `ab_test_sessions` (15,000 records)
Main A/B testing data table containing:

| Field | Description |
|-------|-------------|
| `session_id` | Unique session identifier |
| `user_id` | Unique user identifier |
| `session_date` | Date and time of session |
| `app_name` | Application name being tested |
| `app_genre` | App category (Games, Entertainment, etc.) |
| `age_group` | User age group (18-24, 25-34, 35-44, 45-54, 55+) |
| `device_type` | Device used (iPhone, iPad, Apple Watch, Mac) |
| `country` | User's country code (US, UK, CA, AU, etc.) |
| `icon_design_variant` | Icon design test variant (control, variant_a, variant_b) |
| `description_variant` | Description length test variant (control, variant_a) |
| `pricing_variant` | Pricing strategy test variant (control, variant_a, variant_b) |
| `screenshots_variant` | Screenshot count test variant (control, variant_a) |
| `time_spent_seconds` | Time spent on app store page |
| `converted` | Whether user downloaded the app (Boolean) |
| `rating` | User rating if app was downloaded (1.0-5.0) |

#### 2. `ab_test_variants` (10 records)
Test variant definitions and descriptions

#### 3. `ab_test_summary` (10 records)
Pre-aggregated conversion rates and performance metrics by variant

## 🔧 Technical Architecture

### Data Processing Pipeline

```mermaid
graph TD
    A[Raw Data]:::raw --> B[Data Cleaning]:::cleaning
    B --> C[Feature Engineering]:::engineering
    C --> D[Analysis]:::analysis
    D --> E[Visualization]:::visualization
    E --> F[Insights]:::insights
    F --> G[A/B Testing Simulation]:::abtesting

    classDef raw fill:#FF6B6B,stroke:#FF0000,color:#FFF
    classDef cleaning fill:#4ECDC4,stroke:#0D98BA,color:#000
    classDef engineering fill:#FFD166,stroke:#FFA500,color:#000
    classDef analysis fill:#06D6A0,stroke:#0B7A75,color:#000
    classDef visualization fill:#A78AFF,stroke:#6A5ACD,color:#FFF
    classDef insights fill:#FF85A1,stroke:#FF1493,color:#000
    classDef abtesting fill:#84DCC6,stroke:#20B2AA,color:#000
````

### Technology Stack

- **Data Analysis**: Python, Pandas, NumPy
- **Synthetic Data Generation**: Faker library for realistic A/B testing simulation
- **Visualization**: 
  - Plotly (Interactive plots)
  - Matplotlib & Seaborn (Statistical plots)
- **Environment**: Jupyter Notebook
- **Business Intelligence**: Apache Superset
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **A/B Testing**: Custom simulation with statistical significance testing

### Infrastructure Components

1. **Jupyter Notebook Environment**: Main analysis workspace
2. **PostgreSQL Database**: Data storage and querying
3. **Apache Superset**: Business intelligence and dashboard creation
4. **Redis**: Caching layer for Superset
5. **Docker Containers**: Isolated, reproducible environment

## 🚀 Complete Implementation Guide

### Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ (for local development)
- Git

### Step 1: Environment Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "Apple AppStore Analytics"
   ```

2. **Start the containerized environment**:
   ```bash
   docker-compose up -d
   ```

3. **Verify containers are running**:
   ```bash
   docker-compose ps
   ```
   You should see:
   - `postgres_container` (PostgreSQL database)
   - `superset_app` (Apache Superset)
   - `superset_cache` (Redis cache)

### Step 2: Install Python Dependencies

1. **Configure Python environment**:
   ```bash
   # Install required packages
   pip install faker psycopg2-binary pandas numpy
   ```

### Step 3: Generate A/B Testing Data

1. **Run the A/B testing simulation**:
   ```bash
   python scripts/ab_testing_simulation.py
   ```

   This will:
   - Create 3 database tables in PostgreSQL
   - Generate 15,000 realistic user sessions
   - Simulate 4 different A/B tests
   - Calculate conversion rates and statistical metrics

2. **Verify data generation**:
   ```bash
   # Check total sessions generated
   PGPASSWORD=postgres psql -h localhost -p 5001 -U postgres -d analytics_db -c "SELECT COUNT(*) FROM ab_test_sessions;"
   
   # View A/B test results summary
   PGPASSWORD=postgres psql -h localhost -p 5001 -U postgres -d analytics_db -c "SELECT * FROM ab_test_summary ORDER BY test_name, conversion_rate DESC;"
   ```

### Step 4: Access Services

1. **Apache Superset Dashboard**: 
   - URL: http://localhost:8088
   - Username: `admin`
   - Password: `admin`

2. **PostgreSQL Database**:
   - Host: localhost
   - Port: 5001
   - Database: `analytics_db`
   - Username: `postgres`
   - Password: `postgres`

3. **Jupyter Notebook**:
   - Available in `/notebooks/` directory
   - Main analysis: `analysis.ipynb`
   - Superset guide: `ab_testing_superset_guide.ipynb`

### Step 5: Set Up Superset Database Connection

1. **Login to Superset** (http://localhost:8088)

2. **Add Database Connection**:
   - Go to **Settings** → **Database Connections**
   - Click **+ Database**
   - Select **PostgreSQL**
   - Use these connection details:
     ```
     Host: db (internal Docker network name)
     Port: 5432
     Database: analytics_db
     Username: postgres
     Password: postgres
     ```
   - Click **Test Connection**
   - Save the connection

### Step 6: Create A/B Testing Charts in Superset

Open the Jupyter notebook `ab_testing_superset_guide.ipynb` for detailed instructions on creating:

1. **Conversion Rate Comparison Bar Chart**
2. **Daily Conversion Trends Line Chart**
3. **Demographics Heatmap**
4. **Time Spent Analysis Box Plot**
5. **Geographic Performance Map**
6. **App Genre Performance Treemap**
7. **Statistical Significance Table**

### Step 7: Build Interactive Dashboard

1. **Create Dashboard**:
   - Go to **Dashboards** in Superset
   - Click **+ Dashboard**
   - Name it "A/B Testing Analysis Dashboard"

2. **Add Charts**:
   - Add all 7 charts created in Step 6
   - Arrange them in a logical layout

3. **Add Filters**:
   - Date range filter (session_date)
   - App genre filter
   - Country filter
   - Device type filter
   - Age group filter

### Manual Setup (Local Development Alternative)

If you prefer to run without Docker:

1. **Install PostgreSQL locally**
2. **Install Python dependencies**:
   ```bash
   pip install pandas numpy matplotlib seaborn plotly jupyter missingno faker psycopg2-binary
   ```
3. **Update database connection settings** in the simulation script
4. **Launch Jupyter Notebook**:
   ```bash
   jupyter notebook notebooks/analysis.ipynb
   ```

## 📈 Key Insights and Findings

### 1. Genre Distribution
- **Games** dominate the App Store with the highest number of applications
- **Entertainment**, **Education**, and **Photo & Video** follow as popular categories
- Clear market concentration in entertainment-focused applications

### 2. Free vs Paid Apps Analysis
- Significant majority of apps are **free** (approximately 90%+)
- **Games** and **Entertainment** have the highest number of both free and paid applications
- Paid apps show different rating distributions compared to free apps

### 3. App Quality Metrics
- High-rated apps (4.0-5.0 stars) analysis reveals quality patterns
- Popular apps identified through rating count and user rating correlation
- Genre-specific quality trends observed

### 4. Language and Device Support
- Multi-language support varies significantly across apps
- Some applications support 50+ languages
- Device compatibility patterns influence app success

### 5. Feature Engineering Insights
- Created derived metrics:
  - `total_users_rating`: Rating count divided by user rating
  - `total_users_rating_cur`: Current version specific metrics
- Size conversion from bytes to MB for better analysis
- Data quality improvements (handling zero language counts)

## 🔍 Analysis Workflow

### Data Preprocessing
1. **Missing Value Analysis**: Comprehensive check for null values
2. **Data Type Conversions**: Size conversion from bytes to MB
3. **Duplicate Removal**: Ensuring data quality
4. **Data Merging**: Combining main dataset with descriptions

### Exploratory Data Analysis
1. **Genre Distribution Analysis**
2. **Free vs Paid App Comparison**
3. **Rating and Popularity Analysis**
4. **Device Support Analysis**
5. **Language Support Investigation**
6. **Correlation Analysis** (Pearson correlation matrix)

### Advanced Analytics
1. **Feature Engineering**: Creating meaningful derived variables
2. **Popular App Identification**: Multi-criteria ranking
3. **Genre-specific Analysis**: Deep dive into each category
4. **Price-Quality Relationship**: Understanding value propositions

## 📊 Visualization Capabilities

The project includes various interactive visualizations:

- **Bar Charts**: Genre distribution, app counts
- **Pie Charts**: Free vs paid distribution, popular genres
- **Violin Plots**: Rating distributions by genre and app type
- **Correlation Heatmaps**: Feature relationship analysis
- **Treemaps**: Hierarchical data visualization
- **Interactive Plotly Charts**: Dynamic exploration capabilities

## 🛠️ Docker Environment Details

### Services Configuration

- **PostgreSQL Container**: 
  - Port: 5001
  - Includes initialization scripts for Superset setup
  
- **Apache Superset**: 
  - Port: 8088
  - Pre-configured with analytics database connections
  
- **Redis Cache**: 
  - Port: 6379
  - Supports Superset caching layer

### Environment Variables

Configure through `.env` files in the `docker/` directory for:
- Database credentials
- Superset configuration
- Security settings

## 📋 Project Structure

```
Apple AppStore Analytics/
├── README.md                          # This comprehensive documentation
├── docker-compose.yml                # Multi-container orchestration
├── data/                             # Raw datasets
│   ├── AppleStore.csv               # Main app data (7,197 records)
│   └── appleStore_description.csv   # App descriptions
├── notebooks/                        # Analysis notebooks
│   ├── analysis.ipynb              # Original app store analysis
│   └── ab_testing_superset_guide.ipynb # A/B testing & Superset guide
├── scripts/                          # Python scripts
│   ├── ab_testing_simulation.py    # A/B test data generator
│   └── requirements_ab_testing.txt # Dependencies for A/B testing
├── docker/                           # Docker configuration
│   ├── docker-bootstrap.sh         # Superset bootstrap script
│   ├── docker-init.sh              # Initialization script
│   ├── superset_config.py          # Superset configuration
│   └── .env                        # Environment variables
└── postgres/                         # Database setup
    ├── superset_init.sql            # Database initialization
    └── data/                        # PostgreSQL data directory
```

### Generated Database Tables (After Running A/B Testing)

```
PostgreSQL Database: analytics_db
├── Original Tables
│   └── (Tables can be created from CSV data)
└── A/B Testing Tables
    ├── ab_test_sessions (15,000 records)    # Detailed user session data
    ├── ab_test_variants (10 records)        # Test variant definitions  
    └── ab_test_summary (10 records)         # Aggregated test results
```

## 🎓 Learning Outcomes

This project demonstrates:

### Core Data Science Skills
- **Data Science Pipeline**: End-to-end analytics workflow from raw data to insights
- **Data Visualization**: Multiple visualization techniques using Plotly, Matplotlib, and Seaborn
- **Statistical Analysis**: Correlation analysis, hypothesis testing, and A/B testing methodology
- **Feature Engineering**: Creating meaningful derived variables and data transformations

### Advanced Analytics Techniques
- **A/B Testing**: Complete experimental design, data simulation, and statistical significance testing
- **Synthetic Data Generation**: Using Faker to create realistic user interaction datasets
- **Conversion Rate Optimization**: Understanding user behavior patterns and optimization strategies
- **Demographic Segmentation**: Analyzing user behavior across different segments

### Technical Infrastructure
- **Business Intelligence**: Dashboard creation and KPI tracking with Apache Superset
- **Container Orchestration**: Docker and Docker Compose for reproducible environments
- **Database Integration**: PostgreSQL with analytics tools and complex SQL queries
- **ETL Processes**: Data extraction, transformation, and loading workflows

### Business Intelligence & Visualization
- **Interactive Dashboards**: Creating actionable business dashboards
- **Data Storytelling**: Presenting insights through compelling visualizations
- **Executive Reporting**: Summarizing complex analysis for stakeholder communication
- **Real-time Analytics**: Setting up systems for ongoing data monitoring

## 🔮 Future Enhancements

Potential areas for expansion:

1. **Machine Learning Models**: 
   - App success prediction
   - Price optimization models
   - User rating prediction

2. **Advanced Analytics**:
   - Time series analysis (if temporal data available)
   - Clustering analysis for app categorization
   - Market basket analysis for genre relationships

3. **Real-time Data Integration**:
   - API integration for live App Store data
   - Automated data pipeline with Airflow
   - Real-time dashboard updates

4. **Enhanced Visualizations**:
   - Geographic analysis (if location data available)
   - Network analysis of app relationships
   - Advanced statistical visualizations

## 🧪 A/B Testing Simulation

This project includes a comprehensive A/B testing simulation component that generates realistic user interaction data for various app store optimization experiments. The simulation creates statistically significant datasets that mirror real-world A/B testing scenarios.

### Test Scenarios Implemented

#### 1. **App Icon Design Test** (3 variants)
- **Control**: Original icon design (baseline conversion rate)
- **Variant A**: Minimalist icon design (+2% conversion boost)
- **Variant B**: Colorful icon design (+3.5% conversion boost)
- **Hypothesis**: Visual appeal affects user download decisions

#### 2. **App Description Length Test** (2 variants)
- **Control**: Short description (50-100 words)
- **Variant A**: Detailed description (200-300 words, +2.5% conversion boost)
- **Hypothesis**: More information leads to better-informed and more confident download decisions

#### 3. **Pricing Strategy Test** (3 variants)
- **Control**: Free app (+8% conversion boost)
- **Variant A**: Freemium model (+4% conversion boost)
- **Variant B**: Paid app ($2.99, no boost - baseline)
- **Hypothesis**: Lower barriers to entry increase adoption rates

#### 4. **Screenshot Count Test** (2 variants)
- **Control**: 3 screenshots
- **Variant A**: 5 screenshots (+1.5% conversion boost)
- **Hypothesis**: More visual information increases user confidence

### Simulation Parameters & Realism

#### User Demographics (Weighted Distribution)
- **Age Groups**: 18-24 (20%), 25-34 (35%), 35-44 (25%), 45-54 (15%), 55+ (5%)
- **Device Types**: iPhone (60%), iPad (25%), Apple Watch (10%), Mac (5%)
- **Geographic Distribution**: US (40%), UK (15%), CA (10%), AU (8%), DE (7%), others (20%)
- **App Genres**: 17 categories matching original dataset distribution

#### Behavioral Modeling
- **Base Conversion Rate**: 15% (industry standard for app stores)
- **Time Spent**: Normal distribution around 45-60 seconds
- **Rating Correlation**: Higher ratings for users who engaged longer
- **Statistical Significance**: Sample sizes ensure reliable results

### Generated Dataset Characteristics

#### Volume & Timeframe
- **Total Sessions**: 15,000 user interactions
- **Test Duration**: 45 days of simulated data
- **Daily Sessions**: ~333 sessions per day with realistic variance
- **Overall Conversion Rate**: 22.57% (after variant effects)

#### Data Quality Features
- **Realistic User Journeys**: Time spent correlates with conversion likelihood
- **Demographic Effects**: Younger users show higher conversion rates
- **Device-Specific Behavior**: iPhone users convert better than other devices
- **Geographic Variations**: Different countries show varied response patterns
- **Temporal Patterns**: Sessions distributed across realistic time periods

### Results (Based on Simulation Logic)

<img width="908" height="310" alt="image" src="https://github.com/user-attachments/assets/31046b06-d7d7-46d8-a303-d151846a506e" />

<img width="1678" height="864" alt="image" src="https://github.com/user-attachments/assets/1b1a3612-b5f9-47dd-8132-a2586a2291c6" />

<img width="1675" height="857" alt="image" src="https://github.com/user-attachments/assets/2e82f395-c702-4646-9af4-6e72f2399650" />

<img width="1668" height="595" alt="image" src="https://github.com/user-attachments/assets/b6ffb42d-e966-4ae2-8273-18d86eaa3a73" />


### Implementation & Usage

#### Running the A/B Test Simulation

```bash
# Navigate to project directory
cd "Apple AppStore Analytics"

# Install dependencies (if not already done)
pip install faker psycopg2-binary pandas numpy

# Generate A/B testing data
python scripts/ab_testing_simulation.py
```

**Output**: The script creates realistic conversion rate differences based on:
- User demographics (age, device type, location)  
- App characteristics (genre, features)
- Variant effectiveness (based on real-world patterns)

#### Database Tables Created

1. **`ab_test_sessions`** (15,000 records): Detailed user session data with demographics, test assignments, and outcomes
2. **`ab_test_variants`** (10 records): Test variant definitions and descriptions  
3. **`ab_test_summary`** (10 records): Pre-aggregated conversion rates and metrics by variant

#### Data Validation Queries

```sql
-- Check total sessions generated
SELECT COUNT(*) as total_sessions FROM ab_test_sessions;

-- View A/B test performance summary  
SELECT test_name, variant_key, 
       ROUND(conversion_rate * 100, 2) as conv_rate_pct
FROM ab_test_summary 
ORDER BY test_name, conversion_rate DESC;

-- Analyze demographic patterns
SELECT age_group, device_type, 
       COUNT(*) as users,
       ROUND(AVG(CASE WHEN converted THEN 1.0 ELSE 0.0 END) * 100, 1) as conv_rate
FROM ab_test_sessions
GROUP BY age_group, device_type
ORDER BY conv_rate DESC;
```

### 📊 Superset Dashboard Creation

The project includes a comprehensive guide for creating interactive dashboards in Apache Superset. Access the detailed tutorial in `ab_testing_superset_guide.ipynb`.

#### Available Chart Types & Configurations

1. **📈 Conversion Rate Comparison (Bar Chart)**
   - Compare performance across all test variants
   - X-axis: Test variants, Y-axis: Conversion rates
   - Color coding by test type

2. **📉 Daily Conversion Trends (Line Chart)**  
   - Track conversion rates over time
   - Multiple series for different variants
   - Identify patterns and anomalies

3. **🔥 Demographics Heatmap**
   - Conversion rates by age group and device type
   - Color intensity represents performance
   - Identify high-performing user segments

4. **📦 Time Spent Analysis (Box Plot)**
   - Distribution of session durations by variant
   - Compare engagement patterns
   - Identify variants that keep users engaged

5. **🌍 Geographic Performance (World Map/Bar Chart)**
   - Conversion rates by country and pricing variant
   - Identify regional preferences
   - Optimize global strategies

6. **🌳 App Genre Performance (Treemap)**
   - Multi-dimensional view of app categories
   - Size by session volume, color by conversion rate
   - Hierarchical genre and variant analysis

7. **📋 Statistical Significance Table**
   - Comprehensive test results summary
   - Sample sizes and confidence levels
   - Decision-making framework

#### Some Superset Dashboard Screenshots


#### Dashboard Features

- **Interactive Filters**: Date range, geography, demographics, app genre
- **Drill-down Capabilities**: Click through from high-level to detailed views
- **Real-time Updates**: Refresh data as new sessions are added
- **Export Options**: Download charts and data for presentations


#### Quick Start Guide

1. **Access Superset**: http://localhost:8088 (admin/admin)
2. **Add Database**: PostgreSQL connection to analytics_db
3. **Create Charts**: Use SQL queries from the guide notebook
4. **Build Dashboard**: Combine charts with filters and interactions
5. **Share Insights**: Export or share dashboard links with stakeholders

### 🎯 Key Business Insights 

#### Primary Findings
- **Icon Design Impact**: Colorful icons outperform minimalist and original designs
- **Content Strategy**: Detailed descriptions significantly boost conversions  
- **Pricing Psychology**: Free apps dominate, but freemium shows strong potential
- **Visual Communication**: Additional screenshots provide marginal improvements

#### Demographic Insights
- **Age Segmentation**: Younger users (18-34) show highest conversion rates
- **Device Preferences**: iPhone users convert at higher rates than other devices
- **Geographic Variations**: US and UK markets show different response patterns
- **Genre Performance**: Games and Entertainment apps show highest engagement

#### Statistical Confidence
- **Sample Sizes**: All tests achieve statistical significance (>1000 users per variant)
- **Confidence Levels**: Results reliable at 95% confidence interval
- **Effect Sizes**: Meaningful differences between variants (>2% conversion impact)
- **Practical Significance**: Results have real business impact potential

## Future Enhancements

### Scaling for Real-World Usage

1. **Data Volume**: Current simulation handles 15K sessions; production use case may require:
   - Database partitioning for millions of sessions
   - Data archiving strategies
   - Query optimization for large datasets

2. **Real-time Processing**: 
   - Stream processing for live A/B test results
   - Cache layers for dashboard performance
   - Automated alerting for significant changes

3. **Security & Compliance**:
   - User data anonymization
   - GDPR compliance for European users
   - Access controls for sensitive metrics

4. **Integration Points**:
   - App store APIs for real conversion data
   - Marketing automation platforms
   - Business intelligence ecosystems

## 🔧 Troubleshooting & FAQ

### Common Issues & Solutions

#### Docker Container Issues
```bash
# If containers fail to start
docker-compose down
docker-compose up -d --force-recreate

# Check container logs
docker-compose logs superset_app
docker-compose logs postgres_container
```

#### Database Connection Problems
```bash
# Test PostgreSQL connection
PGPASSWORD=postgres psql -h localhost -p 5001 -U postgres -d analytics_db -c "SELECT version();"

# Reset database if needed
docker-compose down -v  # WARNING: This deletes all data
docker-compose up -d
```

#### Python Dependencies
```bash
# If Faker installation fails
pip install --upgrade pip
pip install faker==19.12.0

# For macOS with Apple Silicon
pip install psycopg2-binary --no-cache-dir
```

#### Superset Access Issues
- **URL**: Ensure you're using http://localhost:8088 (not https)
- **Login**: Default credentials are admin/admin
- **Browser**: Try clearing cache or using incognito mode
- **Ports**: Check that port 8088 isn't used by other applications

### Frequently Asked Questions

**Q: Can I modify the A/B test parameters?**
A: Yes! Edit the `ABTestSimulator` class parameters in `ab_testing_simulation.py`:
- Change `num_users` for different sample sizes
- Modify `test_duration_days` for longer/shorter test periods
- Adjust conversion probability logic for different effect sizes

**Q: How do I add new test variants?**
A: Extend the `generate_test_variants()` method to include additional experiments:
```python
'new_test': {
    'test_id': 'new_test_005',
    'test_name': 'New Feature Test',
    'variants': {
        'control': {'name': 'Original', 'description': 'Current version'},
        'variant_a': {'name': 'New Feature', 'description': 'With new feature'}
    }
}
```

**Q: Can I connect to external databases?**
A: Yes! Modify the `DB_CONFIG` in the simulation script to point to your database:
```python
DB_CONFIG = {
    'host': 'your-db-host',
    'port': 5432,
    'database': 'your-database',
    'user': 'your-username',
    'password': 'your-password'
}
```

**Q: How accurate is the simulation compared to real A/B tests?**
A: The simulation uses industry-standard conversion rates and realistic user behavior patterns. While not identical to real tests, it demonstrates proper A/B testing methodology and statistical analysis techniques.

**Q: Can I use this for other types of A/B tests?**
A: Absolutely! The framework can be adapted for:
- E-commerce conversion testing
- Email marketing campaigns  
- Website optimization experiments
- Mobile app feature testing






