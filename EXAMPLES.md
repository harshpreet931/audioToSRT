# Usage Examples

## Desktop Application Examples

### Basic Audio Conversion

1. **Launch** Audio to SRT
2. **Drag** your audio file into the application window
3. **Wait** for processing to complete
4. **Click "Show"** to reveal the generated SRT file

**Typical workflow for content creators:**
- Record podcast episode as MP3
- Drop into Audio to SRT  
- Import SRT into video editing software
- Sync with video timeline

### Batch Processing Multiple Files

1. **Select multiple files** using the browse button
2. **Files process sequentially** in the queue
3. **Each completion** shows a "Show" button
4. **Click "Clear"** to remove completed jobs

**Perfect for:**
- Podcast series with multiple episodes
- Course content with multiple lessons
- Conference recordings

### Model Selection Guide

**Tiny Model** - Ultra-fast processing
```
Best for: Quick previews, draft transcriptions
Speed: ~10x faster than real-time
Accuracy: 85-90% for clear speech
Use case: Rapid content review
```

**Base Model** - Balanced performance (Recommended)
```
Best for: Most production work
Speed: ~3x faster than real-time  
Accuracy: 92-95% for clear speech
Use case: YouTube videos, podcasts
```

**Large Model** - Maximum accuracy
```
Best for: Professional subtitles
Speed: Real-time or slower
Accuracy: 96-98% for clear speech
Use case: Film, broadcast, accessibility
```

## Command Line Examples

### Single File Conversion

```bash
# Basic conversion
python3 audio_to_srt.py podcast_episode.mp3

# Custom settings
python3 audio_to_srt.py interview.wav --model large --max-chars 40

# Specify output location
python3 audio_to_srt.py lecture.m4a --output-dir ./subtitles/
```

### Batch Processing

```bash
# Process all MP3 files in directory
python3 batch_convert.py ./audio_files/

# With custom output directory
python3 batch_convert.py ./podcast_episodes/ -o ./subtitles/

# High accuracy batch processing
python3 batch_convert.py ./interviews/ --model large --max-chars 60
```

### Advanced Options

```bash
# Short segments for social media
python3 audio_to_srt.py tiktok_audio.mp3 --max-duration 2.0 --max-chars 30

# Long segments for podcasts
python3 audio_to_srt.py podcast.mp3 --max-duration 8.0 --max-chars 100

# Multiple models comparison
python3 audio_to_srt.py test.mp3 --model tiny
python3 audio_to_srt.py test.mp3 --model base  
python3 audio_to_srt.py test.mp3 --model large
```

## Real-World Use Cases

### Content Creator Workflow

**YouTube Video Production:**
```bash
# 1. Extract audio from video
ffmpeg -i video.mp4 -vn -acodec copy audio.m4a

# 2. Generate subtitles
python3 audio_to_srt.py audio.m4a --model base --max-chars 40

# 3. Import SRT into video editor
# 4. Adjust timing if needed
# 5. Export final video with burned-in subtitles
```

**Podcast Distribution:**
```bash
# Process entire podcast series
python3 batch_convert.py ./podcast_episodes/ -o ./transcripts/ --model base

# Each episode gets its own SRT file for:
# - Podcast platforms with transcript support
# - Blog post transcriptions  
# - Accessibility compliance
```

### Educational Content

**Online Course Creation:**
```bash
# Process lecture recordings
for file in lectures/*.mp4; do
    # Extract audio
    ffmpeg -i "$file" -vn audio.wav
    
    # Generate subtitles
    python3 audio_to_srt.py audio.wav --model base --max-chars 50
    
    # Clean up
    rm audio.wav
done
```

**Student Note-Taking:**
```bash
# Quick lecture transcription
python3 audio_to_srt.py lecture_recording.m4a --model tiny

# Review and edit the generated SRT file
# Convert SRT to plain text for notes
```

### Professional Video Production

**Documentary Workflow:**
```bash
# High-accuracy transcription for subtitles
python3 audio_to_srt.py interview_audio.wav --model large --max-chars 35 --max-duration 4.0

# Output optimized for broadcast standards
# Manual review and timing adjustment
# Professional subtitle formatting
```

**Corporate Training Videos:**
```bash
# Batch process training modules
python3 batch_convert.py ./training_audio/ --model medium --max-chars 45

# Consistent formatting across all modules
# Accessibility compliance
# Multi-language support (future feature)
```

