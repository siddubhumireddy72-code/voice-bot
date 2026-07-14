#!/bin/bash

# Voice Bot Setup Script
# This script sets up the Voice Bot environment

echo "🤖 Voice Bot Setup Script"
echo "==========================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🗄️  Setting up database..."
python3 -c "from database.db import init_db; init_db()"

echo "📝 Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env with your configuration"
fi

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env with your OpenAI API key and Asterisk settings"
echo "2. Run: python3 app.py"
echo "3. Access dashboard at: http://localhost:5000"
echo ""
