# Installation Guide

## Desktop Application (Recommended)

### macOS

1. Download the latest `.dmg` file from [Releases](https://github.com/harshpreet931/audioToSRT/releases)
2. Open the `.dmg` file
3. Drag Audio to SRT to your Applications folder
4. Launch from Applications

**Note:** You may need to allow the app in System Preferences > Security & Privacy if you see a warning about an unidentified developer.

### Windows

1. Download the latest `.msi` installer from [Releases](https://github.com/harshpreet931/audioToSRT/releases)
2. Run the installer
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

### Linux

#### AppImage (Universal)
1. Download the `.AppImage` file from [Releases](https://github.com/harshpreet931/audioToSRT/releases)
2. Make it executable: `chmod +x audio-to-srt-app_*.AppImage`
3. Run: `./audio-to-srt-app_*.AppImage`

#### Debian/Ubuntu (.deb)
1. Download the `.deb` file from [Releases](https://github.com/harshpreet931/audioToSRT/releases)
2. Install: `sudo dpkg -i audio-to-srt-app_*.deb`
3. Launch from Applications menu

## Development Setup

### Prerequisites

- **Node.js 18+** - [Download](https://nodejs.org/)
- **Rust 1.70+** - [Install](https://rustup.rs/)
- **Python 3.7+** - [Download](https://python.org/)
- **FFmpeg** - See platform-specific instructions below

### FFmpeg Installation

#### macOS
```bash
# Using Homebrew
brew install ffmpeg
```

#### Windows
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

### Clone and Setup

```bash
# Clone repository
git clone https://github.com/harshpreet931/audioToSRT.git
cd audioToSRT

# Setup Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup Tauri application
cd audio-to-srt-app
npm install

# Start development server
npm run tauri dev
```

### Building from Source

```bash
# Build optimized application
npm run tauri build

# Outputs will be in src-tauri/target/release/bundle/
```

## Command Line Usage

### Direct Python Script

```bash
# Basic usage
python3 audio_to_srt.py your_audio.mp3

# With custom settings
python3 audio_to_srt.py your_audio.mp3 --model base --max-chars 50 --max-duration 5.0

# Batch processing
python3 batch_convert.py /path/to/audio/files/
```

### Available Options

```bash
python3 audio_to_srt.py --help

Options:
  -m, --model TEXT          Whisper model size [tiny, base, small, medium, large]
  --max-chars INTEGER       Maximum characters per subtitle line (default: 50)
  --max-duration FLOAT      Maximum duration per subtitle in seconds (default: 5.0)
  --output-dir TEXT         Output directory for SRT files
  --help                    Show this message and exit
```

## Troubleshooting

### Common Issues

**"FFmpeg not found"**
- Ensure FFmpeg is installed and in your PATH
- Try restarting your terminal/command prompt after installation

**"Python module not found"**
- Make sure you've activated your virtual environment
- Run `pip install -r requirements.txt` again

**"Permission denied" on macOS**
- Go to System Preferences > Security & Privacy
- Click "Open Anyway" for Audio to SRT

**"CUDA out of memory"**
- Use a smaller model (tiny or base)
- Close other GPU-intensive applications
- Process shorter audio files

**Slow processing**
- Use a smaller Whisper model
- Ensure your system has sufficient RAM
- Close unnecessary applications

### Performance Tips

- **Model Selection**: Use 'base' for best speed/quality balance
- **File Format**: MP3 and M4A process fastest
- **File Size**: Smaller files process faster
- **System Resources**: Close other applications during processing

### Getting Help

- **Documentation**: [Wiki](https://github.com/harshpreet931/audioToSRT/wiki)
- **Bug Reports**: [GitHub Issues](https://github.com/harshpreet931/audioToSRT/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/harshpreet931/audioToSRT/discussions)

## System Requirements

### Minimum Requirements
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **OS**: macOS 10.15+, Windows 10+, or Linux (64-bit)

### Recommended Requirements
- **RAM**: 8GB+ (for faster processing)
- **Storage**: 5GB+ free space (for larger models)
- **CPU**: Multi-core processor
- **GPU**: CUDA-compatible GPU (optional, for acceleration)