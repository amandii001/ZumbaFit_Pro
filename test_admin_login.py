#!/usr/bin/env python3
"""
Test Admin Login with Database
"""

import requests
import json

def test_admin_login():
    """Test admin login functionality"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Admin Login with Database...")
    
    # Test admin login
    admin_data = {
        "username": "admin",
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

def test_admin_dashboard_data():
    """Test getting admin dashboard data"""
    base_url = "http://localhost:8000"
    
    print("\n🧪 Testing Admin Dashboard Data...")
    
    try:
        # Test getting video statistics
        response = requests.get(
            f"{base_url}/admin/stats",
            timeout=10
        )
        
        print(f"Stats Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard stats retrieved!")
            print(f"   Total Videos: {data.get('total_videos', 'N/A')}")
            print(f"   Total Users: {data.get('total_users', 'N/A')}")
            print(f"   Correct Postures: {data.get('correct_postures', 'N/A')}")
            print(f"   Incorrect Postures: {data.get('incorrect_postures', 'N/A')}")
        else:
            print("❌ Dashboard stats failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_admin_login()
    test_admin_dashboard_data()
