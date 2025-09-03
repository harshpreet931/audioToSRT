# Contributing to Audio to SRT

Thank you for your interest in contributing to Audio to SRT! This guide will help you get started.

## How to Contribute

### Bug Reports

Before submitting a bug report:
1. Check existing [Issues](https://github.com/harshpreet931/audioToSRT/issues) to avoid duplicates
2. Try the latest version to see if the bug has been fixed
3. Gather relevant information about your system and the bug

**Bug Report Template:**
```
**Environment:**
- OS: [macOS/Windows/Linux + version]
- App Version: [version number]
- Audio Format: [MP3/WAV/etc.]

**Bug Description:**
Clear description of what went wrong

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should have happened

**Actual Behavior:**
What actually happened

**Additional Context:**
Screenshots, error messages, etc.
```

### Feature Requests

We welcome feature ideas! Please:
1. Check [Discussions](https://github.com/harshpreet931/audioToSRT/discussions) for similar requests
2. Explain the use case and benefit
3. Consider the impact on simplicity (our core value)

### Code Contributions

#### Development Setup

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/audioToSRT.git
   cd audioToSRT
   ```
3. **Setup** development environment (see [INSTALLATION.md](INSTALLATION.md))
4. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Code Standards

**Frontend (React/TypeScript):**
- Use TypeScript for all new code
- Follow existing naming conventions
- Add proper error handling
- Keep components simple and focused

**Backend (Rust):**
- Follow Rust best practices
- Handle errors gracefully
- Add appropriate comments for complex logic
- Use existing patterns from the codebase

**Python Integration:**
- Maintain compatibility with existing Python scripts
- Add proper error handling and logging
- Follow PEP 8 style guidelines
- Add docstrings for new functions

**General Guidelines:**
- Write clear commit messages
- Keep changes focused and atomic
- Add tests for new functionality
- Update documentation as needed

#### Pull Request Process

1. **Test** your changes thoroughly
2. **Update** documentation if needed
3. **Submit** a pull request with:
   - Clear title and description
   - Reference to related issues
   - Screenshots for UI changes
   - Testing instructions

**Pull Request Template:**
```
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested on macOS
- [ ] Tested on Windows
- [ ] Tested on Linux
- [ ] Added/updated tests

## Screenshots
(If UI changes)

## Related Issues
Fixes #123
```

#### Review Process

1. Maintainers will review your PR
2. Address any feedback promptly
3. Keep the PR updated with main branch
4. Once approved, we'll merge your contribution

## Development Priorities

### High Priority
- Real-time progress updates during conversion
- Improved error handling and user feedback
- Performance optimizations
- Cross-platform compatibility fixes

### Medium Priority
- Batch processing UI improvements
- Additional export formats (WebVTT, ASS)
- Advanced subtitle timing controls
- Memory usage optimization

### Future Features
- Custom model training interface
- Multi-language auto-detection
- Professional workflow integrations
- Plugin system for video editors

## Code of Conduct

### Our Standards

**Positive behaviors:**
- Using welcoming and inclusive language
- Respecting differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards other community members

**Unacceptable behaviors:**
- Harassment of any kind
- Publishing others' private information
- Trolling, insulting/derogatory comments
- Other conduct inappropriate in a professional setting

### Enforcement

Project maintainers are responsible for clarifying standards and will take appropriate action in response to any behavior that violates this code of conduct.

## Architecture Overview

### Project Structure
```
audioToSRT/
├── audio_to_srt.py          # Core Python transcription logic
├── batch_convert.py         # Batch processing script
├── requirements.txt         # Python dependencies
├── audio-to-srt-app/        # Tauri desktop application
│   ├── src/                 # React frontend
│   ├── src-tauri/           # Rust backend
│   └── package.json         # Node.js dependencies
├── .github/workflows/       # CI/CD automation
└── docs/                    # Documentation
```

### Key Components

**Frontend (React + TypeScript):**
- `App.tsx` - Main application component
- `App.css` - Minimal professional styling
- Drag & drop file interface
- Real-time job status tracking

**Backend (Rust + Tauri):**
- `lib.rs` - Main Tauri commands
- `convert_audio_to_srt` - Python subprocess integration
- `reveal_in_finder` - Cross-platform file operations

**Python Core:**
- `AudioToSRT` class - Whisper integration
- FFmpeg audio preprocessing
- SRT file generation and formatting

## Getting Help

- **Development Questions**: [GitHub Discussions](https://github.com/harshpreet931/audioToSRT/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/harshpreet931/audioToSRT/issues)
- **Feature Ideas**: [GitHub Discussions](https://github.com/harshpreet931/audioToSRT/discussions)

## Recognition

Contributors will be:
- Listed in release notes
- Added to the project's contributors section
- Mentioned in relevant documentation

Thank you for helping make Audio to SRT better!