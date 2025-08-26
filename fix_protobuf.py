#!/usr/bin/env python3
"""
Quick Fix for Protobuf Compatibility Issues
Use this script if you encounter MediaPipe + TensorFlow conflicts
"""

import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Fix protobuf compatibility issues"""
    print("🔧 Quick Fix for Protobuf Compatibility Issues")
    print("=" * 50)
    
    # Check current protobuf version
    try:
        result = subprocess.run("pip show protobuf", shell=True, capture_output=True, text=True)
        if "3.20.3" in result.stdout:
            print("✅ Protobuf is already at correct version (3.20.3)")
            return
        else:
            print("⚠️  Current protobuf version may cause conflicts")
    except:
        print("⚠️  Could not check current protobuf version")
    
    # Uninstall conflicting packages
    print("\n🧹 Cleaning up conflicting packages...")
    packages_to_remove = ["protobuf", "tensorflow", "mediapipe"]
    
    for package in packages_to_remove:
        run_command(f"pip uninstall {package} -y", f"Uninstalling {package}")
    
    # Install protobuf 3.20.3 first
    if not run_command("pip install protobuf==3.20.3", "Installing protobuf 3.20.3"):
        print("❌ Failed to install protobuf 3.20.3")
        return
    
    # Install TensorFlow
    if not run_command("pip install tensorflow==2.15.0", "Installing TensorFlow"):
        print("❌ Failed to install TensorFlow")
        return
    
    # Install MediaPipe
    if not run_command("pip install mediapipe==0.10.7", "Installing MediaPipe"):
        print("❌ Failed to install MediaPipe")
        return
    
    # Verify installation
    print("\n🔍 Verifying installation...")
    try:
        result = subprocess.run("pip show protobuf", shell=True, capture_output=True, text=True)
        if "3.20.3" in result.stdout:
            print("✅ Protobuf version verified: 3.20.3")
        else:
            print("⚠️  Protobuf version may not be correct")
            print(result.stdout)
    except:
        print("⚠️  Could not verify protobuf version")
    
    # Test imports
    print("\n🧪 Testing imports...")
    try:
        import tensorflow as tf
        print("✅ TensorFlow imported successfully")
    except Exception as e:
        print(f"❌ TensorFlow import failed: {e}")
    
    try:
        import mediapipe as mp
        print("✅ MediaPipe imported successfully")
    except Exception as e:
        print(f"❌ MediaPipe import failed: {e}")
    
    print("\n🎉 Fix completed!")
    print("You can now run your ZumbaFit Pro application.")

if __name__ == "__main__":
    main()
