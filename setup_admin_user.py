#!/usr/bin/env python3
"""
Setup Admin User in Database
"""

import mysql.connector
from mysql.connector import Error
import bcrypt

def setup_admin_user():
    """Create admin user if it doesn't exist"""
    
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="zumbafitpro"
        )
        
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            
            # Check if admin user exists
            cursor.execute("SELECT * FROM admin WHERE username = 'admin'")
            admin = cursor.fetchone()
            
            if admin:
                print("✅ Admin user already exists")
                print(f"   Username: {admin['username']}")
                print(f"   Role: {admin['role']}")
                return
            
            # Create admin user
            username = "admin"
            password = "admin123"
            email = "admin@zumbafitpro.com"
            role = "super_admin"
            
            # Hash password
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Insert admin user
            cursor.execute(
                "INSERT INTO admin (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                (username, email, password_hash.decode('utf-8'), role)
            )
            
            conn.commit()
            print("✅ Admin user created successfully!")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            print(f"   Role: {role}")
            
    except Error as e:
        print(f"❌ Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_admin_user()
