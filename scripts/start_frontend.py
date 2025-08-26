#!/usr/bin/env python3
"""
ZumbaFit Pro Frontend Server
"""

import http.server
import socketserver
import os
import sys

def main():
    """Start the frontend server"""
    PORT = 8080
    
    # Change to UI directory
    ui_dir = os.path.join(os.path.dirname(__file__), 'UI')
    if not os.path.exists(ui_dir):
        print(f"❌ UI directory not found: {ui_dir}")
        sys.exit(1)
    
    os.chdir(ui_dir)
    
    print("🎵 Starting ZumbaFit Pro Frontend...")
    print(f"📍 Frontend will be available at: http://localhost:{PORT}")
    print("🎨 Serving files from UI directory")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"🚀 Server started at port {PORT}")
            print("🛑 Press Ctrl+C to stop")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
