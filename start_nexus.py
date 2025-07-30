#!/usr/bin/env python3
"""
NEXUS AI Startup Script
Starts both backend API server and frontend server
"""

import subprocess
import time
import sys
import os
import signal
import threading

def start_backend():
    """Start the NEXUS API backend server"""
    print("🚀 Starting NEXUS API Backend...")
    try:
        # Start backend server
        backend_process = subprocess.Popen([
            sys.executable, "nexus_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test if server is running
        import requests
        try:
            response = requests.get("http://localhost:5001/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server started successfully!")
                return backend_process
            else:
                print(f"❌ Backend server failed to start: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Backend server failed to start: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend server"""
    print("🎨 Starting NEXUS Frontend...")
    try:
        # Change to frontend directory
        os.chdir("frontend")
        
        # Start frontend server
        frontend_process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Test if server is running
        import requests
        try:
            response = requests.get("http://localhost:8000", timeout=5)
            if response.status_code == 200:
                print("✅ Frontend server started successfully!")
                return frontend_process
            else:
                print(f"❌ Frontend server failed to start: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Frontend server failed to start: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def test_system():
    """Test the complete system"""
    print("\n🧪 Testing Complete System...")
    
    import requests
    
    # Test backend
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API: OK")
        else:
            print(f"❌ Backend API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend API: {e}")
        return False
    
    # Test frontend
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: OK")
        else:
            print(f"❌ Frontend: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend: {e}")
        return False
    
    # Test integration
    try:
        response = requests.post(
            "http://localhost:5001/api/nexus/query",
            json={"message": "How do I build a deck?"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Integration: OK")
            print(f"   Response: {data['response']}")
            print(f"   Domain: {data['routing']['domain']}")
        else:
            print(f"❌ Integration: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Integration: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🚀 NEXUS AI System Startup")
    print("=" * 40)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        return False
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Exiting.")
        backend_process.terminate()
        return False
    
    # Test system
    if test_system():
        print("\n🎉 NEXUS AI System is running successfully!")
        print("\n🌐 Access your NEXUS AI system:")
        print("  Frontend: http://localhost:8000")
        print("  Backend API: http://localhost:5001")
        print("  Health Check: http://localhost:5001/health")
        print("\n📝 Test queries you can try:")
        print("  - 'How do I build a deck?'")
        print("  - 'Help me with Python programming'")
        print("  - 'What plants grow well in shade?'")
        print("  - 'How do I cook pasta?'")
        print("  - 'I need help with math homework'")
        print("\n⏹️  Press Ctrl+C to stop the servers")
        
        try:
            # Keep servers running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down NEXUS AI servers...")
            backend_process.terminate()
            frontend_process.terminate()
            print("✅ Servers stopped.")
            return True
    else:
        print("❌ System test failed. Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 