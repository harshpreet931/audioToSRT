# Audio to SRT Converter

Convert MP3 audio files to SRT subtitle files using AI-powered speech recognition. Perfect for creating subtitles that work seamlessly with DaVinci Resolve.

## Features

- 🎯 **Perfect DaVinci Resolve Compatibility**: Generates SRT files that import flawlessly
- 🧠 **AI-Powered Transcription**: Uses OpenAI Whisper for accurate speech-to-text
- ⚡ **Multiple Model Sizes**: Choose from tiny to large models based on accuracy needs
- 📝 **Smart Text Formatting**: Automatically splits long lines and segments
- 🎛️ **Customizable Parameters**: Control subtitle length and duration
- 📁 **Simple Usage**: Command-line interface with sensible defaults

## Installation

1. **Clone or download this project**
2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

This will create a virtual environment and install all required dependencies.

## Usage

### Basic Usage
```bash
# Activate the virtual environment
source venv/bin/activate

# Convert MP3 to SRT
python3 audio_to_srt.py your_audio.mp3
```

### Advanced Usage
```bash
# Specify output file
python3 audio_to_srt.py input.mp3 -o custom_subtitles.srt

# Use a larger model for better accuracy
python3 audio_to_srt.py input.mp3 --model large

# Customize subtitle formatting
python3 audio_to_srt.py input.mp3 --max-chars 40 --max-duration 3.0
```

### Command Line Options

- `input`: Path to the MP3 file (required)
- `-o, --output`: Output SRT file path (optional, defaults to same name as input)
- `-m, --model`: Whisper model size - `tiny`, `base`, `small`, `medium`, `large` (default: `base`)
- `--max-chars`: Maximum characters per subtitle line (default: 50)
- `--max-duration`: Maximum duration per subtitle in seconds (default: 5.0)

## Model Sizes

| Model  | Size    | Speed | Accuracy | Best For |
|--------|---------|-------|----------|----------|
| tiny   | ~39 MB  | Fast  | Good     | Quick tests |
| base   | ~142 MB | Fast  | Better   | Most use cases |
| small  | ~461 MB | Medium| Good     | Better accuracy |
| medium | ~1.5 GB | Slow  | Better   | High accuracy |
| large  | ~3.0 GB | Slowest| Best    | Maximum accuracy |

## Using with DaVinci Resolve

1. **Import your video** into DaVinci Resolve
2. **Generate subtitles** using this tool:
   ```bash
   python3 audio_to_srt.py your_video_audio.mp3
   ```
3. **In DaVinci Resolve**:
   - Right-click on your video in the Media Pool
   - Select "Import Subtitle"
   - Choose the generated `.srt` file
   - The subtitles will be automatically synced!

## Requirements

- Python 3.7+
- FFmpeg (for audio processing)
- Internet connection (for first-time model download)

### Installing FFmpeg on macOS
```bash
# Using Homebrew
brew install ffmpeg

# Using MacPorts
sudo port install ffmpeg
```

## Example Output

Input: `podcast.mp3`
Output: `podcast.srt`

```srt
1
00:00:00,000 --> 00:00:03,500
Welcome to our podcast about technology

2
00:00:03,500 --> 00:00:07,200
Today we'll be discussing artificial intelligence

3
00:00:07,200 --> 00:00:11,800
And how it's changing the way we work and live
```

## Troubleshooting

### Common Issues

1. **"FFmpeg not found"**
   - Install FFmpeg using the instructions above

2. **"Model download failed"**
   - Check your internet connection
   - The model will be downloaded on first use

3. **"Poor transcription quality"**
   - Try a larger model size (`--model large`)
   - Ensure audio quality is good
   - Check that the audio is in a supported language

4. **"Subtitles out of sync in DaVinci Resolve"**
   - Ensure your video and audio files have the same duration
   - Check that the frame rate matches your project settings

### Performance Tips

- Use `base` model for fastest processing with good quality
- Use `large` model for best accuracy (but slower processing)
- Process shorter audio files in batches for better memory usage

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!
