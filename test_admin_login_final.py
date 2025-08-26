#!/usr/bin/env python3
"""
Final Admin Login Test
"""

import requests
import json

def test_admin_login_final():
    """Test admin login with email address"""
    base_url = "http://localhost:8000"
    
    print("🧪 Final Admin Login Test...")
    
    # Test admin login with email (as frontend sends)
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
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login successful!")
            print(f"   Admin ID: {data.get('admin_id')}")
            print(f"   Username: {data.get('username')}")
            print(f"   Role: {data.get('role')}")
            print(f"   Message: {data.get('message')}")
            
            print("\n🎉 Admin login is now working correctly!")
            print("📋 You can now login with:")
            print("   Email: admin@zumbafit.pro")
            print("   Password: admin123")
            
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_admin_login_final()
