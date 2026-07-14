# Voice Bot - Python + OpenAI + Asterisk

A voice bot project that handles incoming calls, converts speech to text, processes with OpenAI, and responds with natural speech synthesis.

## Features

- 🎙️ Free VOIP using Asterisk
- 🤖 OpenAI GPT integration for intelligent responses
- 🔊 Speech-to-Text (OpenAI Whisper)
- 📢 Text-to-Speech synthesis
- 📊 Web Dashboard to monitor calls
- 📝 Call logs and transcript storage
- 🔄 Real-time call handling

## Tech Stack

- **Backend**: Python 3.9+
- **VOIP**: Asterisk (free, self-hosted)
- **AI**: OpenAI API (GPT-3.5-turbo/GPT-4)
- **Speech**: OpenAI Whisper (STT), gTTS (TTS)
- **Web Framework**: Flask
- **Database**: SQLite / PostgreSQL
- **Frontend**: Flask + Bootstrap

## Project Structure

```
voice-bot/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
│
├── call_handler/             # Call handling
│   ├── __init__.py
│   ├── asterisk_handler.py   # Asterisk integration
│   ├── call_manager.py       # Call state management
│   └── webhook.py            # Webhook handlers
│
├── ai_engine/                # AI & NLU
│   ├── __init__.py
│   ├── openai_client.py      # OpenAI integration
│   └── conversation.py       # Conversation logic
│
├── speech/                   # Speech processing
│   ├── __init__.py
│   ├── stt.py                # Speech-to-Text
│   └── tts.py                # Text-to-Speech
│
├── database/                 # Database
│   ├── __init__.py
│   ├── models.py             # SQLAlchemy models
│   └── db.py                 # DB initialization
│
├── dashboard/                # Web Dashboard
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── calls.html
│   │   └── settings.html
│   └── static/
│       ├── css/style.css
│       └── js/dashboard.js
│
└── logs/                     # Application logs
```

## Quick Start

### Prerequisites
- Python 3.9+
- Asterisk 16+ (for VOIP)
- OpenAI API Key
- PostgreSQL or SQLite

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/voice-bot.git
cd voice-bot
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Environment**
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and Asterisk config
```

5. **Initialize Database**
```bash
python -c "from database.db import init_db; init_db()"
```

6. **Run Application**
```bash
python app.py
```

Access dashboard: `http://localhost:5000`

## Configuration

Edit `.env` file:
```
OPENAI_API_KEY=your_key_here
ASTERISK_HOST=localhost
ASTERISK_PORT=5060
ASTERISK_USER=admin
ASTERISK_PASSWORD=password
DATABASE_URL=sqlite:///voice_bot.db
FLASK_SECRET_KEY=your_secret_key
```

## Call Flow

1. Incoming Call → Asterisk receives
2. Webhook Trigger → Flask app receives event
3. Initial Greeting → TTS plays welcome
4. Voice Recording → User speaks
5. Speech-to-Text → Convert speech to text
6. OpenAI Processing → Get bot response
7. Text-to-Speech → Convert to audio
8. Play Response → User hears response
9. Loop or End → Continue or hang up
10. Log Call → Save to database

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/webhook/call` | Incoming call webhook |
| POST | `/api/process_speech` | Process speech input |
| GET | `/api/calls` | Get all calls |
| GET | `/api/calls/<id>` | Get call details |
| GET | `/api/stats` | Get statistics |
| GET | `/dashboard` | View dashboard |

## Asterisk Setup

```bash
# Install Asterisk
sudo apt-get install asterisk

# Start service
sudo systemctl start asterisk

# Check status
sudo asterisk -rvv
```

## OpenAI API

1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env` file
3. Ensure you have credits

## Deployment

### Docker
```bash
docker-compose up -d
```

### Manual
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## License

MIT License

## Support

For issues: Create GitHub issue or contact support
