#!/usr/bin/env python3
"""
Audio to SRT Converter
Converts MP3 files to SRT subtitle files using OpenAI Whisper
Perfect for importing into DaVinci Resolve
"""

import argparse
import os
import sys
from datetime import timedelta
from pathlib import Path

import srt
import whisper


class AudioToSRT:
    def __init__(self, model_size="base"):
        """
        Initialize the converter with Whisper model
        
        Args:
            model_size (str): Whisper model size - tiny, base, small, medium, large
        """
        print(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        print("Model loaded successfully!")
    
    def convert_mp3_to_srt(self, mp3_path, output_path=None, max_chars_per_line=50, max_duration=5.0):
        """
        Convert MP3 file to SRT subtitle file
        
        Args:
            mp3_path (str): Path to the MP3 file
            output_path (str): Path for the output SRT file (optional)
            max_chars_per_line (int): Maximum characters per subtitle line
            max_duration (float): Maximum duration per subtitle segment in seconds
        
        Returns:
            str: Path to the generated SRT file
        """
        if not os.path.exists(mp3_path):
            raise FileNotFoundError(f"MP3 file not found: {mp3_path}")
        
        # Generate output path if not provided
        if output_path is None:
            mp3_file = Path(mp3_path)
            output_path = mp3_file.with_suffix('.srt')
        
        print(f"Transcribing: {mp3_path}")
        
        # Transcribe audio with word-level timestamps
        result = self.model.transcribe(
            mp3_path,
            word_timestamps=True,
            verbose=False
        )
        
        print("Transcription complete! Creating subtitles...")
        
        # Create subtitle segments
        subtitles = self._create_subtitle_segments(
            result, 
            max_chars_per_line, 
            max_duration
        )
        
        # Write SRT file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt.compose(subtitles))
        
        print(f"SRT file created: {output_path}")
        return str(output_path)
    
    def _create_subtitle_segments(self, result, max_chars_per_line, max_duration):
        """
        Create properly formatted subtitle segments from Whisper output
        
        Args:
            result: Whisper transcription result
            max_chars_per_line (int): Maximum characters per line
            max_duration (float): Maximum duration per segment
        
        Returns:
            list: List of SRT subtitle objects
        """
        subtitles = []
        segment_index = 1
        
        for segment in result['segments']:
            text = segment['text'].strip()
            start_time = segment['start']
            end_time = segment['end']
            
            # Split long segments
            if len(text) > max_chars_per_line or (end_time - start_time) > max_duration:
                sub_segments = self._split_segment(segment, max_chars_per_line, max_duration)
                for sub_segment in sub_segments:
                    subtitle = srt.Subtitle(
                        index=segment_index,
                        start=timedelta(seconds=sub_segment['start']),
                        end=timedelta(seconds=sub_segment['end']),
                        content=sub_segment['text'].strip()
                    )
                    subtitles.append(subtitle)
                    segment_index += 1
            else:
                subtitle = srt.Subtitle(
                    index=segment_index,
                    start=timedelta(seconds=start_time),
                    end=timedelta(seconds=end_time),
                    content=text
                )
                subtitles.append(subtitle)
                segment_index += 1
        
        return subtitles
    
    def _split_segment(self, segment, max_chars_per_line, max_duration):
        """
        Split a long segment into smaller ones based on word boundaries
        
        Args:
            segment: Whisper segment with word-level timestamps
            max_chars_per_line (int): Maximum characters per line
            max_duration (float): Maximum duration per segment
        
        Returns:
            list: List of sub-segments
        """
        if 'words' not in segment:
            # Fallback: split by time only
            return self._split_by_time(segment, max_duration)
        
        words = segment['words']
        sub_segments = []
        current_text = ""
        current_start = words[0]['start']
        current_words = []
        
        for word in words:
            word_text = word['word']
            word_start = word['start']
            word_end = word['end']
            
            # Check if adding this word would exceed limits
            potential_text = current_text + word_text
            potential_duration = word_end - current_start
            
            if (len(potential_text) > max_chars_per_line or 
                potential_duration > max_duration) and current_text:
                
                # Create sub-segment with current words
                sub_segments.append({
                    'text': current_text.strip(),
                    'start': current_start,
                    'end': current_words[-1]['end'] if current_words else word_start
                })
                
                # Start new sub-segment
                current_text = word_text
                current_start = word_start
                current_words = [word]
            else:
                current_text = potential_text
                current_words.append(word)
        
        # Add the last sub-segment
        if current_text:
            sub_segments.append({
                'text': current_text.strip(),
                'start': current_start,
                'end': current_words[-1]['end']
            })
        
        return sub_segments
    
    def _split_by_time(self, segment, max_duration):
        """
        Fallback method to split segment by time when word timestamps aren't available
        """
        text = segment['text']
        start_time = segment['start']
        end_time = segment['end']
        duration = end_time - start_time
        
        if duration <= max_duration:
            return [{'text': text, 'start': start_time, 'end': end_time}]
        
        # Split text roughly in half
        words = text.split()
        mid_point = len(words) // 2
        
        first_half = ' '.join(words[:mid_point])
        second_half = ' '.join(words[mid_point:])
        
        mid_time = start_time + (duration / 2)
        
        return [
            {'text': first_half, 'start': start_time, 'end': mid_time},
            {'text': second_half, 'start': mid_time, 'end': end_time}
        ]


def main():
    parser = argparse.ArgumentParser(
        description="Convert MP3 files to SRT subtitle files using AI transcription"
    )
    parser.add_argument("input", help="Path to MP3 file")
    parser.add_argument("-o", "--output", help="Output SRT file path")
    parser.add_argument("-m", "--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--max-chars", type=int, default=50,
                       help="Maximum characters per subtitle line (default: 50)")
    parser.add_argument("--max-duration", type=float, default=5.0,
                       help="Maximum duration per subtitle in seconds (default: 5.0)")
    
    args = parser.parse_args()
    
    try:
        # Create converter
        converter = AudioToSRT(model_size=args.model)
        
        # Convert MP3 to SRT
        output_file = converter.convert_mp3_to_srt(
            mp3_path=args.input,
            output_path=args.output,
            max_chars_per_line=args.max_chars,
            max_duration=args.max_duration
        )
        
        print(f"\n✅ Success! SRT file created: {output_file}")
        print("\n📝 To use in DaVinci Resolve:")
        print("1. Import your video file")
        print("2. Right-click on the video in the Media Pool")
        print("3. Select 'Import Subtitle'")
        print(f"4. Choose the generated file: {output_file}")
        print("5. The subtitles will be automatically synced!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
