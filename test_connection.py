#!/usr/bin/env python3
"""
Test script to verify Telegram connection and list available conversations.
"""

import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel

# Load environment variables
load_dotenv()

async def test_connection():
    """Test connection to Telegram and list available conversations."""
    
    # Check environment variables
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    phone_number = os.getenv('PHONE_NUMBER')
    session_name = os.getenv('SESSION_NAME', 'telegram_session')
    
    if not all([api_id, api_hash, phone_number]):
        print("❌ Missing required environment variables!")
        print("Please run: python setup.py")
        return
    
    print("Testing Telegram connection...")
    print(f"API ID: {api_id}")
    print(f"Phone: {phone_number}")
    print(f"Session: {session_name}")
    print("-" * 40)
    
    try:
        # Create client and connect
        client = TelegramClient(session_name, int(api_id), api_hash)
        await client.start(phone=phone_number)
        
        print("✅ Successfully connected to Telegram!")
        
        # Get account info
        me = await client.get_me()
        print(f"Logged in as: {me.first_name} {me.last_name or ''} (@{me.username})")
        print(f"Phone: +{me.phone}")
        print(f"User ID: {me.id}")
        print()
        
        # List recent conversations
        print("Recent conversations:")
        print("-" * 40)
        
        count = 0
        async for dialog in client.iter_dialogs(limit=20):
            entity = dialog.entity
            count += 1
            
            # Format entity info
            if isinstance(entity, User):
                name = f"{entity.first_name or ''} {entity.last_name or ''}".strip()
                entity_type = "User"
                identifier = f"@{entity.username}" if entity.username else f"+{entity.phone}" if entity.phone else f"ID:{entity.id}"
            elif isinstance(entity, Chat):
                name = entity.title
                entity_type = "Group"
                identifier = f"ID:{entity.id}"
            elif isinstance(entity, Channel):
                name = entity.title
                entity_type = "Channel" if entity.broadcast else "Supergroup"
                identifier = f"@{entity.username}" if entity.username else f"ID:{entity.id}"
            else:
                name = f"Unknown_{entity.id}"
                entity_type = "Unknown"
                identifier = f"ID:{entity.id}"
            
            # Show unread count
            unread = f" ({dialog.unread_count} unread)" if dialog.unread_count > 0 else ""
            
            print(f"{count:2d}. {name}")
            print(f"    Type: {entity_type}")
            print(f"    ID: {identifier}")
            print(f"    Messages: {dialog.message.id if dialog.message else 'N/A'}{unread}")
            print()
        
        if count == 0:
            print("No conversations found.")
        else:
            print(f"Found {count} conversations.")
        
        print("\n" + "=" * 40)
        print("Connection test completed successfully!")
        print("You can now run: python telegram_exporter.py")
        
        await client.disconnect()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your API credentials in .env file")
        print("2. Ensure your phone number includes country code")
        print("3. Try deleting session files and re-authenticating")
        return

if __name__ == "__main__":
    asyncio.run(test_connection())