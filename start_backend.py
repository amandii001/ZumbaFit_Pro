#!/usr/bin/env python3
"""
ZumbaFit Pro Backend Startup Script
"""

import uvicorn
import os
import sys

def main():
    """Start the FastAPI backend server"""
    print("🎵 Starting ZumbaFit Pro Backend...")
    print("📍 API will be available at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    print("🔄 Auto-reload enabled for development")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
