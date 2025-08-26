#!/usr/bin/env python3
"""
ZumbaFit Pro Environment Setup Script
Handles protobuf compatibility issues between TensorFlow and MediaPipe
"""

import subprocess
import sys
import os

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

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_virtual_environment():
    """Create and activate virtual environment"""
    if not os.path.exists("venv"):
        print("🔄 Creating virtual environment...")
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    else:
        print("✅ Virtual environment already exists")
    return True

def install_dependencies():
    """Install dependencies with protobuf compatibility fix"""
    print("\n🔧 Installing dependencies...")
    
    # First, upgrade pip
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install protobuf 3.20.3 first (compatible with both TensorFlow and MediaPipe)
    if not run_command("pip install protobuf==3.20.3", "Installing protobuf 3.20.3"):
        return False
    
    # Install other dependencies
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        return False
    
    # Verify protobuf version
    try:
        result = subprocess.run("pip show protobuf", shell=True, capture_output=True, text=True)
        if "3.20.3" in result.stdout:
            print("✅ Protobuf version verified: 3.20.3")
        else:
            print("⚠️  Warning: Protobuf version may not be correct")
            print(result.stdout)
    except:
        print("⚠️  Could not verify protobuf version")
    
    return True

def verify_installation():
    """Verify that key packages are installed correctly"""
    print("\n🔍 Verifying installation...")
    
    packages_to_check = [
        "fastapi",
        "tensorflow", 
        "opencv-python",
        "mediapipe",
        "protobuf"
    ]
    
    for package in packages_to_check:
        try:
            result = subprocess.run(f"pip show {package}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {package} installed")
            else:
                print(f"❌ {package} not found")
        except:
            print(f"⚠️  Could not verify {package}")

def main():
    """Main setup function"""
    print("🎵 ZumbaFit Pro Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        print("❌ Failed to setup virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Verify installation
    verify_installation()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    print("   Windows: venv\\Scripts\\activate")
    print("   macOS/Linux: source venv/bin/activate")
    print("2. Start the backend: python start_backend.py")
    print("3. Start the frontend: python start_frontend.py")
    print("4. Access the application:")
    print("   Frontend: http://localhost:8080")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
