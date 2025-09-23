#!/usr/bin/env python3
"""
EchoOS Fast Startup Version
Optimized for lightning-fast startup (2-3 seconds)
"""

import sys
import pathlib
import json
import pickle
import logging
import threading
import time
from datetime import datetime

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# Fast imports - only load what's needed for UI
from modules.ui_pyside import EchoMainWindow
from modules.tts import TTS

CONFIG_DIR = pathlib.Path("config")
CONFIG_DIR.mkdir(exist_ok=True)

# Create minimal configs if they don't exist
if not (CONFIG_DIR/"commands.json").exists():
    (CONFIG_DIR/"commands.json").write_text(json.dumps({
        "open": ["open","launch","start"],
        "open_website": ["open website","open site","go to"],
        "search_product": ["search product","find on amazon","search on amazon","search on swiggy","order on swiggy"],
        "send_whatsapp": ["send whatsapp","whatsapp"],
        "send_mail": ["send mail","send email","email"],
        "stop_listening": ["stop","sleep","go to sleep","stop listening","pause"],
        "wake_up": ["wake up","start listening","resume","start"],
    }, indent=2))

if not (CONFIG_DIR/"apps.json").exists():
    (CONFIG_DIR/"apps.json").write_text(json.dumps({"apps": []}, indent=2))

if not (CONFIG_DIR/"users.pkl").exists():
    with open(CONFIG_DIR/"users.pkl", "wb") as f:
        pickle.dump({}, f)

def main():
    print("🚀 EchoOS Fast Startup - Initializing...")
    start_time = time.time()
    
    # Setup minimal logging
    logging.basicConfig(
        level=logging.WARNING,  # Reduced logging for speed
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Initialize Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("EchoOS")
    app.setApplicationVersion("2.0")
    
    try:
        # Initialize only essential components for fast startup
        print("⚡ Initializing TTS...")
        tts = TTS()
        
        print("⚡ Creating main window...")
        # Create window with minimal components (will load others on demand)
        win = EchoMainWindow(None, None, None, None, None, tts, None)
        win.show()
        
        # Load heavy components in background
        def load_heavy_components():
            try:
                print("🔄 Loading heavy components in background...")
                
                # Import heavy modules
                from modules.auth import Authenticator
                from modules.app_discovery import AppDiscovery
                from modules.stt import VoskManager
                from modules.parser import CommandParser
                from modules.executor import Executor
                from modules.accessibility import AccessibilityManager
                
                # Initialize components
                auth = Authenticator(tts=tts)
                app_disc = AppDiscovery()
                stt_mgr = VoskManager(tts=tts)
                parser = CommandParser(tts=tts)
                executor = Executor(tts=tts, auth=auth)
                accessibility = AccessibilityManager(tts=tts)
                
                # Update window with loaded components
                win.update_components(auth, stt_mgr, app_disc, parser, executor, accessibility)
                
                # Start app discovery
                print("🔍 Starting app discovery...")
                discovered_apps = app_disc.discover_and_save("config/apps.json")
                print(f"✅ Discovery complete! Found {len(discovered_apps)} applications")
                
                # Update UI status
                if hasattr(win, 'apps_status'):
                    win.apps_status.setText(f"✅ Discovery complete! Found {len(discovered_apps)} applications")
                
                print("🎉 All components loaded successfully!")
                
            except Exception as e:
                print(f"❌ Error loading components: {e}")
                if hasattr(win, 'apps_status'):
                    win.apps_status.setText(f"❌ Error: {str(e)}")
        
        # Start background loading
        loading_thread = threading.Thread(target=load_heavy_components, daemon=True)
        loading_thread.start()
        
        startup_time = time.time() - start_time
        print(f"⚡ EchoOS started in {startup_time:.2f} seconds!")
        print("🎤 Voice commands will be available once components finish loading...")
        
        # Start the application
        try:
            sys.exit(app.exec())
        finally:
            print("👋 EchoOS shutdown complete")
        
    except Exception as e:
        print(f"❌ Failed to start EchoOS: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
