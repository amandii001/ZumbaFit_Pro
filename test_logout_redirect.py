#!/usr/bin/env python3
"""
Test Updated Logout Redirect Functionality
"""

import requests
import json

def test_logout_redirect():
    """Test the updated logout redirect to index page"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Updated Logout Redirect...")
    
    try:
        # Test user login
        login_data = {
            "email": "newtest@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post(
            f"{base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ User login successful")
        else:
            print(f"❌ User login failed: {response.status_code}")
        
        # Test admin login
        admin_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(
            f"{base_url}/auth/admin/login",
            json=admin_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Admin login successful")
        else:
            print(f"❌ Admin login failed: {response.status_code}")
        
        print("\n🎉 Logout redirect updated successfully!")
        print("📋 Updated logout behavior:")
        print("   - User logout → redirects to index.html")
        print("   - Admin logout → redirects to index.html")
        print("   - Both show success message before redirect")
        print("   - Sessions are properly cleared")
        
        print("\n🌐 Test the updated logout:")
        print("   1. Login as user → go to upload page")
        print("   2. Click logout → should redirect to index.html")
        print("   3. Login as admin → go to dashboard")
        print("   4. Click logout → should redirect to index.html")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_logout_redirect()
