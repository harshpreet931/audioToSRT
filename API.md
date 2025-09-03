# API Documentation

## Python API

### AudioToSRT Class

The core class for audio-to-subtitle conversion.

```python
from audio_to_srt import AudioToSRT

# Initialize with model
converter = AudioToSRT(model_size="base")

# Convert audio to SRT
converter.convert_mp3_to_srt(
    mp3_path="audio.mp3",
    output_path="subtitles.srt",
    max_chars_per_line=50,
    max_duration=5.0
)
```

#### Constructor

```python
AudioToSRT(model_size="base")
```

**Parameters:**
- `model_size` (str): Whisper model size
  - Options: `"tiny"`, `"base"`, `"small"`, `"medium"`, `"large"`
  - Default: `"base"`

#### Methods

##### convert_mp3_to_srt()

```python
convert_mp3_to_srt(
    mp3_path: str,
    output_path: str = None,
    max_chars_per_line: int = 50,
    max_duration: float = 5.0
) -> str
```

Converts audio file to SRT subtitles.

**Parameters:**
- `mp3_path` (str): Path to input audio file
- `output_path` (str, optional): Output SRT file path. If None, uses input path with .srt extension
- `max_chars_per_line` (int): Maximum characters per subtitle line (default: 50)
- `max_duration` (float): Maximum duration per subtitle segment in seconds (default: 5.0)

**Returns:**
- `str`: Path to generated SRT file

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `Exception`: If conversion fails

**Example:**
```python
converter = AudioToSRT(model_size="base")
srt_path = converter.convert_mp3_to_srt(
    mp3_path="podcast.mp3",
    max_chars_per_line=60,
    max_duration=4.0
)
print(f"SRT file created: {srt_path}")
```

### Batch Processing

```python
from batch_convert import batch_convert

batch_convert(
    input_dir="/path/to/audio/files",
    output_dir="/path/to/srt/files",
    model_size="base",
    max_chars_per_line=50,
    max_duration=5.0
)
```

**Parameters:**
- `input_dir` (str): Directory containing MP3 files
- `output_dir` (str, optional): Output directory for SRT files
- `model_size` (str): Whisper model size (default: "base")
- `max_chars_per_line` (int): Max characters per line (default: 50)
- `max_duration` (float): Max duration per segment (default: 5.0)

## Tauri API

### Frontend Commands

The Tauri application exposes these commands to the frontend:

#### convert_audio_to_srt

```typescript
import { invoke } from '@tauri-apps/api/core';

const result = await invoke('convert_audio_to_srt', {
  filePath: '/path/to/audio.mp3',
  modelSize: 'base',
  maxChars: 50,
  maxDuration: 5.0
});
```

**Parameters:**
- `filePath` (string): Full path to audio file
- `modelSize` (string): Whisper model size
- `maxChars` (number): Maximum characters per subtitle line
- `maxDuration` (number): Maximum duration per subtitle segment

**Returns:**
- `Promise<string>`: Path to generated SRT file

**Example:**
```typescript
try {
  const srtPath = await invoke('convert_audio_to_srt', {
    filePath: selectedFile.path,
    modelSize: 'base',
    maxChars: 50,
    maxDuration: 5.0
  });
  console.log('Conversion complete:', srtPath);
} catch (error) {
  console.error('Conversion failed:', error);
}
```

#### reveal_in_finder

```typescript
import { invoke } from '@tauri-apps/api/core';

await invoke('reveal_in_finder', {
  path: '/path/to/file.srt'
});
```

**Parameters:**
- `path` (string): Full path to file to reveal

**Returns:**
- `Promise<void>`

**Example:**
```typescript
// Show generated SRT file in file manager
await invoke('reveal_in_finder', {
  path: outputPath
});
```

### File Dialog API

```typescript
import { open } from '@tauri-apps/plugin-dialog';

const selected = await open({
  multiple: true,
  filters: [{
    name: 'Audio Files',
    extensions: ['mp3', 'wav', 'm4a', 'flac', 'ogg']
  }]
});
```

## Error Handling

### Python Errors

```python
try:
    converter = AudioToSRT(model_size="base")
    srt_path = converter.convert_mp3_to_srt("audio.mp3")
except FileNotFoundError:
    print("Audio file not found")
except Exception as e:
    print(f"Conversion failed: {e}")
```

### TypeScript Errors

```typescript
try {
  const result = await invoke('convert_audio_to_srt', params);
  // Handle success
} catch (error) {
  if (error.includes('FileNotFound')) {
    // Handle missing file
  } else if (error.includes('FFmpeg')) {
    // Handle FFmpeg errors
  } else {
    // Handle other errors
  }
}
```

## Model Specifications

| Model | Parameters | Size | Speed | Accuracy | VRAM Usage |
|-------|------------|------|-------|----------|------------|
| tiny | 39M | 39 MB | Very Fast | Good | ~1 GB |
| base | 74M | 142 MB | Fast | Better | ~1 GB |
| small | 244M | 461 MB | Medium | Good | ~2 GB |
| medium | 769M | 1.5 GB | Slow | Better | ~5 GB |
| large | 1550M | 3.0 GB | Slowest | Best | ~10 GB |

## Supported Audio Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| MP3 | .mp3 | Most common, fast processing |
| WAV | .wav | Uncompressed, highest quality |
| M4A | .m4a | Apple format, good quality |
| FLAC | .flac | Lossless compression |
| OGG | .ogg | Open source format |

## SRT Format

Generated SRT files follow the standard format:

```
1
00:00:00,000 --> 00:00:04,000
First subtitle line

2
00:00:04,000 --> 00:00:08,000
Second subtitle line
```

### Timing Rules

- Segments respect `max_duration` parameter
- Overlapping segments are automatically adjusted
- Minimum segment duration: 0.5 seconds
- Maximum gap between segments: 1.0 second

### Text Formatting

- Lines are broken at `max_chars_per_line`
- Word boundaries are preserved
- Punctuation is maintained
- Multiple speakers are not separated

## Integration Examples

### DaVinci Resolve

```python
# Generate subtitles optimized for video editing
converter = AudioToSRT(model_size="base")
srt_path = converter.convert_mp3_to_srt(
    "video_audio.wav",
    max_chars_per_line=40,  # Shorter lines for video
    max_duration=3.0        # Shorter segments
)
```

### Podcast Workflow

```python
# Batch process podcast episodes
from pathlib import Path

episodes = Path("podcast_episodes").glob("*.mp3")
for episode in episodes:
    converter.convert_mp3_to_srt(
        str(episode),
        max_chars_per_line=80,  # Longer lines for reading
        max_duration=10.0       # Longer segments
    )
```

### Web Application Integration

```typescript
// Handle file upload and conversion
const handleFileUpload = async (file: File) => {
  const tempPath = await saveTempFile(file);
  
  try {
    const srtPath = await invoke('convert_audio_to_srt', {
      filePath: tempPath,
      modelSize: 'base',
      maxChars: 50,
      maxDuration: 5.0
    });
    
    // Download or display SRT content
    const srtContent = await readSrtFile(srtPath);
    return srtContent;
  } finally {
    // Clean up temp file
    await deleteTempFile(tempPath);
  }
};
```