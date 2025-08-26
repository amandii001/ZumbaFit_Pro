#!/usr/bin/env python3
"""
Simple API Test
"""

import requests
import json

def test_login():
    """Test login endpoint"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing login...")
    
    # Test login endpoint
    login_data = {
        "email": "newtest@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
        else:
            print("❌ Login failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_registration():
    """Test registration endpoint"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing registration...")
    
    # Test registration endpoint
    test_user = {
        "name": "New Test User",
        "email": "newtest@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
        else:
            print("❌ Registration failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()
