#!/bin/bash

# Audio to SRT Converter Setup Script
# This script sets up the environment and installs required dependencies

echo "🎵 Audio to SRT Converter Setup"
echo "================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "📥 Installing required packages..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Usage:"
echo "1. Activate the environment: source venv/bin/activate"
echo "2. Run the converter: python3 audio_to_srt.py your_audio.mp3"
echo ""
echo "💡 Example: python3 audio_to_srt.py example.mp3 -o subtitles.srt"
