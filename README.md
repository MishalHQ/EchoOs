<div align="center">

# 🎙️ EchoOS

### *Your Voice, Your Command*

**A hands-free, offline voice-controlled operating system interface**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/MishalHQ/EchoOs)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/MishalHQ/EchoOs)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Commands](#-voice-commands) • [Contributing](#-contributing)

---

</div>

## 🌟 Overview

**EchoOS** is an offline, voice-controlled operating system interface designed to provide **secure and hands-free system automation**. Unlike cloud-based voice assistants, EchoOS performs all speech recognition and authentication **locally**, ensuring privacy and usability even without internet connectivity.

### 🎯 Why EchoOS?

- 🔒 **100% Offline** - No internet required, complete privacy
- 🎤 **Voice Biometric Authentication** - Secure access using your unique voice
- ♿ **Accessibility First** - Perfect for users with mobility challenges
- 🚀 **OS-Level Control** - Full system automation capabilities
- 🔐 **Secure Environments** - Ideal for shared systems requiring controlled access

---

## ✨ Features

### 🔐 Security & Authentication
- **Voice Biometric Authentication** using Resemblyzer
- Session management with automatic timeout
- Failed attempt tracking and account lockout
- Local-only processing - no cloud dependencies

### 🎮 System Control
- **System Operations**: Shutdown, restart, sleep, lock screen
- **Volume Control**: Adjust volume, mute/unmute
- **System Monitoring**: Battery status, disk space, memory usage, CPU stats

### 📁 File Management
- Open, create, and delete files/folders
- Navigate directories with voice commands
- List files in current directory
- Context-aware file operations

### 🖥️ Application Control
- Launch any installed application
- Switch between open apps and browser tabs
- Close applications with voice commands
- Dynamic app discovery (no hardcoding!)

### 🌐 Web Operations
- Open websites by voice
- Search Google, YouTube, Amazon
- Browser tab management
- Web navigation commands

### 🎨 Advanced Features
- **OCR Screen Reading** - Understands what's on your screen
- **Context-Aware Execution** - Smart command interpretation
- **Media Control** - Play, pause, skip tracks
- **Text Operations** - Type, copy, paste, select all
- **Command Prompt Integration** - Execute terminal commands

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Microphone for voice input
- Tesseract OCR (optional, for screen reading)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/MishalHQ/EchoOs.git
cd EchoOs/EchoOS_PySide6

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (optional but recommended)
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr

# Run EchoOS
python main.py
```

---

## 🎤 Usage

### First Time Setup

1. **Register Your Voice**
   - Go to "User Manager" tab
   - Click "Register User"
   - Provide 3 voice samples (5 seconds each)

2. **Authenticate**
   - Click "Wake / Authenticate"
   - Speak clearly for 5 seconds
   - Wait for "Access granted"

3. **Start Using**
   - Click "Start Listening"
   - Speak your commands naturally

---

## 📋 Voice Commands

### System Control
```
"lock screen"          - Lock your computer
"shutdown"             - Shutdown system (10s delay)
"restart"              - Restart system
"volume up/down/mute"  - Control volume
"battery status"       - Check battery level
```

### File Operations
```
"open file [name]"     - Open a file
"create file [name]"   - Create new file
"delete file [name]"   - Delete file
"list files"           - Show files in directory
```

### Application Control
```
"open [app name]"      - Launch application
"close app"            - Close current app
"switch to [app]"      - Switch to specific app
"next app"             - Alt+Tab functionality
```

### Web & Search
```
"search [query]"       - Google search
"search youtube [query]" - YouTube search
"open website [url]"   - Open any website
```

### Media Control
```
"play/pause/stop"      - Media controls
"next/previous"        - Track navigation
```

[See full command list →](EchoOS_PySide6/README.md)

---

## 🏗️ Architecture

```
EchoOS/
├── 🎯 Voice Authentication (Resemblyzer)
├── 🎤 Speech Recognition (Vosk - Offline)
├── 🔊 Text-to-Speech (pyttsx3)
├── 👁️ Screen Analysis (OCR)
├── 🤖 Command Execution Engine
└── 🖥️ PySide6 GUI Interface
```

**Key Principles:**
- ✅ Everything discovered dynamically (no hardcoding)
- ✅ Cross-platform compatibility
- ✅ Privacy-first design
- ✅ Accessibility-focused

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **GUI Framework** | PySide6 |
| **Speech Recognition** | Vosk (Offline) |
| **Voice Authentication** | Resemblyzer |
| **Text-to-Speech** | pyttsx3 |
| **Screen Analysis** | Tesseract OCR, OpenCV |
| **UI Automation** | PyAutoGUI |
| **System Control** | psutil, platform-specific APIs |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🔧 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🎉 Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**M A Mohammed Mishal**

- GitHub: [@MishalHQ](https://github.com/MishalHQ)
- Email: mohammedmishal2004@gmail.com

---

## 🙏 Acknowledgments

- Original concept by [@Mohammed-Zaid-ZH](https://github.com/Mohammed-Zaid-ZH)
- Built with ❤️ for accessibility and privacy
- Inspired by the need for offline, secure voice control

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/MishalHQ/EchoOs?style=social)
![GitHub forks](https://img.shields.io/github/forks/MishalHQ/EchoOs?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/MishalHQ/EchoOs?style=social)

---

<div align="center">

### ⭐ Star this repo if you find it useful!

**Made with 🎤 and Python**

</div>
