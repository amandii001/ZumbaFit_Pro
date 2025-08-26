#!/usr/bin/env python3
"""
Check Admin User Details
"""

import mysql.connector
from mysql.connector import Error

def check_admin_user():
    """Check admin user details in database"""
    
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
            
            # Check admin user
            cursor.execute("SELECT * FROM admin WHERE username = 'admin'")
            admin = cursor.fetchone()
            
            if admin:
                print("✅ Admin user found:")
                print(f"   Admin ID: {admin['admin_id']}")
                print(f"   Username: {admin['username']}")
                print(f"   Email: {admin['email']}")
                print(f"   Role: {admin['role']}")
                print(f"   Created: {admin['created_at']}")
                print(f"   Last Login: {admin['last_login']}")
            else:
                print("❌ Admin user not found")
                
    except Error as e:
        print(f"❌ Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    check_admin_user()
