#!/usr/bin/env python3
"""
Batch Audio to SRT Converter
Process multiple MP3 files in a directory
"""

import argparse
import sys
from pathlib import Path

from audio_to_srt import AudioToSRT


def batch_convert(input_dir, output_dir=None, model_size="base", max_chars_per_line=50, max_duration=5.0):
    """
    Convert all MP3 files in a directory to SRT files
    
    Args:
        input_dir (str): Directory containing MP3 files
        output_dir (str): Directory to save SRT files (optional)
        model_size (str): Whisper model size
        max_chars_per_line (int): Maximum characters per subtitle line
        max_duration (float): Maximum duration per subtitle segment
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    # Find all MP3 files
    mp3_files = list(input_path.glob("*.mp3")) + list(input_path.glob("*.MP3"))
    
    if not mp3_files:
        print(f"No MP3 files found in {input_dir}")
        return
    
    print(f"Found {len(mp3_files)} MP3 file(s)")
    
    # Set up output directory
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path
    
    # Initialize converter
    converter = AudioToSRT(model_size=model_size)
    
    # Process each file
    successful = 0
    failed = 0
    
    for i, mp3_file in enumerate(mp3_files, 1):
        try:
            print(f"\n[{i}/{len(mp3_files)}] Processing: {mp3_file.name}")
            
            output_file = output_path / mp3_file.with_suffix('.srt').name
            
            converter.convert_mp3_to_srt(
                mp3_path=str(mp3_file),
                output_path=str(output_file),
                max_chars_per_line=max_chars_per_line,
                max_duration=max_duration
            )
            
            successful += 1
            
        except Exception as e:
            print(f"❌ Failed to process {mp3_file.name}: {e}")
            failed += 1
    
    print("\n✅ Batch processing complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert MP3 files to SRT subtitle files"
    )
    parser.add_argument("input_dir", help="Directory containing MP3 files")
    parser.add_argument("-o", "--output-dir", help="Output directory for SRT files")
    parser.add_argument("-m", "--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("--max-chars", type=int, default=50,
                       help="Maximum characters per subtitle line (default: 50)")
    parser.add_argument("--max-duration", type=float, default=5.0,
                       help="Maximum duration per subtitle in seconds (default: 5.0)")
    
    args = parser.parse_args()
    
    try:
        batch_convert(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            model_size=args.model,
            max_chars_per_line=args.max_chars,
            max_duration=args.max_duration
        )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
