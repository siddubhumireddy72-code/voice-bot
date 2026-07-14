# Voice Bot - Complete Setup Guide

## 📚 Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Asterisk Setup](#asterisk-setup)
6. [Running the Bot](#running-the-bot)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

---

## Overview

Voice Bot is a Python-based intelligent voice assistant that:
- Receives incoming phone calls via Asterisk VOIP
- Converts speech to text using OpenAI Whisper API
- Processes user intent with GPT-3.5-turbo/GPT-4
- Converts responses to speech using gTTS
- Logs all calls and transcripts
- Provides a web dashboard for monitoring

---

## System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 18.04+) or macOS
- **Python**: 3.9 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 5GB for logs and recordings
- **Network**: Internet connection (for OpenAI API)

### Required Services
- **Asterisk**: 16 or higher (for VOIP)
- **PostgreSQL**: 12 or higher (optional, SQLite works for testing)
- **OpenAI API Key**: Get from https://platform.openai.com/api-keys

---

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/voice-bot.git
cd voice-bot
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
```bash
cp .env.example .env
# Edit .env with your settings
```

### Step 5: Initialize Database
```bash
python3 -c "from database.db import init_db; init_db()"
```

---

## Configuration

### .env File Configuration

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4

# Asterisk Configuration
ASTERISK_HOST=localhost
ASTERISK_PORT=5060
ASTERISK_USER=admin
ASTERISK_PASSWORD=your-asterisk-password
ASTERISK_CONTEXT=from-internal

# Database Configuration
DATABASE_URL=sqlite:///voice_bot.db
# For PostgreSQL: postgresql://user:password@localhost/voice_bot

# Flask Configuration
FLASK_ENV=development  # or production
FLASK_SECRET_KEY=your-secret-key-here
DEBUG=True  # Set to False in production

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=5000

# Speech Configuration
SPEECH_LANGUAGE=en-US
SPEECH_RATE=1.0
SPEECH_VOLUME=1.0

# Call Configuration
DEFAULT_GREETING=Hello! You have reached the voice bot. How can I help you?
DEFAULT_MAX_CALL_DURATION=300
DEFAULT_SILENCE_TIMEOUT=10
```

---

## Asterisk Setup

### Install Asterisk on Ubuntu

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    libssl-dev \
    libncurses5-dev \
    uuid-dev \
    sqlite3 \
    libsqlite3-dev

# Download Asterisk (latest LTS)
cd /tmp
wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-20-current.tar.gz
tar -xzf asterisk-20-current.tar.gz
cd asterisk-20.*/

# Build and Install
./configure
make menuselect
make
sudo make install
sudo make config

# Start Asterisk
sudo systemctl start asterisk
sudo systemctl enable asterisk

# Verify installation
asterisk -rvv
```

### Configure Asterisk

1. Copy configuration files:
```bash
sudo cp asterisk_config/extensions.conf /etc/asterisk/
sudo cp asterisk_config/pjsip.conf /etc/asterisk/
```

2. Restart Asterisk:
```bash
sudo asterisk -rvv
cli> reload
```

---

## Running the Bot

### Option 1: Direct Python Execution

```bash
# Activate virtual environment
source venv/bin/activate

# Run application
python3 app.py

# Access dashboard at: http://localhost:5000
```

### Option 2: Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### Option 3: Using Docker

```bash
# Build Docker image
docker build -t voice-bot .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

---

## API Reference

### Health Check
```
GET /api/health

Response:
{
  "status": "healthy",
  "message": "Voice Bot is running"
}
```

### Get All Calls
```
GET /api/calls

Response:
{
  "status": "success",
  "calls": [
    {
      "id": 1,
      "caller_number": "+1234567890",
      "duration": 120,
      "status": "answered",
      "transcript": "...",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

### Get Call Details
```
GET /api/calls/<id>

Response:
{
  "status": "success",
  "call": { ... }
}
```

### Process Speech
```
POST /api/process_speech

Request Body:
{
  "text": "User input text",
  "call_id": 1
}

Response:
{
  "status": "success",
  "response": "Bot response text",
  "call_id": 1
}
```

### Get Statistics
```
GET /api/stats

Response:
{
  "status": "success",
  "stats": {
    "total_calls": 150,
    "answered_calls": 145,
    "missed_calls": 5
  }
}
```

### Webhook: Incoming Call
```
POST /webhook/call

Request Body:
{
  "from": "+1234567890",
  "to": "+0987654321",
  "channel": "SIP/2000-00000001"
}

Response:
{
  "status": "success",
  "message": "Call received and processing",
  "result": { ... }
}
```

---

## Call Flow Diagram

```
Incoming Call
     |
     v
Asterisk Receives Call
     |
     v
Webhook Triggered → Flask App
     |
     v
Answer Call & Play Greeting (TTS)
     |
     v
Record User Speech
     |
     v
Convert Speech to Text (Whisper API)
     |
     v
Send to OpenAI (GPT-3.5/4)
     |
     v
Get Bot Response
     |
     v
Convert Response to Speech (gTTS)
     |
     v
Play Response to User
     |
     v
Wait for User Input (or End Call)
     |
     v
Save Call Log to Database
     |
     v
End Call
```

---

## Troubleshooting

### Issue: Asterisk Not Connecting

**Solution:**
```bash
# Check if Asterisk is running
sudo systemctl status asterisk

# Check if port 5060 is open
sudo netstat -tuln | grep 5060

# Verify configuration
sudo asterisk -rvv
cli> sip show peers

# Check logs
sudo tail -f /var/log/asterisk/messages
```

### Issue: OpenAI API Errors

**Solution:**
- Verify API key is correct
- Check account balance at https://platform.openai.com/account/usage/overview
- Ensure API key has necessary permissions
- Check rate limits

### Issue: Audio Not Working

**Solution:**
```bash
# Check audio devices
arecord -l
aplay -l

# Install missing packages
sudo apt-get install alsa-utils pulseaudio

# Test audio
aplay /usr/share/sounds/alsa/Noise.wav
```

### Issue: Database Connection Error

**Solution:**
```bash
# Reset database
python3 -c "from database.db import reset_db; reset_db()"

# Check database file
ls -la voice_bot.db

# For PostgreSQL, verify connection
psql -h localhost -U voicebot -d voicebot
```

### Issue: High CPU Usage

**Solution:**
- Reduce number of worker processes in Gunicorn
- Check for infinite loops in code
- Monitor active calls
- Use profiling tools

---

## Logging

Logs are stored in the `logs/` directory:

```bash
# View application logs
tail -f logs/app.log

# View call logs
tail -f logs/calls.log

# View error logs
tail -f logs/error.log
```

---

## Performance Optimization

1. **Database Optimization**
   - Add indexes to frequently queried columns
   - Archive old call logs regularly

2. **Caching**
   - Cache common bot responses
   - Use Redis for session management

3. **Asterisk Tuning**
   - Adjust buffer sizes
   - Optimize codec settings

4. **API Rate Limiting**
   - Implement rate limiting for API endpoints
   - Monitor OpenAI API usage

---

## Security Best Practices

1. **Environment Variables**
   - Never commit .env file
   - Use strong secret keys
   - Rotate API keys regularly

2. **Database Security**
   - Use strong passwords
   - Enable SSL for PostgreSQL
   - Regular backups

3. **API Security**
   - Use HTTPS in production
   - Implement authentication
   - Rate limiting
   - Input validation

4. **Asterisk Security**
   - Change default credentials
   - Restrict SIP access
   - Enable firewall rules

---

## Additional Resources

- [Asterisk Documentation](https://www.asterisk.org/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- [WebRTC](https://webrtc.org/)

---

## Support & Community

- 📧 Email: support@voicebot.local
- 🐛 GitHub Issues: https://github.com/yourusername/voice-bot/issues
- 💬 Discussions: https://github.com/yourusername/voice-bot/discussions
- 📖 Wiki: https://github.com/yourusername/voice-bot/wiki

---

**Last Updated**: January 2024
**Version**: 1.0.0
