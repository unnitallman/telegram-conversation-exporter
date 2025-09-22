# Telegram Conversation Exporter

A Python script that exports all messages from a specific Telegram conversation, including text messages, media files, voice messages, and other attachments.

## Features

- **Complete message export**: Downloads all text messages with timestamps
- **Media download**: Automatically downloads and organizes:
  - Photos
  - Voice messages
  - Audio files
  - Videos
  - Documents
  - Stickers
- **Multiple output formats**: 
  - JSON format for programmatic access
  - Human-readable text format
- **Smart conversation search**: Find conversations by username, phone number, or display name
- **Organized file structure**: Media files are organized into separate folders by type

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Telegram API Credentials

1. Go to [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your phone number
3. Create a new application
4. Note down your `API ID` and `API Hash`

### 3. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your credentials:
   ```env
   API_ID=your_api_id_here
   API_HASH=your_api_hash_here
   PHONE_NUMBER=+1234567890
   SESSION_NAME=telegram_session
   ```

## Usage

Run the script:

```bash
python telegram_exporter.py
```

The script will:

1. **Authenticate**: First-time users will receive an SMS with a verification code
2. **Search**: Enter the username, phone number, or display name of the person/chat
3. **Export**: Choose to export all messages or set a limit
4. **Download**: The script will download all messages and media files

### Example Usage

```
$ python telegram_exporter.py
Telegram Conversation Exporter
========================================
Enter username, phone number, or name to export: @username
Enter message limit (press Enter for all messages): 
```

## Output Structure

After export, you'll find a new directory under `exports/` with the following structure:

```
exports/
└── PersonName_20241222_143052/
    ├── conversation.json          # Complete data in JSON format
    ├── conversation.txt          # Human-readable text format
    ├── photos/                   # Downloaded photos
    ├── voice/                    # Voice messages
    ├── videos/                   # Video files
    ├── documents/                # Documents and files
    ├── stickers/                 # Sticker files
    └── media/                    # Other media files
```

## File Formats

### conversation.json
Contains complete conversation data including:
- Message metadata (ID, timestamp, sender)
- Media file references
- Forward information
- Reply references

### conversation.txt
Human-readable format showing:
- Chronological message order
- Sender identification
- Media attachments noted
- Reply chains indicated

## Authentication

The script uses Telethon which creates a session file (`telegram_session.session`) after first authentication. This file allows future runs without re-authentication.

**Security Note**: Keep your session file secure as it provides access to your Telegram account.

## Limitations

- **Rate limits**: Telegram has API rate limits. Large exports may take time
- **Private groups**: You can only export conversations you're a member of
- **Deleted messages**: Cannot export messages that have been deleted
- **Secret chats**: Secret chats cannot be exported via the API

## Troubleshooting

### "Could not find conversation"
- Try different search terms (username, phone, display name)
- Ensure you have an active conversation with the person/group
- Check that the username is spelled correctly (include @ if searching by username)

### Authentication errors
- Verify your API credentials in the `.env` file
- Ensure your phone number includes the country code
- Delete the session file and re-authenticate if needed

### Download failures
- Check your internet connection
- Some media files may have been deleted from Telegram servers
- Large files may timeout - the script will continue with other messages

## Privacy and Legal Considerations

- Only export conversations you have permission to export
- Respect privacy rights and local laws
- Exported data contains sensitive personal information - handle appropriately
- Consider informing conversation participants before exporting shared conversations

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source. Please use responsibly and in accordance with Telegram's Terms of Service.