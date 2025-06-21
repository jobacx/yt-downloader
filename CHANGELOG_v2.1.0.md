# YouTube Downloader v2.1.0 - Changelog

## 🎉 New Features & Enhancements

### 1. **Application and Installer Icons**
- ✅ **Window Icon**: Added custom icon to the application window
- ✅ **Installer Icon**: Updated installer to include and copy the icon file
- 📁 **Location**: `icon.ico` in the main application directory

### 2. **Default Downloads Directory**
- ✅ **Auto-Detection**: Output directory now defaults to user's Downloads folder
- ✅ **Cross-Platform**: Works on Windows, Linux, and macOS
- ✅ **Auto-Creation**: Creates Downloads folder if it doesn't exist
- 📁 **Default Path**: `%USERPROFILE%\Downloads` (Windows)

### 3. **Enhanced FFmpeg Detection & UX**
- ✅ **Improved Detection**: Better logic for finding FFmpeg installations
- ✅ **Multiple Locations**: Checks system PATH and common installation paths:
  - `C:/tools/ffmpeg/bin/ffmpeg.exe`
  - `C:/ffmpeg/bin/ffmpeg.exe`
  - `C:/Program Files/ffmpeg/bin/ffmpeg.exe`
  - `C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe`
  - `C:/ProgramData/chocolatey/bin/ffmpeg.exe` (Chocolatey installs)
- ✅ **Better UX**: Placeholder text when FFmpeg not found
- ✅ **Smart Validation**: Only shows paths that actually work
- ✅ **Clear Feedback**: Better status messages for users

## 🔧 Technical Improvements

### Code Quality
- Enhanced error handling for FFmpeg detection
- Better user feedback with color-coded status messages
- Improved input field behavior with focus events

### User Experience
- Placeholder text for empty FFmpeg field
- Automatic clearing/restoration of placeholder text
- More informative status messages

### Installation
- Updated installer to v2.1.0
- Automatic icon copying during installation
- Better FFmpeg setup instructions

## 📋 Files Modified

1. **`download.py`** - Main application file
   - Added `get_downloads_folder()` function
   - Enhanced FFmpeg detection logic
   - Added window icon support
   - Improved UI/UX for FFmpeg field

2. **`create_installer.bat`** - Installation script
   - Updated to v2.1.0
   - Added icon copying
   - Enhanced user instructions

3. **`requirements.txt`** - Dependencies
   - Added Pillow for icon processing

4. **`icon.ico`** - Application icon
   - Custom icon for window and installer

## 🚀 Installation & Usage

1. **Install FFmpeg** (if not already installed):
   ```bash
   # Option 1: Using Chocolatey (Recommended)
   choco install ffmpeg
   
   # Option 2: Manual installation to C:\tools\ffmpeg\bin\
   ```

2. **Run the application**:
   - Downloads folder is automatically selected
   - FFmpeg is auto-detected if properly installed
   - Use Browse button if FFmpeg is in a custom location

3. **Build executable**:
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Build with PyInstaller (ensure icon.ico is in the directory)
   pyinstaller --onefile --windowed --icon=icon.ico download.py
   ```

## 🎯 Version Information
- **Version**: 2.1.0
- **Previous Version**: 2.0.0
- **Release Date**: December 2024
- **Compatibility**: Windows 10/11, Python 3.8+

---

**All requested features for v2.1.0 have been successfully implemented and tested! 🎉** 