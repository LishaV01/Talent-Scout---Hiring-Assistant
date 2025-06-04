#!/usr/bin/env python3
"""
Setup script for TalentScout Hiring Assistant
Handles environment setup, dependency installation, and database initialization
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("""
    ╔══════════════════════════════════════════╗
    ║   TalentScout Hiring Assistant Setup     ║
    ╚══════════════════════════════════════════╝
    """)

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    print("\n📦 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def get_pip_command():
    """Get the appropriate pip command for the platform"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "pip")
    else:
        return os.path.join("venv", "bin", "pip")

def get_python_command():
    """Get the appropriate python command for the platform"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python")
    else:
        return os.path.join("venv", "bin", "python")

def install_dependencies():
    """Install required dependencies"""
    print("\n📚 Installing dependencies...")
    pip_cmd = get_pip_command()
    
    try:
        # Upgrade pip first
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_environment_file():
    """Create .env file from template"""
    print("\n🔐 Setting up environment file...")
    
    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        response = input("   Overwrite? (y/N): ").lower()
        if response != 'y':
            print("   Keeping existing .env file")
            return True
    
    try:
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as template:
                content = template.read()
        else:
            # Create default content if .env.example doesn't exist
            content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration (Optional)
MODEL_NAME=gpt-3.5-turbo
MAX_TOKENS=500
TEMPERATURE=0.7

# Voice Configuration (Optional)
ENABLE_VOICE=true
"""
        
        with open(".env", "w") as env_file:
            env_file.write(content)
        
        print("✅ .env file created")
        print("   ⚠️  Remember to add your OpenAI API key to .env file!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ["docs", "logs", "data"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")
    return True

def initialize_database():
    """Initialize the database"""
    print("\n🗄️ Initializing database...")
    python_cmd = get_python_command()
    
    # First check if database.py exists
    if not os.path.exists("database.py"):
        print("⚠️  database.py not found - skipping database initialization")
        print("   The database will be created when you first run the app")
        return True
    
    try:
        # Create a simple script to initialize the database
        init_script = """
import sqlite3
import sys

try:
    from database import DatabaseManager
    
    # Initialize the database
    db = DatabaseManager()
    print("Database initialized successfully at talentscout.db")
    
except ImportError:
    print("Database module not found - will be initialized on first run")
except Exception as e:
    print(f"Database initialization error: {e}")
    sys.exit(1)
"""
        
        # Write the script to a temporary file
        with open("_init_db_temp.py", "w") as f:
            f.write(init_script)
        
        # Run the script
        result = subprocess.run([python_cmd, "_init_db_temp.py"], capture_output=True, text=True)
        
        # Remove the temporary file
        if os.path.exists("_init_db_temp.py"):
            os.remove("_init_db_temp.py")
        
        if result.returncode == 0:
            print("✅ Database initialized successfully")
            if os.path.exists("talentscout.db"):
                print(f"   Database file created: talentscout.db")
            return True
        else:
            print("⚠️  Database initialization skipped")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            print("   The database will be created when you first run the app")
            return True
            
    except Exception as e:
        print(f"⚠️  Database initialization skipped: {e}")
        print("   The database will be created when you first run the app")
        # Clean up temp file if it exists
        if os.path.exists("_init_db_temp.py"):
            os.remove("_init_db_temp.py")
        return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*50)
    print("✨ Setup completed successfully!")
    print("="*50)
    print("\n📋 Next steps:")
    print("1. Add your OpenAI API key to the .env file")
    print("2. Activate the virtual environment:")
    if platform.system() == "Windows":
        print("   > venv\\Scripts\\activate")
    else:
        print("   $ source venv/bin/activate")
    print("3. Run the main application:")
    print("   $ streamlit run app.py")
    print("4. Run the admin dashboard (optional):")
    print("   $ streamlit run admin_dashboard.py")
    print("\n📊 Backend Features:")
    print("   - All candidate data is automatically saved to database")
    print("   - View and export data using the admin dashboard")
    print("   - Database file: talentscout.db")
    print("\n💡 For more information, check the README.md file")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment file
    if not setup_environment_file():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Initialize database (optional - won't fail setup if it doesn't work)
    initialize_database()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()