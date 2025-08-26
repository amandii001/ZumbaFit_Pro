#!/usr/bin/env python3
"""
Test API Endpoints Script
"""

import requests
import json

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing API endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Make sure the backend server is running: python start_backend.py")
        return
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test registration endpoint
    test_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Registration endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Registration endpoint error: {e}")
    
    # Test login endpoint
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Login endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Login endpoint error: {e}")

if __name__ == "__main__":
    test_api()
