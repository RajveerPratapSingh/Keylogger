# 🔐 Keylogger Monitoring System

## 📘 Overview
**It captures keyboard input, encrypts the data, and transmits it securely to a local mock server for monitoring through a browser-based dashboard.**


## 🧠 Features
- 🔒 **End-to-End Encryption:** Uses AES-based **Fernet** encryption for all keystrokes.  
- 🧾 **Buffered Logging:** Collects multiple keystrokes before encrypting and sending.  
- 🖥️ **Live Dashboard:** View decrypted keystrokes in real-time via a local web server.  
- 🛑 **Kill Switch:** Press **F12** to stop the keylogger instantly.  
- 💾 **Local Encrypted Log File:** All recorded data is securely saved in `keylog.encrypted`.

---

## ⚙️ Tools & Libraries Used
- **Python 3.10+**
- [`cryptography`](https://pypi.org/project/cryptography/) – for encryption and decryption  
- [`pynput`](https://pypi.org/project/pynput/) – for keyboard event capture  
- [`requests`](https://pypi.org/project/requests/) – for sending data to the mock server  
- Built-in **`http.server`** – for serving the monitoring dashboard  

---

## 🧩 Project Structure
```
📁 Keylogger-Monitoring-System
│
├── images
├── crypto_utils.py      # Handles encryption and decryption
├── keylogger.py         # Captures keystrokes and sends data
├── mock_server.py       # Mock HTTP server to display decrypted data
└── Keylogger_Project_Report.pdf  # Project report (optional)
```


---

## 🚀 Usage Instructions

### 🖥️ Step 1: Start the Mock Server
```bash
python mock_server.py
```
- The server starts on **http://localhost:8080**
- It displays logs in real-time in a browser.

### ⌨️ Step 2: Start the Keylogger
Open another terminal window and run:
```bash
python keylogger.py
```

- It will start recording keyboard input.
- Press **F12** to stop the keylogger safely.
- Encrypted logs are saved in `keylog.encrypted`.

### 🌐 Step 3: View Logs
Open your browser and go to:
```
http://localhost:8080
```
You’ll see:
- A **status indicator** (“Active” or “Stopped”)
- A **live feed** of decrypted keystrokes
- Automatic refresh every 2 seconds

---

## 🧰 How It Works

1. **crypto_utils.py**
   - Generates an encryption key using Fernet.
   - Provides `encrypt_data()` and `decrypt_data()` functions.

2. **keylogger.py**
   - Captures keystrokes with timestamps.
   - Encrypts and saves them locally.
   - Sends encrypted logs to the mock server in small batches.

3. **mock_server.py**
   - Receives POST requests from the keylogger.
   - Decrypts the data using the same key.
   - Displays all received logs in a real-time HTML dashboard.

---
