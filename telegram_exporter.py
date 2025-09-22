#!/usr/bin/env python3
"""
Telegram Conversation Exporter

This script exports all messages from a specific Telegram conversation,
including text messages, media files, voice messages, and other attachments.
"""

import asyncio
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

import aiofiles
from telethon import TelegramClient, events
from telethon.tl.types import (
    MessageMediaDocument, MessageMediaPhoto,
    DocumentAttributeAudio, DocumentAttributeVideo, DocumentAttributeSticker,
    DocumentAttributeAnimated, DocumentAttributeFilename,
    User, Chat, Channel
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_export.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TelegramExporter:
    def __init__(self):
        self.api_id = os.getenv('API_ID')
        self.api_hash = os.getenv('API_HASH')
        self.phone_number = os.getenv('PHONE_NUMBER')
        self.session_name = os.getenv('SESSION_NAME', 'telegram_session')
        
        if not all([self.api_id, self.api_hash, self.phone_number]):
            raise ValueError("Missing required environment variables. Check your .env file.")
        
        self.client = None  # Will be created when needed
    
    def _create_client(self):
        """Create the Telegram client if it doesn't exist."""
        if self.client is None:
            self.client = TelegramClient(self.session_name, int(self.api_id), self.api_hash)
        return self.client
        
    async def connect(self):
        """Connect to Telegram and authenticate if necessary."""
        self._create_client()
        await self.client.start(phone=self.phone_number)
        logger.info("Connected to Telegram successfully")
        
    async def disconnect(self):
        """Disconnect from Telegram."""
        if self.client:
            await self.client.disconnect()
        logger.info("Disconnected from Telegram")
        
    async def find_conversation(self, query: str) -> Optional[Any]:
        """Find a conversation by username, phone number, or name."""
        logger.info(f"Searching for conversation: {query}")
        client = self._create_client()
        
        # Try to find by username first
        try:
            entity = await client.get_entity(query)
            return entity
        except Exception as e:
            logger.debug(f"Could not find by username: {e}")
        
        # Search through dialogs
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            
            # Check different identifier types
            if hasattr(entity, 'username') and entity.username and entity.username.lower() == query.lower():
                return entity
            elif hasattr(entity, 'phone') and entity.phone and entity.phone == query.replace('+', ''):
                return entity
            elif hasattr(entity, 'first_name'):
                full_name = f"{entity.first_name or ''} {getattr(entity, 'last_name', '') or ''}".strip()
                if full_name.lower() == query.lower():
                    return entity
            elif hasattr(entity, 'title') and entity.title and entity.title.lower() == query.lower():
                return entity
        
        logger.error(f"Could not find conversation for: {query}")
        return None
    
    def create_export_directory(self, entity_name: str) -> Path:
        """Create directory structure for exported data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = Path(f"exports/{entity_name}_{timestamp}")
        
        # Create subdirectories
        (base_dir / "messages").mkdir(parents=True, exist_ok=True)
        (base_dir / "media").mkdir(parents=True, exist_ok=True)
        (base_dir / "voice").mkdir(parents=True, exist_ok=True)
        (base_dir / "documents").mkdir(parents=True, exist_ok=True)
        (base_dir / "photos").mkdir(parents=True, exist_ok=True)
        (base_dir / "videos").mkdir(parents=True, exist_ok=True)
        (base_dir / "stickers").mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Created export directory: {base_dir}")
        return base_dir
    
    def get_entity_name(self, entity: Any) -> str:
        """Get a suitable name for the entity."""
        if isinstance(entity, User):
            name = f"{entity.first_name or ''} {entity.last_name or ''}".strip()
            return name or entity.username or f"user_{entity.id}"
        elif isinstance(entity, (Chat, Channel)):
            return entity.title or f"chat_{entity.id}"
        else:
            return f"entity_{entity.id}"
    
    async def download_media(self, message: Any, export_dir: Path) -> Optional[Dict[str, Any]]:
        """Download media from a message and return file info."""
        if not message.media:
            return None
        
        media_info = {
            "type": "unknown",
            "file_path": None,
            "file_name": None,
            "file_size": None,
            "mime_type": None
        }
        
        try:
            if isinstance(message.media, MessageMediaPhoto):
                media_info["type"] = "photo"
                file_path = export_dir / "photos" / f"photo_{message.id}.jpg"
                
            elif isinstance(message.media, MessageMediaDocument):
                document = message.media.document
                media_info["mime_type"] = getattr(document, 'mime_type', None)
                
                # Determine media type from document attributes
                is_voice = False
                is_audio = False
                is_video = False
                is_sticker = False
                is_animated = False
                filename = f"file_{message.id}"
                
                for attr in document.attributes:
                    if isinstance(attr, DocumentAttributeAudio):
                        if getattr(attr, 'voice', False):
                            is_voice = True
                            media_info["type"] = "voice"
                        else:
                            is_audio = True
                            media_info["type"] = "audio"
                    elif isinstance(attr, DocumentAttributeVideo):
                        is_video = True
                        media_info["type"] = "video"
                    elif isinstance(attr, DocumentAttributeSticker):
                        is_sticker = True
                        media_info["type"] = "sticker"
                    elif isinstance(attr, DocumentAttributeAnimated):
                        is_animated = True
                        if media_info["type"] == "unknown":
                            media_info["type"] = "animated"
                    elif isinstance(attr, DocumentAttributeFilename):
                        if attr.file_name:
                            filename = attr.file_name
                
                # Determine file extension and subdirectory
                if is_voice:
                    ext = "ogg"
                    subdir = "voice"
                    file_path = export_dir / subdir / f"voice_{message.id}.{ext}"
                elif is_audio:
                    ext = "mp3"
                    subdir = "media"
                    file_path = export_dir / subdir / f"audio_{message.id}.{ext}"
                elif is_video:
                    ext = "mp4"
                    subdir = "videos"
                    file_path = export_dir / subdir / f"video_{message.id}.{ext}"
                elif is_sticker:
                    ext = "webp"
                    subdir = "stickers"
                    file_path = export_dir / subdir / f"sticker_{message.id}.{ext}"
                elif is_animated:
                    ext = "gif"
                    subdir = "media"
                    file_path = export_dir / subdir / f"animated_{message.id}.{ext}"
                else:
                    # Regular document
                    media_info["type"] = "document"
                    subdir = "documents"
                    file_path = export_dir / subdir / f"{message.id}_{filename}"
            
            else:
                # Other media types (contacts, locations, etc.)
                media_info["type"] = "other"
                subdir = "media"
                file_path = export_dir / subdir / f"media_{message.id}"
            
            # Download the file
            if 'file_path' in locals():
                logger.info(f"Downloading {media_info['type']}: {file_path.name}")
                client = self._create_client()
                await client.download_media(message.media, str(file_path))
                
                media_info["file_path"] = str(file_path.relative_to(export_dir))
                media_info["file_name"] = file_path.name
                media_info["file_size"] = file_path.stat().st_size if file_path.exists() else None
                
        except Exception as e:
            logger.error(f"Error downloading media for message {message.id}: {e}")
            return None
        
        return media_info
    
    async def export_conversation(self, query: str, limit: Optional[int] = None) -> bool:
        """Export entire conversation with a specific entity."""
        entity = await self.find_conversation(query)
        if not entity:
            return False
        
        entity_name = self.get_entity_name(entity)
        export_dir = self.create_export_directory(entity_name)
        
        logger.info(f"Starting export for: {entity_name}")
        
        messages_data = []
        message_count = 0
        
        try:
            # Get conversation info
            conversation_info = {
                "entity_id": entity.id,
                "entity_name": entity_name,
                "entity_type": type(entity).__name__,
                "export_date": datetime.now().isoformat(),
                "total_messages": 0,
                "messages": []
            }
            
            # Iterate through all messages
            client = self._create_client()
            async for message in client.iter_messages(entity, limit=limit):
                message_count += 1
                
                if message_count % 100 == 0:
                    logger.info(f"Processed {message_count} messages...")
                
                # Basic message info
                message_data = {
                    "id": message.id,
                    "date": message.date.isoformat() if message.date else None,
                    "text": message.text or "",
                    "sender_id": message.sender_id,
                    "is_outgoing": message.out,
                    "reply_to": message.reply_to_msg_id,
                    "forward_from": None,
                    "media": None
                }
                
                # Handle forwarded messages
                if message.forward:
                    message_data["forward_from"] = {
                        "date": message.forward.date.isoformat() if message.forward.date else None,
                        "from_id": getattr(message.forward, 'from_id', None),
                        "from_name": getattr(message.forward, 'from_name', None)
                    }
                
                # Download and record media
                media_info = await self.download_media(message, export_dir)
                if media_info:
                    message_data["media"] = media_info
                
                messages_data.append(message_data)
            
            # Update conversation info
            conversation_info["total_messages"] = message_count
            conversation_info["messages"] = messages_data
            
            # Save messages data to JSON
            messages_file = export_dir / "conversation.json"
            async with aiofiles.open(messages_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(conversation_info, indent=2, ensure_ascii=False))
            
            # Create a readable text version
            text_file = export_dir / "conversation.txt"
            async with aiofiles.open(text_file, 'w', encoding='utf-8') as f:
                await f.write(f"Conversation with: {entity_name}\n")
                await f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                await f.write(f"Total messages: {message_count}\n")
                await f.write("-" * 50 + "\n\n")
                
                for msg in reversed(messages_data):  # Show chronological order
                    date_str = datetime.fromisoformat(msg['date']).strftime('%Y-%m-%d %H:%M:%S') if msg['date'] else 'Unknown'
                    sender = "You" if msg['is_outgoing'] else entity_name
                    
                    await f.write(f"[{date_str}] {sender}: {msg['text']}\n")
                    
                    if msg['media']:
                        await f.write(f"    📎 Media: {msg['media']['type']} - {msg['media']['file_name']}\n")
                    
                    if msg['reply_to']:
                        await f.write(f"    ↩️ Reply to message ID: {msg['reply_to']}\n")
                    
                    await f.write("\n")
            
            logger.info(f"Export completed! {message_count} messages exported to {export_dir}")
            logger.info(f"Files saved:")
            logger.info(f"  - conversation.json: Complete data in JSON format")
            logger.info(f"  - conversation.txt: Human-readable text format")
            logger.info(f"  - media/: Downloaded attachments organized by type")
            
            return True
            
        except Exception as e:
            logger.error(f"Error during export: {e}")
            return False


async def main():
    """Main function to run the exporter."""
    print("Telegram Conversation Exporter")
    print("=" * 40)
    
    exporter = TelegramExporter()
    
    try:
        await exporter.connect()
        
        # Get target conversation
        query = input("Enter username, phone number, or name to export: ").strip()
        if not query:
            print("No target specified. Exiting.")
            return
        
        # Optional: set message limit
        limit_input = input("Enter message limit (press Enter for all messages): ").strip()
        limit = int(limit_input) if limit_input.isdigit() else None
        
        # Start export
        success = await exporter.export_conversation(query, limit)
        
        if success:
            print("\n✅ Export completed successfully!")
        else:
            print("\n❌ Export failed. Check logs for details.")
            
    except KeyboardInterrupt:
        print("\n⏹️  Export interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        await exporter.disconnect()


if __name__ == "__main__":
    asyncio.run(main())