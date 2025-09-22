#!/usr/bin/env python3
"""
Setup script for Telegram Conversation Exporter
Helps users configure their API credentials.
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from template with user input."""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        overwrite = input(f".env file already exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return False
    
    if not env_example.exists():
        print("Error: .env.example file not found!")
        return False
    
    print("Setting up your Telegram API credentials...")
    print("\nTo get your API credentials:")
    print("1. Go to https://my.telegram.org/apps")
    print("2. Log in with your phone number")
    print("3. Create a new application")
    print("4. Copy your API ID and API Hash\n")
    
    # Get API credentials
    api_id = input("Enter your API ID: ").strip()
    if not api_id.isdigit():
        print("Error: API ID should be a number!")
        return False
    
    api_hash = input("Enter your API Hash: ").strip()
    if not api_hash:
        print("Error: API Hash cannot be empty!")
        return False
    
    phone_number = input("Enter your phone number (with country code, e.g., +1234567890): ").strip()
    if not phone_number.startswith('+'):
        print("Warning: Phone number should include country code (e.g., +1234567890)")
    
    session_name = input("Enter session name (default: telegram_session): ").strip()
    if not session_name:
        session_name = "telegram_session"
    
    # Create .env file
    with open(env_file, 'w') as f:
        f.write(f"# Telegram API credentials\n")
        f.write(f"API_ID={api_id}\n")
        f.write(f"API_HASH={api_hash}\n")
        f.write(f"\n")
        f.write(f"# Your phone number with country code\n")
        f.write(f"PHONE_NUMBER={phone_number}\n")
        f.write(f"\n")
        f.write(f"# Session name for persistent login\n")
        f.write(f"SESSION_NAME={session_name}\n")
    
    print(f"\n✅ Created .env file successfully!")
    print(f"Your credentials have been saved to .env")
    print(f"\n⚠️  Security reminder:")
    print(f"  - Keep your .env file secure and never share it")
    print(f"  - The .env file is already in .gitignore to prevent accidental commits")
    
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import telethon
        import aiofiles
        from dotenv import load_dotenv
        print("✅ All required dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main setup function."""
    print("Telegram Conversation Exporter - Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path('telegram_exporter.py').exists():
        print("Error: telegram_exporter.py not found!")
        print("Please run this script from the project directory.")
        return
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    if not check_dependencies():
        return
    
    # Setup environment
    print("\n2. Setting up environment...")
    if not create_env_file():
        return
    
    print("\n" + "=" * 40)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the exporter: python telegram_exporter.py")
    print("2. Follow the authentication prompts")
    print("3. Enter the username/name of the person to export")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()