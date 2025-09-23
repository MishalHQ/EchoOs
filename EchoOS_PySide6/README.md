# EchoOS - Enhanced Voice-Controlled Operating System

EchoOS is an offline, Python-based voice-controlled operating environment designed to automate operating system tasks through natural speech commands, eliminating reliance on physical input devices or internet-based assistants. This enhanced version implements all the objectives specified in the project report.

## 🎯 Project Objectives Achieved

### ✅ Secure Multi-User Voice Authentication
- **Resemblyzer Integration**: Advanced speaker recognition using Resemblyzer for secure voice authentication
- **Session Management**: Secure session-based authentication with automatic timeout
- **Multi-User Support**: Support for multiple users with individual voice profiles
- **Security Features**: Failed attempt tracking, account lockout, and secure session storage

### ✅ Comprehensive Voice Command Recognition
- **System Control**: Shutdown, restart, sleep, lock screen, logout
- **File Operations**: Open, create, delete, copy, move, rename files and folders
- **Application Control**: Launch, close, minimize, maximize applications
- **Web Operations**: Open websites, search Google, YouTube, Amazon, Swiggy
- **System Information**: Battery status, disk space, memory usage, CPU usage
- **Accessibility Commands**: Screen reading, navigation, clicking, scrolling, zooming

### ✅ OS-Level Control and Automation
- **File Management**: Complete file system navigation and manipulation
- **Process Control**: System process monitoring and control
- **Hardware Control**: Volume control, display settings, power management
- **Cross-Platform**: Windows, macOS, and Linux support

### ✅ Accessibility Features for Differently-Abled Users
- **Screen Reading**: OCR-based screen content reading
- **Voice Navigation**: Hands-free cursor and interface navigation
- **Visual Accessibility**: High contrast and large text modes
- **Voice Control**: Complete system control through voice commands
- **Assistive Technology**: Integration with accessibility APIs

### ✅ Privacy and Security
- **Offline Operation**: Complete offline functionality, no internet required
- **Data Privacy**: All voice data processed locally
- **Secure Authentication**: Multi-factor voice authentication
- **Session Security**: Encrypted session management

### ✅ Modular and Extensible Architecture
- **Plugin System**: Easy addition of new voice commands
- **Modular Design**: Separate modules for each functionality
- **Configuration Management**: JSON-based configuration system
- **Logging System**: Comprehensive logging for debugging and monitoring

## 🚀 Key Features

### Voice Authentication
- **Resemblyzer-based**: Advanced speaker recognition
- **Multiple Samples**: 3 voice samples per user for accuracy
- **Session Management**: 30-minute session timeout
- **Security**: Failed attempt tracking and lockout

### Voice Commands
- **System Control**: "shutdown", "restart", "sleep", "lock screen"
- **File Operations**: "open file", "create file", "delete file", "list files"
- **App Control**: "open [app name]", "close app", "minimize"
- **Web Search**: "search google for [query]", "open website [url]"
- **System Info**: "system info", "battery status", "disk space"
- **Accessibility**: "read screen", "navigate up", "click", "scroll down"

### Accessibility Features
- **Screen Reading**: OCR-based text extraction and reading
- **Voice Navigation**: Hands-free cursor movement
- **Visual Modes**: High contrast and large text support
- **Voice Speed Control**: Adjustable TTS speed
- **Navigation Mode**: Dedicated voice navigation mode

### Security Features
- **Offline Operation**: No internet connection required
- **Local Processing**: All voice data processed locally
- **Encrypted Storage**: Secure user profile storage
- **Session Management**: Automatic session cleanup

## 📋 Requirements

### Core Dependencies
```
PySide6
vosk
sounddevice
pyttsx3
python_speech_features
numpy
scipy
rapidfuzz
pywin32 (Windows only)
```

### Enhanced Dependencies
```
resemblyzer
librosa
scikit-learn
psutil
pathlib
shutil
threading
json
pickle
datetime
logging
```