### DaVinci Resolve Integration

**Step-by-step workflow:**

1. **Export audio** from DaVinci Resolve timeline:
   ```
   Deliver Page > Audio Only > WAV format
   ```

2. **Generate subtitles**:
   ```bash
   python3 audio_to_srt.py exported_audio.wav --model base --max-chars 40 --max-duration 4.0
   ```

3. **Import back to DaVinci Resolve**:
   ```
   Media Pool > Right-click > Import > Select SRT file
   ```

4. **Add to timeline**:
   ```
   Drag SRT from Media Pool to video track
   Subtitles automatically sync to audio
   ```

5. **Customize appearance**:
   ```
   Inspector > Text > Font, size, color
   Position and styling adjustments
   ```

### API Integration Examples

**Python Script Integration:**
```python
from audio_to_srt import AudioToSRT

# Initialize converter
converter = AudioToSRT(model_size="base")

# Process multiple files with progress tracking
audio_files = ["episode1.mp3", "episode2.mp3", "episode3.mp3"]

for i, audio_file in enumerate(audio_files):
    print(f"Processing {i+1}/{len(audio_files)}: {audio_file}")
    
    srt_path = converter.convert_mp3_to_srt(
        audio_file,
        max_chars_per_line=50,
        max_duration=5.0
    )
    
    print(f"Generated: {srt_path}")
```

**Web Application Integration:**
```javascript
// Frontend file upload handling
const handleAudioUpload = async (file) => {
  const formData = new FormData();
  formData.append('audio', file);
  formData.append('model', 'base');
  formData.append('maxChars', '50');
  
  const response = await fetch('/api/convert', {
    method: 'POST',
    body: formData
  });
  
  const { srtContent } = await response.json();
  return srtContent;
};
```

### Performance Optimization Examples

**Memory-Constrained Systems:**
```bash
# Use tiny model for lower memory usage
python3 audio_to_srt.py large_file.mp3 --model tiny

# Process in smaller chunks if needed
ffmpeg -i large_file.mp3 -t 300 chunk1.mp3  # First 5 minutes
python3 audio_to_srt.py chunk1.mp3
```

**High-Performance Batch Processing:**
```bash
# Parallel processing with GNU parallel
find ./audio/ -name "*.mp3" | parallel python3 audio_to_srt.py {} --model base

# Or use multiple model sizes simultaneously
python3 audio_to_srt.py file1.mp3 --model tiny &
python3 audio_to_srt.py file2.mp3 --model base &
python3 audio_to_srt.py file3.mp3 --model small &
wait
```

### Quality Control Examples

**Compare Model Outputs:**
```bash
# Generate with different models
python3 audio_to_srt.py test.mp3 --model tiny -o test_tiny.srt
python3 audio_to_srt.py test.mp3 --model base -o test_base.srt
python3 audio_to_srt.py test.mp3 --model large -o test_large.srt

# Compare accuracy manually
# Choose best model for your content type
```

**Subtitle Formatting Tests:**
```bash
# Test different line lengths
python3 audio_to_srt.py video.mp3 --max-chars 30  # Mobile-friendly
python3 audio_to_srt.py video.mp3 --max-chars 50  # Standard
python3 audio_to_srt.py video.mp3 --max-chars 80  # Desktop/reading

# Test different timing
python3 audio_to_srt.py video.mp3 --max-duration 3.0  # Fast-paced
python3 audio_to_srt.py video.mp3 --max-duration 6.0  # Relaxed
```

## Tips and Best Practices

### Audio Quality Tips
- **Use high-quality audio** for better transcription accuracy
- **Reduce background noise** before processing if possible
- **Clear speech** produces better results than music or multiple speakers
- **Consistent volume levels** help with accuracy

### File Management
- **Organize by project** to keep audio and SRT files together
- **Use descriptive filenames** for easy identification
- **Backup original audio files** before processing
- **Version control** for subtitle edits and revisions

### Workflow Optimization
- **Start with tiny model** for quick content preview
- **Use base model** for most production work
- **Reserve large model** for final, critical subtitles
- **Batch process overnight** for large projects

### Subtitle Guidelines
- **40-50 characters per line** for video subtitles
- **60-80 characters per line** for reading/transcripts
- **3-5 second segments** for most content
- **2-3 second segments** for fast-paced content