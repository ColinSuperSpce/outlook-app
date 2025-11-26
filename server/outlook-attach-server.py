#!/usr/bin/env python3
"""
Outlook Auto Attach Server
Receives file paths from Chrome extension and opens Outlook with file attached.
Supports both macOS (AppleScript) and Windows (COM automation).
"""

import http.server
import json
import sys
import os
import subprocess
import platform
import shutil
import tempfile
import re
from datetime import datetime

PORT = 8765


def create_unique_file_copy(original_path):
    """
    Create a unique copy of the file with a clean name format based on file type:
    - Files with 7-digit numbers → "Faktura-datum-tid.pdf"
    - Files with "Inköp" → "Order-datum-tid.pdf"
    - Files with "Orderbekräftelse" → "Orderbekräftelse-datum-tid.pdf"
    Includes microseconds to ensure uniqueness and avoid system-appended numbers.
    Returns the path to the unique copy.
    """
    if not os.path.exists(original_path):
        return None, f"File not found: {original_path}"
    
    try:
        original_name = os.path.basename(original_path)
        name_parts = os.path.splitext(original_name)
        file_extension = name_parts[1]
        
        home_dir = os.path.expanduser("~")
        desktop_dir = os.path.join(home_dir, "Desktop")
        businessnxtdocs_dir = os.path.join(desktop_dir, "businessnxtdocs")
                
        os.makedirs(businessnxtdocs_dir, exist_ok=True)
        
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d-%H%M%S")
        microseconds = now.strftime("%f")
        
        original_lower = original_name.lower()
        
        has_7digits = bool(re.search(r'\d{7}', original_name))
        has_inkop = 'inköp' in original_lower or 'inkop' in original_lower
        has_orderbekraeftelse = 'orderbekräftelse' in original_lower or 'orderbekr' in original_lower
                
        if has_7digits:
            base_name = "Faktura"
        elif has_inkop:
            base_name = "Order"
        else:
            base_name = "Orderbekräftelse"
        
        unique_name = f"{base_name}-{timestamp}-{microseconds}{file_extension}"
        unique_path = os.path.join(businessnxtdocs_dir, unique_name)
        
        shutil.copy2(original_path, unique_path)
        
        return unique_path, None
        
    except Exception as e:
        return None, f"Error creating unique copy: {str(e)}"


def open_outlook_mac(file_path):
    """Open Outlook on macOS using AppleScript and attach the file."""
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    try:
        file_path = os.path.abspath(file_path)
        
        script = f'''
        tell application "Microsoft Outlook"
            activate
            set newMessage to make new outgoing message
            tell newMessage
                make new attachment with properties {{file:POSIX file "{file_path}"}}
            end tell
            open newMessage
        end tell
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return True, "Outlook opened successfully"
        else:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            return False, f"AppleScript error: {error_msg}"
            
    except subprocess.TimeoutExpired:
        return False, "Timeout opening Outlook"
    except Exception as e:
        return False, f"Error: {str(e)}"


def open_outlook_windows(file_path):
    """Open Outlook on Windows using COM automation and attach the file."""
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    try:
        import win32com.client
        
        file_path = os.path.abspath(file_path)
        file_path = file_path.replace('/', '\\')
        
        outlook = win32com.client.Dispatch("Outlook.Application")
        
        mail_item = outlook.CreateItem(0)
        
        mail_item.Attachments.Add(file_path)
        
        mail_item.Display()
        
        return True, "Outlook opened successfully"
        
    except ImportError:
        return False, "pywin32 not installed"
    except Exception as e:
        return False, f"Error: {str(e)}"


class AttachHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for /attach endpoint."""
    
    def log_message(self, format, *args):
        """Override to use custom log format with timestamp."""
        timestamp = datetime.now().strftime("[%d/%b/%Y %H:%M:%S]")
        sys.stderr.write(f"{timestamp} {format % args}\n")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests to /attach endpoint."""
        if self.path != '/attach':
            self.send_response(404)
            self.end_headers()
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode('utf-8'))
            file_path = data.get('filePath')
            
            if not file_path:
                self.send_error_response(400, "Missing filePath in request")
                return
            
            unique_file_path, copy_error = create_unique_file_copy(file_path)
            if not unique_file_path:
                self.send_error_response(500, copy_error or "Failed to create unique file copy")
                return
            
            file_to_attach = unique_file_path
            
            system = platform.system()
            if system == 'Darwin':
                success, message = open_outlook_mac(file_to_attach)
            elif system == 'Windows':
                success, message = open_outlook_windows(file_to_attach)
            else:
                self.send_error_response(400, f"Unsupported platform: {system}")
                return
            
            response_data = {
                'success': success,
                'message': message
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
            status = "Success" if success else "Failed"
            original_filename = os.path.basename(file_path)
            unique_filename = os.path.basename(file_to_attach)
            self.log_message(f"Attached file: {original_filename} (unique: {unique_filename}) - {status}: {success}")
            
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON in request body")
        except Exception as e:
            self.send_error_response(500, f"Internal server error: {str(e)}")
    
    def send_error_response(self, status_code, message):
        """Send an error response with JSON body."""
        response_data = {
            'success': False,
            'message': message
        }
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
    
    def do_GET(self):
        """Handle GET requests - return simple status."""
        if self.path == '/' or self.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Outlook Auto Attach Server is running')
        else:
            self.send_response(404)
            self.end_headers()


def main():
    """Start the HTTP server."""
    server_address = ('127.0.0.1', PORT)
    httpd = http.server.HTTPServer(server_address, AttachHandler)
    
    print(f"Outlook Auto Attach server started on http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.shutdown()


if __name__ == '__main__':
    main()

