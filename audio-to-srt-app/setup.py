#!/usr/bin/env python3
"""
Setup script for Audio to SRT Converter
Ensures Python dependencies are installed for the Tauri app
"""

import subprocess
import sys
import os
import venv
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"Python version OK: {sys.version.split()[0]}")

def install_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("FFmpeg is already installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg not found")
        
        # Try to install with homebrew on macOS
        if sys.platform == "darwin":
            try:
                print("Attempting to install FFmpeg with Homebrew...")
                subprocess.run(["brew", "install", "ffmpeg"], check=True)
                print("FFmpeg installed successfully")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Failed to install FFmpeg. Please install manually:")
                print("   brew install ffmpeg")
                return False
        else:
            print("Please install FFmpeg manually:")
            print("   - Windows: Download from https://ffmpeg.org/download.html")
            print("   - Linux: sudo apt install ffmpeg (Ubuntu/Debian)")
            print("   - macOS: brew install ffmpeg")
            return False

def setup_python_env():
    """Setup Python virtual environment and install dependencies"""
    app_dir = Path(__file__).parent
    venv_dir = app_dir / "python_env"
    
    # Create virtual environment
    if not venv_dir.exists():
        print("Creating Python virtual environment...")
        venv.create(venv_dir, with_pip=True)
    else:
        print("Python virtual environment already exists")
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        pip_path = venv_dir / "Scripts" / "pip.exe"
        python_path = venv_dir / "Scripts" / "python.exe"
    else:
        pip_path = venv_dir / "bin" / "pip"
        python_path = venv_dir / "bin" / "python"
    
    print("Installing Python dependencies...")
    
    # Install requirements
    requirements = [
        "openai-whisper==20231117",
        "pydub==0.25.1", 
        "srt==3.5.3"
    ]
    
    for req in requirements:
        try:
            subprocess.run([str(pip_path), "install", req], check=True, capture_output=True)
            print(f"Installed {req}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {req}: {e}")
            return False
    
    return True

def main():
    print("Audio to SRT Converter Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Check/install FFmpeg
    ffmpeg_ok = install_ffmpeg()
    
    # Setup Python environment
    python_ok = setup_python_env()
    
    print("\\n" + "=" * 40)
    if ffmpeg_ok and python_ok:
        print("Setup completed successfully!")
        print("\\nNext steps:")
        print("1. Build the app: npm run tauri build")
        print("2. Or run in development: npm run tauri dev")
    else:
        print("Setup completed with warnings")
        print("   Please resolve the issues above before using the app")

if __name__ == "__main__":
    main()