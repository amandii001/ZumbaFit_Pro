#!/usr/bin/env python3
"""
Test Database Connection Script
"""

import mysql.connector
from mysql.connector import Error

def test_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    try:
        # Test connection without database first
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        print("✅ MySQL connection successful")
        
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if "zumbafitpro" in databases:
            print("✅ Database 'zumbafitpro' exists")
            
            # Connect to the specific database
            conn.close()
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="zumbafitpro"
            )
            cursor = conn.cursor()
            
            # Check tables
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            print(f"📋 Tables found: {tables}")
            
            # Check if users table exists and has data
            if "users" in tables:
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                print(f"👥 Users in database: {user_count}")
                
                # Show table structure
                cursor.execute("DESCRIBE users")
                columns = cursor.fetchall()
                print("📊 Users table structure:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")
            else:
                print("❌ Users table not found!")
                
            # Check if admin table exists
            if "admin" in tables:
                cursor.execute("SELECT COUNT(*) FROM admin")
                admin_count = cursor.fetchone()[0]
                print(f"👨‍💼 Admins in database: {admin_count}")
            else:
                print("❌ Admin table not found!")
                
        else:
            print("❌ Database 'zumbafitpro' does not exist!")
            print("Available databases:", databases)
            
        conn.close()
        
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure XAMPP is running")
        print("2. Check if MySQL service is started")
        print("3. Verify database credentials")
        print("4. Import the database schema from ZumbaFitPro_Database.txt")

def create_database_and_tables():
    """Create database and tables if they don't exist"""
    print("\n🔧 Creating database and tables...")
    
    try:
        # Connect without database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS zumbafitpro")
        print("✅ Database created/verified")
        
        # Use the database
        cursor.execute("USE zumbafitpro")
        
        # Read and execute the schema
        with open("ZumbaFitPro_Database.txt", "r") as f:
            schema = f.read()
        
        # Split by semicolon and execute each statement
        statements = schema.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    print(f"✅ Executed: {statement[:50]}...")
                except Error as e:
                    if "already exists" not in str(e).lower():
                        print(f"⚠️  Statement failed: {e}")
        
        conn.commit()
        print("✅ Database schema imported successfully")
        
        # Create a test admin user
        cursor.execute("SELECT COUNT(*) FROM admin")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            import bcrypt
            hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("""
                INSERT INTO admin (username, email, password_hash, role) 
                VALUES (%s, %s, %s, %s)
            """, ("admin", "admin@zumbafitpro.com", hashed_password, "super_admin"))
            conn.commit()
            print("✅ Test admin user created (username: admin, password: admin123)")
        
        conn.close()
        
    except Error as e:
        print(f"❌ Failed to create database: {e}")

if __name__ == "__main__":
    test_connection()
    create_database_and_tables()
    print("\n🔍 Final connection test:")
    test_connection()
