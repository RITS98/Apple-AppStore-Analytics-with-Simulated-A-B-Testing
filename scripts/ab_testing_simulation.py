#!/usr/bin/env python3
"""
A/B Testing Simulation for Apple App Store Analytics
====================================================

This script simulates A/B testing scenarios for various app store features:
1. App Icon Design (Control vs Variant)
2. App Description Style (Short vs Detailed)
3. Pricing Strategy (Free vs Freemium vs Paid)
4. App Store Screenshots (3 vs 5 screenshots)

The simulation generates realistic user interaction data and stores it in PostgreSQL
for analysis in Apache Superset.
"""

import pandas as pd
import numpy as np
from faker import Faker
import psycopg2
from psycopg2.extras import execute_values
import random
from datetime import datetime, timedelta
import uuid
import json


fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)


DB_CONFIG = {
    'host': 'localhost',
    'port': 5001,
    'database': 'analytics_db',
    'user': 'postgres',
    'password': 'postgres'
}

class ABTestSimulator:
    def __init__(self, num_users=10000, test_duration_days=30):
        self.num_users = num_users
        self.test_duration_days = test_duration_days
        self.start_date = datetime.now() - timedelta(days=test_duration_days)
        self.end_date = datetime.now()
        
        # App categories from the original dataset
        self.app_genres = [
            'Games', 'Entertainment', 'Education', 'Photo & Video', 
            'Music', 'Social Networking', 'Shopping', 'Productivity',
            'Finance', 'Sports', 'Food & Drink', 'Travel', 'News',
            'Health & Fitness', 'Utilities', 'Weather', 'Reference'
        ]
        
        # Device types
        self.device_types = ['iPhone', 'iPad', 'Apple Watch', 'Mac']
        
        # Countries for geographic analysis
        self.countries = ['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP', 'IN', 'BR', 'MX']
        
    def generate_test_variants(self):
        """Define A/B test variants"""
        return {
            'icon_design_test': {
                'test_id': 'icon_design_001',
                'test_name': 'App Icon Design Test',
                'variants': {
                    'control': {'name': 'Original Icon', 'description': 'Current app icon design'},
                    'variant_a': {'name': 'Minimalist Icon', 'description': 'Clean, minimalist icon design'},
                    'variant_b': {'name': 'Colorful Icon', 'description': 'Bright, colorful icon design'}
                }
            },
            'description_test': {
                'test_id': 'description_002',
                'test_name': 'App Description Length Test',
                'variants': {
                    'control': {'name': 'Short Description', 'description': 'Concise app description (50-100 words)'},
                    'variant_a': {'name': 'Detailed Description', 'description': 'Comprehensive app description (200-300 words)'},
                }
            },
            'pricing_test': {
                'test_id': 'pricing_003',
                'test_name': 'Pricing Strategy Test',
                'variants': {
                    'control': {'name': 'Free', 'description': 'Completely free app'},
                    'variant_a': {'name': 'Freemium', 'description': 'Free with in-app purchases'},
                    'variant_b': {'name': 'Paid', 'description': 'One-time purchase ($2.99)'}
                }
            },
            'screenshots_test': {
                'test_id': 'screenshots_004',
                'test_name': 'Screenshot Count Test',
                'variants': {
                    'control': {'name': '3 Screenshots', 'description': 'App store listing with 3 screenshots'},
                    'variant_a': {'name': '5 Screenshots', 'description': 'App store listing with 5 screenshots'},
                }
            }
        }
    
    def generate_user_sessions(self):
        """Generate user session data"""
        sessions = []
        
        for _ in range(self.num_users):
            user_id = str(uuid.uuid4())
            session_date = fake.date_time_between(start_date=self.start_date, end_date=self.end_date)
            
            # User characteristics
            age_group = random.choices(
                ['18-24', '25-34', '35-44', '45-54', '55+'],
                weights=[20, 35, 25, 15, 5]
            )[0]
            
            device_type = random.choices(
                self.device_types,
                weights=[60, 25, 10, 5]
            )[0]
            
            country = random.choices(
                self.countries,
                weights=[40, 15, 10, 8, 7, 6, 5, 4, 3, 2]
            )[0]
            
            # App being tested
            app_genre = random.choice(self.app_genres)
            app_name = f"{fake.company()} {fake.word().title()}"
            
            # Assign to test variants
            tests = self.generate_test_variants()
            user_tests = {}
            
            for test_key, test_info in tests.items():
                variants = list(test_info['variants'].keys())
                assigned_variant = random.choice(variants)
                user_tests[test_key] = assigned_variant
            
            # Generate user behavior based on variants
            conversion_probability = self.calculate_conversion_probability(user_tests, age_group, device_type)
            converted = random.random() < conversion_probability
            
            # Time spent on app store page (in seconds)
            base_time = 45
            if user_tests['description_test'] == 'variant_a':  # Detailed description
                base_time += random.randint(10, 30)
            if user_tests['screenshots_test'] == 'variant_a':  # More screenshots
                base_time += random.randint(5, 20)
            
            time_spent = max(5, int(np.random.normal(base_time, 15)))
            
            # Rating (if user converted and installed the app)
            rating = None
            if converted:
                # Different variants affect satisfaction
                base_rating = 4.0
                if user_tests['icon_design_test'] in ['variant_a', 'variant_b']:
                    base_rating += random.uniform(-0.2, 0.4)
                if user_tests['pricing_test'] == 'control':  # Free apps might get slightly lower ratings
                    base_rating += random.uniform(-0.3, 0.1)
                
                rating = min(5.0, max(1.0, base_rating + random.uniform(-1.0, 1.0)))
                rating = round(rating, 1)
            
            sessions.append({
                'user_id': user_id,
                'session_date': session_date,
                'app_name': app_name,
                'app_genre': app_genre,
                'age_group': age_group,
                'device_type': device_type,
                'country': country,
                'icon_design_variant': user_tests['icon_design_test'],
                'description_variant': user_tests['description_test'],
                'pricing_variant': user_tests['pricing_test'],
                'screenshots_variant': user_tests['screenshots_test'],
                'time_spent_seconds': time_spent,
                'converted': converted,
                'rating': rating,
                'session_id': str(uuid.uuid4())
            })
        
        return pd.DataFrame(sessions)
    
    def calculate_conversion_probability(self, user_tests, age_group, device_type):
        """Calculate conversion probability based on test variants and user characteristics"""
        base_prob = 0.15  # 15% base conversion rate
        
        # Icon design effects
        if user_tests['icon_design_test'] == 'variant_a':  # Minimalist
            base_prob += 0.02
        elif user_tests['icon_design_test'] == 'variant_b':  # Colorful
            base_prob += 0.035
        
        # Description effects
        if user_tests['description_test'] == 'variant_a':  # Detailed
            base_prob += 0.025
        
        # Pricing effects
        if user_tests['pricing_test'] == 'control':  # Free
            base_prob += 0.08
        elif user_tests['pricing_test'] == 'variant_a':  # Freemium
            base_prob += 0.04
        # Paid apps have lower conversion (no boost)
        
        # Screenshot effects
        if user_tests['screenshots_test'] == 'variant_a':  # More screenshots
            base_prob += 0.015
        
        # Age group effects
        age_multipliers = {
            '18-24': 1.2,
            '25-34': 1.1,
            '35-44': 1.0,
            '45-54': 0.9,
            '55+': 0.8
        }
        base_prob *= age_multipliers.get(age_group, 1.0)
        
        # Device type effects
        device_multipliers = {
            'iPhone': 1.0,
            'iPad': 0.9,
            'Apple Watch': 0.7,
            'Mac': 0.6
        }
        base_prob *= device_multipliers.get(device_type, 1.0)
        
        return min(0.95, max(0.01, base_prob))  # Cap between 1% and 95%
    
    def create_database_tables(self):
        """Create tables in PostgreSQL for A/B testing data"""
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Drop existing tables
        cur.execute("DROP TABLE IF EXISTS ab_test_sessions CASCADE;")
        cur.execute("DROP TABLE IF EXISTS ab_test_variants CASCADE;")
        cur.execute("DROP TABLE IF EXISTS ab_test_summary CASCADE;")
        
        # Create sessions table
        cur.execute("""
            CREATE TABLE ab_test_sessions (
                session_id VARCHAR(50) PRIMARY KEY,
                user_id VARCHAR(50) NOT NULL,
                session_date TIMESTAMP NOT NULL,
                app_name VARCHAR(200) NOT NULL,
                app_genre VARCHAR(50) NOT NULL,
                age_group VARCHAR(20) NOT NULL,
                device_type VARCHAR(20) NOT NULL,
                country VARCHAR(10) NOT NULL,
                icon_design_variant VARCHAR(20) NOT NULL,
                description_variant VARCHAR(20) NOT NULL,
                pricing_variant VARCHAR(20) NOT NULL,
                screenshots_variant VARCHAR(20) NOT NULL,
                time_spent_seconds INTEGER NOT NULL,
                converted BOOLEAN NOT NULL,
                rating DECIMAL(2,1),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create test variants table
        cur.execute("""
            CREATE TABLE ab_test_variants (
                test_id VARCHAR(50) NOT NULL,
                test_name VARCHAR(200) NOT NULL,
                variant_key VARCHAR(20) NOT NULL,
                variant_name VARCHAR(100) NOT NULL,
                variant_description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (test_id, variant_key)
            );
        """)
        
        # Create summary table for quick analysis
        cur.execute("""
            CREATE TABLE ab_test_summary (
                test_name VARCHAR(200) NOT NULL,
                variant_key VARCHAR(20) NOT NULL,
                total_users INTEGER NOT NULL,
                conversions INTEGER NOT NULL,
                conversion_rate DECIMAL(5,4) NOT NULL,
                avg_time_spent DECIMAL(8,2) NOT NULL,
                avg_rating DECIMAL(3,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (test_name, variant_key)
            );
        """)
        
        # Create indexes for better query performance
        cur.execute("CREATE INDEX idx_sessions_date ON ab_test_sessions(session_date);")
        cur.execute("CREATE INDEX idx_sessions_genre ON ab_test_sessions(app_genre);")
        cur.execute("CREATE INDEX idx_sessions_converted ON ab_test_sessions(converted);")
        cur.execute("CREATE INDEX idx_sessions_country ON ab_test_sessions(country);")
        
        conn.commit()
        cur.close()
        conn.close()
        print("Database tables created successfully!")
    
    def insert_test_variants(self):
        """Insert test variant definitions into database"""
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        tests = self.generate_test_variants()
        variant_data = []
        
        for test_key, test_info in tests.items():
            for variant_key, variant_info in test_info['variants'].items():
                variant_data.append((
                    test_info['test_id'],
                    test_info['test_name'],
                    variant_key,
                    variant_info['name'],
                    variant_info['description']
                ))
        
        execute_values(
            cur,
            """INSERT INTO ab_test_variants 
               (test_id, test_name, variant_key, variant_name, variant_description) 
               VALUES %s""",
            variant_data
        )
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"Inserted {len(variant_data)} test variants!")
    
    def insert_session_data(self, df):
        """Insert session data into PostgreSQL"""
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Convert DataFrame to list of tuples
        data = [tuple(row) for row in df.to_numpy()]
        
        execute_values(
            cur,
            """INSERT INTO ab_test_sessions 
               (user_id, session_date, app_name, app_genre, age_group, device_type, 
                country, icon_design_variant, description_variant, pricing_variant, 
                screenshots_variant, time_spent_seconds, converted, rating, session_id) 
               VALUES %s""",
            data
        )
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"Inserted {len(data)} session records!")
    
    def generate_summary_statistics(self):
        """Generate and insert summary statistics"""
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Generate summary for each test
        tests = [
            ('App Icon Design Test', 'icon_design_variant'),
            ('App Description Length Test', 'description_variant'),
            ('Pricing Strategy Test', 'pricing_variant'),
            ('Screenshot Count Test', 'screenshots_variant')
        ]
        
        for test_name, variant_column in tests:
            cur.execute(f"""
                INSERT INTO ab_test_summary 
                (test_name, variant_key, total_users, conversions, conversion_rate, 
                 avg_time_spent, avg_rating)
                SELECT 
                    '{test_name}' as test_name,
                    {variant_column} as variant_key,
                    COUNT(*) as total_users,
                    SUM(CASE WHEN converted THEN 1 ELSE 0 END) as conversions,
                    AVG(CASE WHEN converted THEN 1.0 ELSE 0.0 END) as conversion_rate,
                    AVG(time_spent_seconds::decimal) as avg_time_spent,
                    AVG(rating) as avg_rating
                FROM ab_test_sessions
                GROUP BY {variant_column};
            """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Generated summary statistics!")
    
    def run_simulation(self):
        """Run the complete A/B testing simulation"""
        print("🚀 Starting A/B Testing Simulation...")
        print(f"Generating data for {self.num_users:,} users over {self.test_duration_days} days")
        
        # Create database structure
        self.create_database_tables()
        
        # Insert test variant definitions
        self.insert_test_variants()
        
        # Generate session data
        print("Generating user session data...")
        df = self.generate_user_sessions()
        
        # Insert data into PostgreSQL
        print("Inserting data into PostgreSQL...")
        self.insert_session_data(df)
        
        # Generate summary statistics
        self.generate_summary_statistics()
        
        print("\nA/B Testing Simulation Complete!")
        print("\nSummary:")
        print(f"   • Total Users: {len(df):,}")
        print(f"   • Total Conversions: {df['converted'].sum():,}")
        print(f"   • Overall Conversion Rate: {df['converted'].mean():.2%}")
        print(f"   • Average Time Spent: {df['time_spent_seconds'].mean():.1f} seconds")
        print(f"   • Average Rating: {df[df['rating'].notna()]['rating'].mean():.2f}/5.0")
        
        return df

def main():
    """Main function to run the A/B testing simulation"""
    simulator = ABTestSimulator(num_users=15000, test_duration_days=45)
    df = simulator.run_simulation()
    
    print("\nReady for Superset Analysis!")
    print("You can now create charts in Superset using the following tables:")
    print("   • ab_test_sessions (detailed session data)")
    print("   • ab_test_variants (test variant definitions)")
    print("   • ab_test_summary (aggregated results)")
    
    return df

if __name__ == "__main__":
    main()