### Optional Dependencies (for full accessibility)
```
pyautogui
opencv-python
pytesseract
Pillow
pygetwindow
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd EchoOS_PySide6
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Vosk Model** (if not already present)
   ```bash
   python -c "from modules.stt import download_vosk_model; download_vosk_model('models/vosk-model-small-en-us-0.15')"
   ```

4. **Run EchoOS**
   ```bash
   python main.py
   ```

## 🎮 Usage

### Initial Setup
1. **Launch EchoOS**: Run `python main.py`
2. **Register User**: Go to "User Manager" tab and register your voice
3. **Authenticate**: Click "Wake / Authenticate" to log in
4. **Start Listening**: Click "Start Listening" to begin voice commands

### Voice Commands

#### System Control
- "shutdown" - Shutdown the system
- "restart" - Restart the system
- "sleep" - Put system to sleep
- "lock screen" - Lock the screen
- "log out" - Logout current user

#### File Operations
- "open file [filename]" - Open a file
- "create file [filename]" - Create a new file
- "delete file [filename]" - Delete a file
- "list files" - List files in current directory
- "navigate to [directory]" - Change directory
- "create folder [name]" - Create a new folder

#### Application Control
- "open [app name]" - Launch an application
- "close all tabs" - Close all applications (keeps EchoOS)
- "close chrome tabs" - Close only Chrome browser
- "close firefox tabs" - Close only Firefox browser
- "close edge tabs" - Close only Edge browser
- "close paint" - Close only Microsoft Paint
- "close word" - Close only Microsoft Word
- "close excel" - Close only Microsoft Excel
- "close powerpoint" - Close only Microsoft PowerPoint
- "close notepad" - Close only Notepad
- "close app" - Close current application
- "minimize" - Minimize current window
- "maximize" - Maximize current window

#### Web Operations
- "open website [url]" - Open a website
- "search google for [query]" - Search Google
- "search youtube for [query]" - Search YouTube
- "search amazon for [query]" - Search Amazon

#### System Information
- "system info" - Get system information
- "battery status" - Check battery status
- "disk space" - Check disk usage
- "memory usage" - Check memory usage
- "cpu usage" - Check CPU usage

#### Accessibility
- "read screen" - Read screen content
- "describe screen" - Describe screen layout
- "navigate up/down/left/right" - Move cursor
- "click" - Left click
- "double click" - Double click
- "right click" - Right click
- "scroll up/down" - Scroll
- "zoom in/out" - Zoom
- "high contrast" - Toggle high contrast
- "large text" - Toggle large text

## 🏗️ Project Structure

```
EchoOS_PySide6/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This documentation
├── close_commands_guide.md # Close commands reference
├── config/                # Configuration files
│   ├── apps.json          # Discovered applications
│   ├── commands.json      # Voice command patterns
│   ├── sessions.pkl       # User sessions
│   └── users.pkl          # User voice profiles
├── modules/               # Core modules
│   ├── accessibility.py   # Accessibility features
│   ├── app_discovery.py   # Application discovery
│   ├── auth.py           # Voice authentication
│   ├── executor.py       # Command execution
│   ├── parser.py         # Command parsing
│   ├── stt.py            # Speech-to-text
│   ├── tts.py            # Text-to-speech
│   └── ui_pyside.py      # PySide6 GUI
├── models/                # Vosk speech model
│   └── vosk-model-small-en-us-0.15/
└── venv/                  # Virtual environment (optional)
```

### Core Modules
- **main.py**: Application entry point and initialization
- **ui_pyside.py**: PySide6-based GUI interface
- **stt.py**: Speech-to-text using Vosk
- **tts.py**: Text-to-speech using pyttsx3
- **auth.py**: Voice authentication using Resemblyzer
- **parser.py**: Voice command parsing and recognition
- **executor.py**: Command execution and OS integration
- **app_discovery.py**: Application discovery and cataloging
- **accessibility.py**: Accessibility features and screen reading

### Configuration Files
- **config/commands.json**: Voice command patterns
- **config/apps.json**: Discovered applications
- **config/users.pkl**: User voice profiles
- **config/sessions.pkl**: Active user sessions

## 🔧 Configuration

### Voice Commands
Edit `config/commands.json` to add or modify voice command patterns:

```json
{
  "system_control": ["shutdown", "restart", "sleep"],
  "file_operations": ["open file", "create file", "delete file"],
  "accessibility": ["read screen", "navigate", "click"]
}
```

### Application Discovery
The system automatically discovers installed applications and stores them in `config/apps.json`. You can manually edit this file to add custom applications.

## 🐛 Troubleshooting

### Common Issues

1. **Vosk Model Not Found**
   - Download the model using the built-in downloader
   - Ensure the model path is correct in settings

2. **Voice Recognition Not Working**
   - Check microphone permissions
   - Ensure good audio quality
   - Try adjusting the microphone sensitivity

3. **Authentication Fails**
   - Ensure you've registered your voice properly
   - Speak clearly and at normal volume
   - Try re-registering with multiple samples

4. **Accessibility Features Not Working**
   - Install optional dependencies (pyautogui, opencv-python, pytesseract)
   - Check system permissions for screen access

### Logs
Check `echoos.log` for detailed error messages and debugging information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Vosk**: Offline speech recognition
- **Resemblyzer**: Speaker verification
- **PySide6**: GUI framework
- **pyttsx3**: Text-to-speech synthesis
- **psutil**: System information
- **OpenCV & Tesseract**: OCR capabilities

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the logs for error details

---

**EchoOS v2.0** - Enhanced Voice-Controlled Operating System
*Complete offline operation with comprehensive accessibility features*