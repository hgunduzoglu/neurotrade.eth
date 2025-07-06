#!/usr/bin/env python3
"""
NeuroTrade.eth Launcher Script

This script helps start both the frontend and AI agent services.
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def print_banner():
    """Print the NeuroTrade banner"""
    print("=" * 60)
    print("🚀 NeuroTrade.eth - AI Trading Agent Launcher")
    print("=" * 60)
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("📋 Checking dependencies...")
    
    # Check if Python is available
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("❌ Python not found")
        return False
    
    # Check if Node.js is available
    try:
        result = subprocess.run(["node", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Node.js: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("❌ Node.js not found. Please install Node.js first.")
        return False
    
    # Check if npm is available
    try:
        result = subprocess.run(["npm", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ npm: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("❌ npm not found")
        return False
    
    return True

def install_python_dependencies():
    """Install Python dependencies for the AI agent"""
    print("\n🔧 Installing Python dependencies...")
    
    agent_dir = Path("neurotrade_ai_agent")
    if not agent_dir.exists():
        print("❌ neurotrade_ai_agent directory not found")
        return False
    
    requirements_file = agent_dir / "requirements.txt"
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                      check=True)
        print("✅ Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False

def install_node_dependencies():
    """Install Node.js dependencies for the frontend"""
    print("\n🔧 Installing Node.js dependencies...")
    
    try:
        subprocess.run(["npm", "install"], check=True)
        print("✅ Node.js dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Node.js dependencies: {e}")
        return False

def start_ai_agent():
    """Start the AI agent API bridge"""
    print("\n🤖 Starting AI Agent API Bridge...")
    
    agent_dir = Path("neurotrade_ai_agent")
    api_bridge_file = agent_dir / "api_bridge.py"
    
    if not api_bridge_file.exists():
        print("❌ api_bridge.py not found")
        return None
    
    try:
        # Start the API bridge with uvicorn
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "neurotrade_ai_agent.api_bridge:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ AI Agent API Bridge started on http://localhost:8000")
            return process
        else:
            print("❌ AI Agent API Bridge failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting AI Agent: {e}")
        return None

def start_frontend():
    """Start the Next.js frontend"""
    print("\n🌐 Starting Frontend...")
    
    try:
        process = subprocess.Popen(["npm", "run", "dev"])
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ Frontend started on http://localhost:3000")
            return process
        else:
            print("❌ Frontend failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def main():
    """Main launcher function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install required dependencies.")
        sys.exit(1)
    
    # Install dependencies
    if not install_python_dependencies():
        print("\n❌ Failed to install Python dependencies.")
        sys.exit(1)
    
    if not install_node_dependencies():
        print("\n❌ Failed to install Node.js dependencies.")
        sys.exit(1)
    
    # Start services
    ai_agent_process = start_ai_agent()
    if not ai_agent_process:
        print("\n❌ Failed to start AI agent. Exiting.")
        sys.exit(1)
    
    frontend_process = start_frontend()
    if not frontend_process:
        print("\n❌ Failed to start frontend. Cleaning up...")
        ai_agent_process.terminate()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 NeuroTrade.eth is now running!")
    print("📊 Frontend: http://localhost:3000")
    print("🤖 AI Agent API: http://localhost:8000")
    print("=" * 60)
    print("\n💡 Press Ctrl+C to stop all services")
    
    # Wait for user to stop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping services...")
        
        # Gracefully stop processes
        if frontend_process:
            frontend_process.terminate()
        if ai_agent_process:
            ai_agent_process.terminate()
        
        # Wait a bit for graceful shutdown
        time.sleep(2)
        
        # Force kill if still running
        if frontend_process and frontend_process.poll() is None:
            frontend_process.kill()
        if ai_agent_process and ai_agent_process.poll() is None:
            ai_agent_process.kill()
        
        print("✅ All services stopped. Goodbye!")

if __name__ == "__main__":
    main() 