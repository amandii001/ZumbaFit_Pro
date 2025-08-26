#!/usr/bin/env python3
"""
Test Admin Login with Email
"""

import requests
import json

def test_admin_email_login():
    """Test admin login with email address"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Admin Login with Email...")
    
    # Test admin login with email
    admin_data = {
        "email": "admin@zumbafit.pro",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/admin/login",
            json=admin_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login successful!")
            print(f"   Admin ID: {data.get('admin_id')}")
            print(f"   Username: {data.get('username')}")
            print(f"   Role: {data.get('role')}")
            print(f"   Message: {data.get('message')}")
        else:
            print("❌ Admin login failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_admin_email_login()
