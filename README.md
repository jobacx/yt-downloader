# YouTube Video Downloader

A modern, user-friendly YouTube video downloader with a GUI interface built using Python, tkinter, and yt-dlp. Features real-time download progress, automatic video/audio merging, and smart FFmpeg integration.

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## ✨ Features

- 🎥 **High-Quality Downloads** - Download YouTube videos up to 1080p resolution
- 🔄 **Automatic Merging** - Seamlessly combines video and audio into MP4 format
- 📊 **Real-Time Progress** - Live download progress with speed and ETA information
- 🖥️ **User-Friendly GUI** - Clean, intuitive interface built with tkinter
- 🔍 **Smart FFmpeg Detection** - Automatically finds FFmpeg installations
- 📁 **Flexible Output** - Choose custom download directories
- 📝 **Detailed Logging** - Comprehensive real-time logs for debugging
- ⚡ **Standalone Executable** - No Python installation required for end users

## 📋 Requirements

### For End Users (Executable)
- Windows 10/11
- FFmpeg (installation instructions included)

### For Developers
- Python 3.8 or higher
- FFmpeg
- Virtual environment (recommended)

## 🚀 Quick Start (End Users)

### Option 1: Download Pre-built Executable
1. Download `YouTube_Downloader_v2.0.zip` from releases
2. Extract the ZIP file
3. Run `create_installer.bat` for guided setup
4. Install FFmpeg (see FFmpeg Installation section)
5. Launch `YouTube_Downloader.exe`

### Option 2: Manual Installation
1. Download `YouTube_Downloader.exe` from the `dist/` folder
2. Install FFmpeg to `C:\tools\ffmpeg\bin\ffmpeg.exe` (recommended)
3. Double-click the executable to run

## 🛠️ Development Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd yt-downloader
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv
#or
python3 -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Mac Terminal Prompt:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg
See the [FFmpeg Installation](#ffmpeg-installation) section below.

### 5. Run the Application
```bash
python download.py
```

## 📦 FFmpeg Installation

FFmpeg is required for merging video and audio files. The application defaults to `C:\tools\ffmpeg\bin\ffmpeg.exe`.

### Option 1: Chocolatey (Recommended)
```powershell
# Run as Administrator
choco install ffmpeg
```

### Option 2: Manual Installation
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\tools\ffmpeg\`
3. Verify `ffmpeg.exe` is at `C:\tools\ffmpeg\bin\ffmpeg.exe`

### Option 3: Add to System PATH
1. Install FFmpeg anywhere on your system
2. Add the `bin` folder to your Windows PATH environment variable
3. The application will automatically detect it

### Option 4: Custom Location
Use the "Browse" button in the application to locate your FFmpeg installation.

## 💻 Usage

1. **Launch the Application**
   - Run `python download.py` (development)
   - Or double-click `YouTube_Downloader.exe` (executable)

2. **Enter YouTube URL**
   - Paste any valid YouTube video URL

3. **Select Output Directory**
   - Use the Browse button or leave empty for current directory

4. **Verify FFmpeg Path**
   - The application will auto-detect FFmpeg
   - Use Browse if needed to locate manually

5. **Start Download**
   - Click "Download" and monitor real-time progress
   - Check the logs for detailed information

## 🔧 Compilation and Distribution

### Prerequisites for Compilation
```bash
pip install pyinstaller
```

### Build Executable
```bash
# Clean build
pyinstaller --clean build_config.spec
```

### Build Configuration
The `build_config.spec` file contains:
- Application name: `YouTube_Downloader`
- Console window: Hidden for clean user experience
- All dependencies bundled
- Optimized for Windows

### Distribution Package Contents
- `YouTube_Downloader.exe` - Main executable (18MB)
- `README.txt` - User instructions
- `create_installer.bat` - Installation script

### Create Distribution ZIP
```bash
Compress-Archive -Path "dist\*", "create_installer.bat" -DestinationPath "YouTube_Downloader_v2.0.zip" -Force
```

## 📁 Project Structure

```
yt-downloader/
├── download.py              # Main application source
├── requirements.txt         # Python dependencies
├── build_config.spec       # PyInstaller configuration
├── create_installer.bat    # User installation script
├── README.md               # This file
├── dist/                   # Compiled executable
│   ├── YouTube_Downloader.exe
│   └── README.txt
└── .venv/                  # Virtual environment (development)
```

## 🔍 Technical Details

### Dependencies
- **yt-dlp** - YouTube video downloading engine
- **tkinter** - GUI framework (built into Python)
- **threading** - Background download processing
- **subprocess** - FFmpeg integration
- **queue** - Thread-safe logging

### Architecture
- **Main Thread** - GUI and user interaction
- **Download Thread** - Video downloading process
- **Log Consumer Thread** - Real-time log processing
- **Progress Hooks** - Download progress tracking
- **Custom Logger** - yt-dlp output capture

### Download Process
1. URL validation and FFmpeg verification
2. yt-dlp extracts video information
3. Downloads best video (≤1080p) and audio streams
4. FFmpeg merges streams into MP4
5. Cleanup of temporary files
6. Success confirmation

## 🐛 Troubleshooting

### Common Issues

**"FFmpeg not found" Error**
- Install FFmpeg using one of the methods above
- Verify the path in the application
- Use the Browse button to locate manually

**Download Fails with Permission Error**
- Choose a different output directory (Desktop, Downloads)
- Run as Administrator if necessary
- Check disk space availability

**Application Won't Start**
- Ensure Windows 10/11 compatibility
- Install Visual C++ Redistributables
- Check antivirus software (may flag PyInstaller executables)

**Poor Video Quality**
- Application downloads best available quality up to 1080p
- Some videos may not have high-resolution versions
- Check the original video quality on YouTube

### Debug Mode
For developers, run with verbose output:
```bash
python download.py --debug
```

## 🔄 Version History

### v2.0 (Current)
- Enhanced real-time logging with detailed progress
- Improved success detection and error handling  
- Better FFmpeg path management and auto-detection
- Updated default FFmpeg location to `C:\tools\ffmpeg\bin\ffmpeg.exe`
- More detailed progress information with filenames
- Professional installer with comprehensive instructions
- Complete documentation and troubleshooting guide

### v1.0
- Initial release with basic YouTube downloading
- GUI interface with tkinter
- FFmpeg integration for video/audio merging
- Basic progress tracking and error handling

## 📄 License

This project is for educational and personal use. Please respect YouTube's Terms of Service and only download content you have permission to download.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify FFmpeg installation
3. Ensure stable internet connection
4. Try a different output directory
5. Check that the YouTube URL is valid and accessible

---

**Enjoy downloading your favorite YouTube videos responsibly!** 🎉

