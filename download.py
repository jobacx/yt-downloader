import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from yt_dlp import YoutubeDL
import os
import subprocess
import queue
import time
import sys
import io

def check_ffmpeg_installation(ffmpeg_path):
    """Check if FFmpeg is available at the given path"""
    try:
        result = subprocess.run([ffmpeg_path, '-version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return False

def find_ffmpeg_in_path():
    """Try to find FFmpeg in system PATH"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return 'ffmpeg'  # Return just the command name if found in PATH
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    return None

def get_default_ffmpeg_path():
    """Get the default FFmpeg path, checking common locations"""
    # Primary default path
    primary_default = "C:/tools/ffmpeg/bin/ffmpeg.exe"
    
    # Common FFmpeg installation paths on Windows
    common_paths = [
        "C:/tools/ffmpeg/bin/ffmpeg.exe",
        "C:/ffmpeg/bin/ffmpeg.exe",
        "C:/Program Files/ffmpeg/bin/ffmpeg.exe",
        "C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe"
    ]
    
    # Check if FFmpeg is in PATH first
    path_ffmpeg = find_ffmpeg_in_path()
    if path_ffmpeg:
        return path_ffmpeg
    
    # Check if primary default exists and works
    if os.path.exists(primary_default) and check_ffmpeg_installation(primary_default):
        return primary_default
    
    # Check other common installation paths
    for path in common_paths[1:]:  # Skip the first one since we already checked it
        if os.path.exists(path) and check_ffmpeg_installation(path):
            return path
    
    # Return the primary default path even if not found (user will need to change it)
    return primary_default

class CustomLogger:
    def __init__(self, log_queue):
        self.log_queue = log_queue
        self.download_finished = False
        
    def debug(self, msg):
        if '[download]' in msg:
            if '100%' in msg or 'finished' in msg.lower():
                self.download_finished = True
            self.log_queue.put(f"[DEBUG] {msg}")
        elif '[Merger]' in msg:
            self.log_queue.put(f"[MERGE] {msg}")
        elif '[VideoConvertor]' in msg:
            self.log_queue.put(f"[CONVERT] {msg}")
        elif 'Deleting' in msg:
            self.log_queue.put(f"[CLEANUP] {msg}")
            
    def info(self, msg):
        self.log_queue.put(f"[INFO] {msg}")
        
    def warning(self, msg):
        self.log_queue.put(f"[WARNING] {msg}")
        
    def error(self, msg):
        self.log_queue.put(f"[ERROR] {msg}")

class ProgressHook:
    def __init__(self, log_queue):
        self.log_queue = log_queue
        self.files_finished = 0
        self.total_files = 0
    
    def __call__(self, d):
        if d['status'] == 'downloading':
            # Extract progress information
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            filename = d.get('filename', 'Unknown file')
            
            if total > 0:
                percentage = (downloaded / total) * 100
                speed_mb = speed / 1024 / 1024 if speed else 0
                eta_str = f"{eta//60:02d}:{eta%60:02d}" if eta else "Unknown"
                
                # Extract just the filename without path
                file_display = os.path.basename(filename) if filename != 'Unknown file' else filename
                log_message = f"[DOWNLOAD] {file_display} - {percentage:.1f}% | Speed: {speed_mb:.2f} MB/s | ETA: {eta_str}"
                self.log_queue.put(log_message)
                
        elif d['status'] == 'finished':
            filename = d.get('filename', 'Unknown file')
            file_display = os.path.basename(filename) if filename != 'Unknown file' else filename
            self.log_queue.put(f"[FINISHED] {file_display}")
            self.files_finished += 1
            
        elif d['status'] == 'error':
            self.log_queue.put(f"[ERROR] {d.get('error', 'Unknown error')}")

def download_highest_resolution(url, output_path='.', ffmpeg_path=None, log_queue=None):
    progress_hook = ProgressHook(log_queue) if log_queue else None
    custom_logger = CustomLogger(log_queue) if log_queue else None
    
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',  # Merge into MP4
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Ensure MP4 output
        }],
        'progress_hooks': [progress_hook] if progress_hook else [],
        'logger': custom_logger,
        'verbose': True,
    }
    
    # Add FFmpeg location if provided
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # Add final success message
        if log_queue:
            log_queue.put("[SUCCESS] Download and processing completed successfully!")
            
        return True
        
    except Exception as e:
        if log_queue:
            log_queue.put(f"[ERROR] Download failed: {str(e)}")
        raise e

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.ffmpeg_path = get_default_ffmpeg_path()
        self.log_queue = queue.Queue()
        self.download_success = False
        self.create_widgets()
        self.validate_ffmpeg()
        self.start_log_consumer()

    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # URL Entry
        url_label = ttk.Label(main_frame, text="YouTube URL:")
        url_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        # Directory Entry
        dir_label = ttk.Label(main_frame, text="Output Directory:")
        dir_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.dir_entry = ttk.Entry(main_frame, width=40)
        self.dir_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        browse_button = ttk.Button(main_frame, text="Browse", command=self.browse_directory)
        browse_button.grid(row=1, column=2, padx=5, pady=5)

        # FFmpeg Location Entry
        ffmpeg_label = ttk.Label(main_frame, text="FFmpeg Location:")
        ffmpeg_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.ffmpeg_entry = ttk.Entry(main_frame, width=40)
        self.ffmpeg_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        self.ffmpeg_entry.insert(0, self.ffmpeg_path)
        ffmpeg_browse_button = ttk.Button(main_frame, text="Browse", command=self.browse_ffmpeg)
        ffmpeg_browse_button.grid(row=2, column=2, padx=5, pady=5)

        # Download Button
        self.download_button = ttk.Button(main_frame, text="Download", command=self.start_download)
        self.download_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=tk.EW)

        # Status Label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        # Log Display
        log_label = ttk.Label(main_frame, text="Download Logs:")
        log_label.grid(row=5, column=0, columnspan=3, padx=5, pady=(10, 5), sticky=tk.W)
        
        # Create scrolled text widget for logs
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=80, 
                                                 font=('Consolas', 9), bg='black', fg='white')
        self.log_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Configure grid weights to make widgets expand
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def start_log_consumer(self):
        """Start the log consumer thread"""
        def consume_logs():
            while True:
                try:
                    # Get log message from queue with timeout
                    message = self.log_queue.get(timeout=0.1)
                    timestamp = time.strftime("%H:%M:%S")
                    formatted_message = f"[{timestamp}] {message}\n"
                    
                    # Check for success indicators
                    if "[SUCCESS]" in message or "completed successfully" in message.lower():
                        self.download_success = True
                    
                    # Update UI in main thread
                    self.root.after(0, self.append_log, formatted_message)
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Log consumer error: {e}")
                    break
        
        log_thread = threading.Thread(target=consume_logs, daemon=True)
        log_thread.start()

    def append_log(self, message):
        """Append message to log text widget"""
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)  # Auto-scroll to bottom
        self.root.update_idletasks()

    def clear_logs(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
        self.download_success = False

    def validate_ffmpeg(self):
        """Validate FFmpeg installation and update UI accordingly"""
        ffmpeg_path = self.ffmpeg_entry.get().strip()
        if check_ffmpeg_installation(ffmpeg_path):
            self.status_label.config(text="FFmpeg found and ready to use", foreground="green")
            self.download_button.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="FFmpeg not found. Please locate FFmpeg installation.", foreground="red")
            self.download_button.config(state=tk.DISABLED)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def browse_ffmpeg(self):
        file_path = filedialog.askopenfilename(
            title="Select FFmpeg executable",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if file_path:
            self.ffmpeg_entry.delete(0, tk.END)
            self.ffmpeg_entry.insert(0, file_path)
            self.validate_ffmpeg()

    def start_download(self):
        url = self.url_entry.get().strip()
        directory = self.dir_entry.get().strip() or '.'  # Default to current directory if empty
        ffmpeg_path = self.ffmpeg_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        
        if not ffmpeg_path:
            messagebox.showerror("Error", "Please specify FFmpeg location.")
            return
        
        if not check_ffmpeg_installation(ffmpeg_path):
            messagebox.showerror("Error", "FFmpeg not found at the specified location. Please verify the path.")
            return
        
        # Clear previous logs
        self.clear_logs()
        
        # Disable the download button during download
        self.download_button.config(state=tk.DISABLED)
        self.status_label.config(text="Downloading...", foreground="black")
        
        # Add initial log message
        self.append_log(f"Starting download for: {url}\n")
        self.append_log(f"Output directory: {directory}\n")
        self.append_log(f"FFmpeg path: {ffmpeg_path}\n")
        self.append_log("-" * 50 + "\n")
        
        # Start the download in a thread
        thread = threading.Thread(target=self.download_thread, args=(url, directory, ffmpeg_path))
        thread.start()

    def download_thread(self, url, directory, ffmpeg_path):
        try:
            success = download_highest_resolution(url, directory, ffmpeg_path, self.log_queue)
            # Give a moment for all logs to be processed
            time.sleep(1)
            self.root.after(0, self.on_download_complete, True, None)
        except Exception as e:
            error_msg = f"Download error: {str(e)}"
            self.log_queue.put(error_msg)
            self.root.after(0, self.on_download_complete, False, str(e))

    def on_download_complete(self, success, error):
        self.download_button.config(state=tk.NORMAL)
        
        # Check if we detected success through logs
        if success or self.download_success:
            self.status_label.config(text="Download completed successfully!", foreground="green")
            self.append_log("\n" + "=" * 50 + "\n")
            self.append_log("DOWNLOAD COMPLETED SUCCESSFULLY!\n")
            self.append_log("Check your output directory for the downloaded file.\n")
        else:
            self.status_label.config(text=f"Error: {error}", foreground="red")
            self.append_log("\n" + "=" * 50 + "\n")
            self.append_log(f"DOWNLOAD FAILED: {error}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()