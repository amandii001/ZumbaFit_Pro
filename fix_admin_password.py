#!/usr/bin/env python3
"""
Fix Admin Password Hash
"""

import mysql.connector
from mysql.connector import Error
import bcrypt

def fix_admin_password():
    """Update admin password with correct hash"""
    
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
            
            # Update admin password
            username = "admin"
            password = "admin123"
            
            # Hash password correctly
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Update admin user
            cursor.execute(
                "UPDATE admin SET password_hash = %s WHERE username = %s",
                (password_hash.decode('utf-8'), username)
            )
            
            conn.commit()
            print("✅ Admin password updated successfully!")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            
    except Error as e:
        print(f"❌ Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    fix_admin_password()
