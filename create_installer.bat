@echo off
echo ========================================
echo YouTube Downloader Installer v2.0
echo ========================================
echo.

set "INSTALL_DIR=%USERPROFILE%\Desktop\YouTube Downloader"

echo Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Copying executable...
copy "dist\YouTube_Downloader.exe" "%INSTALL_DIR%\"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo The YouTube Downloader has been installed to:
echo %INSTALL_DIR%
echo.
echo IMPORTANT: FFmpeg Setup Required
echo ========================================
echo This application requires FFmpeg to work properly.
echo.
echo RECOMMENDED: Install FFmpeg to the default location:
echo C:\tools\ffmpeg\bin\ffmpeg.exe
echo.
echo Quick FFmpeg Installation Options:
echo.
echo Option 1 - Using Chocolatey (Easiest):
echo   1. Open PowerShell as Administrator
echo   2. Run: choco install ffmpeg
echo.
echo Option 2 - Manual Installation:
echo   1. Download FFmpeg from: https://ffmpeg.org/download.html
echo   2. Extract to: C:\tools\ffmpeg\
echo   3. The ffmpeg.exe should be at: C:\tools\ffmpeg\bin\ffmpeg.exe
echo.
echo Option 3 - Use Browse Button:
echo   1. Install FFmpeg anywhere on your system
echo   2. Use the Browse button in the app to locate ffmpeg.exe
echo.
echo ========================================
echo.
echo Press any key to open the installation folder...
pause >nul

explorer "%INSTALL_DIR%"

echo.
echo Installation folder opened!
echo You can now run YouTube_Downloader.exe
echo.
echo Press any key to exit...
pause >nul 