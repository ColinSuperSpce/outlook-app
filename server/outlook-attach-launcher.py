#!/usr/bin/env python3
"""
Outlook Auto Attach Server Launcher with GUI
Simple GUI application to start/stop the server
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import http.server
import sys
import os
import socket
from datetime import datetime

# Import server functionality from outlook-attach-server.py
# Handle both development (direct Python) and PyInstaller bundled execution
def get_server_file_path():
    """Get the path to outlook-attach-server.py, handling PyInstaller bundling."""
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller bundle
        base_path = sys._MEIPASS
        server_file = os.path.join(base_path, "outlook-attach-server.py")
    else:
        # Running as a script
        base_path = os.path.dirname(os.path.abspath(__file__))
        server_file = os.path.join(base_path, "outlook-attach-server.py")
    
    if not os.path.exists(server_file):
        raise FileNotFoundError(f"Could not find outlook-attach-server.py at: {server_file}")
    
    return server_file

# Import server code
try:
    import importlib.util
    server_file_path = get_server_file_path()
    spec = importlib.util.spec_from_file_location(
        "outlook_attach_server",
        server_file_path
    )
    server_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server_module)
except Exception as e:
    # If import fails, show error and exit
    import traceback
    error_msg = f"Failed to load server module: {e}\n{traceback.format_exc()}"
    print(error_msg, file=sys.stderr)
    # Try to show error dialog (might not work if tkinter isn't loaded)
    try:
        import tkinter.messagebox
        root = tk.Tk()
        root.withdraw()
        tkinter.messagebox.showerror("Error", f"Failed to start application:\n{e}")
    except:
        pass
    sys.exit(1)

PORT = server_module.PORT
BaseAttachHandler = server_module.AttachHandler

# Create GUI-aware handler that logs to GUI
class GUIAttachHandler(BaseAttachHandler):
    """HTTP request handler that logs to GUI."""
    
    def log_message(self, format, *args):
        """Override to log to GUI as well as stderr."""
        timestamp = datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")
        message = f"{timestamp} {format % args}"
        # Log to stderr (original behavior)
        sys.stderr.write(message + "\n")
        # Also send to GUI log if callback is set
        if hasattr(self.server, 'log_callback'):
            self.server.log_callback(message)


class ServerLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Outlook Auto Attach Server")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        self.server_running = False
        self.server_instance = None
        self.server_thread = None
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_ui()
        
        # Check if server is already running
        self.check_server_status()
        
        # Auto-start server if not already running (after a short delay to ensure UI is ready)
        if not self.server_running:
            self.root.after(500, self.auto_start_server)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_ui(self):
        """Create the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Outlook Auto Attach Server",
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Server Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(
            status_frame,
            text="Status: Stopped",
            font=("Helvetica", 12)
        )
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.port_label = ttk.Label(
            status_frame,
            text=f"Port: {PORT}",
            font=("Helvetica", 10)
        )
        self.port_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        self.start_button = ttk.Button(
            button_frame,
            text="Start Server",
            command=self.start_server,
            width=15
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop Server",
            command=self.stop_server,
            state=tk.DISABLED,
            width=15
        )
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            width=60,
            font=("Courier", 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Info label
        info_label = ttk.Label(
            main_frame,
            text="The server runs in the background. You can minimize this window.",
            font=("Helvetica", 9),
            foreground="gray"
        )
        info_label.grid(row=4, column=0, columnspan=2)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def log(self, message):
        """Add a message to the log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Update UI (thread-safe)
        self.root.after(0, self.update_log_ui, log_entry)
    
    def update_log_ui(self, message):
        """Update the log UI (must be called from main thread)."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Keep only last 100 lines
        line_count = int(self.log_text.index('end-1c').split('.')[0])
        if line_count > 100:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete('1.0', '2.0')
            self.log_text.config(state=tk.DISABLED)
    
    def check_server_status(self):
        """Check if server is already running on the port."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', PORT))
        sock.close()
        
        if result == 0:
            self.log("Server appears to be running already (port in use)")
            self.server_running = True
            self.update_ui()
        else:
            self.log("Server is stopped")
    
    def auto_start_server(self):
        """Automatically start the server when app launches."""
        if not self.server_running:
            self.log("Auto-starting server...")
            self.start_server()
    
    def start_server(self):
        """Start the server in a separate thread."""
        if self.server_running:
            self.log("Server is already running!")
            return
        
        def run_server():
            try:
                server_address = ('', PORT)
                httpd = http.server.HTTPServer(server_address, GUIAttachHandler)
                httpd.log_callback = self.log
                self.server_instance = httpd
                
                self.root.after(0, self.log, f"Starting server on port {PORT}...")
                self.root.after(0, self.server_started_ui)
                
                httpd.serve_forever()
            except OSError as e:
                if "Address already in use" in str(e):
                    self.root.after(0, self.log, f"Error: Port {PORT} is already in use!")
                    self.root.after(0, self.server_stopped_ui)
                else:
                    self.root.after(0, self.log, f"Error starting server: {e}")
                    self.root.after(0, self.server_stopped_ui)
            except Exception as e:
                self.root.after(0, self.log, f"Unexpected error: {e}")
                self.root.after(0, self.server_stopped_ui)
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
    
    def server_started_ui(self):
        """Update UI when server starts."""
        self.server_running = True
        self.update_ui()
        self.log("Server started successfully!")
        self.log("Ready to receive file attachments from Chrome extension")
    
    def stop_server(self):
        """Stop the server."""
        if not self.server_running or not self.server_instance:
            self.log("Server is not running!")
            return
        
        try:
            self.log("Stopping server...")
            self.server_instance.shutdown()
            self.server_instance = None
            self.server_running = False
            self.update_ui()
            self.log("Server stopped")
        except Exception as e:
            self.log(f"Error stopping server: {e}")
    
    def server_stopped_ui(self):
        """Update UI when server stops."""
        self.server_running = False
        self.update_ui()
    
    def update_ui(self):
        """Update the UI based on server status."""
        if self.server_running:
            self.status_label.config(text="Status: Running", foreground="green")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="Status: Stopped", foreground="red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def on_closing(self):
        """Handle window closing."""
        if self.server_running:
            self.stop_server()
            # Wait a bit for server to stop
            self.root.after(100, self.root.destroy)
        else:
            self.root.destroy()


def main():
    """Start the GUI application."""
    try:
        root = tk.Tk()
        app = ServerLauncher(root)
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = f"Failed to start application: {e}\n{traceback.format_exc()}"
        print(error_msg, file=sys.stderr)
        # Show error dialog
        try:
            import tkinter.messagebox
            error_root = tk.Tk()
            error_root.withdraw()
            tkinter.messagebox.showerror("Error", f"Failed to start application:\n{e}")
        except:
            pass
        sys.exit(1)


if __name__ == '__main__':
    main()
