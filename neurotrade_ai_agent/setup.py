#!/usr/bin/env python3
"""
Setup script for NeuroTrade AI Agent
This script helps set up the agent for first-time users
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version < (3, 10):
        print(f"❌ Python {version.major}.{version.minor} is not supported.")
        print("💡 Please upgrade to Python 3.10 or higher.")
        return False
    print(f"✅ Python {version.major}.{version.minor} is compatible.")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")
        print("💡 Please run: pip install -r requirements.txt")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\n🔧 Setting up environment file...")
    
    if os.path.exists('.env'):
        print("✅ .env file already exists.")
        return True
    
    print("Creating .env file...")
    env_content = """# NeuroTrade AI Agent Environment Variables

# Required: Get your mailbox key from https://agentverse.ai
AGENT_MAILBOX_KEY=your_mailbox_key_here

# Optional: Customize these settings
AGENT_SEED=neurotrade_ai_agent_seed_2024
AGENT_PORT=8000
LOG_LEVEL=INFO
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("⚠️  Please edit the .env file and add your AGENT_MAILBOX_KEY")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def verify_installation():
    """Verify that the installation is working"""
    print("\n🧪 Verifying installation...")
    
    try:
        # Test imports
        from uagents import Agent
        print("✅ uAgents framework is working")
        
        import aiohttp
        print("✅ aiohttp is working")
        
        import requests
        print("✅ requests is working")
        
        from dotenv import load_dotenv
        print("✅ python-dotenv is working")
        
        # Test our modules
        from neurotrade_agent import TradingData
        print("✅ NeuroTrade agent modules are working")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def show_next_steps():
    """Show next steps to the user"""
    print("\n🎯 Next Steps:")
    print("="*50)
    print("1. 🔑 Get your Agentverse mailbox key:")
    print("   - Visit https://agentverse.ai")
    print("   - Create an account")
    print("   - Get your mailbox key")
    print("   - Add it to your .env file")
    print()
    print("2. 🧪 Test the agent:")
    print("   python test_agent.py")
    print()
    print("3. 🚀 Run the agent:")
    print("   python neurotrade_agent.py")
    print()
    print("4. 🌐 Check ASI:One:")
    print("   - Visit https://asi1.ai")
    print("   - Search for 'NeuroTrade' or 'trading'")
    print("   - Start chatting with your agent!")
    print()
    print("5. 📊 Example queries to try:")
    print("   - 'What's the current ETH price?'")
    print("   - 'Should I buy ETH now?'")
    print("   - 'Should I swap USDC to ETH?'")
    print("   - 'Cross-chain trading advice'")

def main():
    """Main setup function"""
    print("🚀 NeuroTrade AI Agent Setup")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create environment file
    if not create_env_file():
        return
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Installation verification failed.")
        print("💡 Please check the error messages above and try again.")
        return
    
    print("\n🎉 Setup completed successfully!")
    show_next_steps()

if __name__ == "__main__":
    main() 