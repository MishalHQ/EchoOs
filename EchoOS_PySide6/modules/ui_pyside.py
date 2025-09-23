from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
                               QListWidget, QHBoxLayout, QFileDialog, QMessageBox, QTabWidget,
                               QInputDialog, QTextEdit, QLineEdit, QFormLayout, QSlider)
from PySide6.QtCore import Qt, Signal, QThread
import json, os, webbrowser

class WorkerThread(QThread):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn; self.args = args; self.kwargs = kwargs
        self._result = None
    def run(self):
        try:
            self._result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            self._result = e
    def result(self):
        return self._result

class EchoMainWindow(QMainWindow):
    def __init__(self, auth, stt_mgr, app_disc, parser, executor, tts, accessibility=None):
        super().__init__()
        self.setWindowTitle("EchoOS - Enhanced Voice OS (PySide6)")
        self.resize(1000, 700)
        self.auth = auth
        self.stt_mgr = stt_mgr
        self.app_disc = app_disc
        self.parser = parser
        self.executor = executor
        self.tts = tts
        self.accessibility = accessibility
        self.components_loaded = False
        self._build_ui()

    def update_components(self, auth, stt_mgr, app_disc, parser, executor, accessibility):
        """Update components after background loading"""
        self.auth = auth
        self.stt_mgr = stt_mgr
        self.app_disc = app_disc
        self.parser = parser
        self.executor = executor
        self.accessibility = accessibility
        self.components_loaded = True
        print("✅ Components updated successfully!")

    def _build_ui(self):
        tabs = QTabWidget()
        tabs.addTab(self._dashboard_tab(), "Dashboard")
        tabs.addTab(self._users_tab(), "User Manager")
        tabs.addTab(self._apps_tab(), "App Catalog")
        tabs.addTab(self._accessibility_tab(), "Accessibility")
        tabs.addTab(self._settings_tab(), "Settings")
        self.setCentralWidget(tabs)
        self.status = self.statusBar()
        self.user_label = QLabel("User: -"); self.state_label = QLabel("State: Sleeping"); self.last_label = QLabel("Last: -")
        self.status.addPermanentWidget(self.user_label); self.status.addPermanentWidget(self.state_label); self.status.addPermanentWidget(self.last_label)

    def _dashboard_tab(self):
        w = QWidget(); layout = QVBoxLayout(); w.setLayout(layout)
        self.wake_btn = QPushButton("Wake / Authenticate"); self.wake_btn.clicked.connect(self.on_wake)
        self.sleep_btn = QPushButton("Sleep EchoOS"); self.sleep_btn.clicked.connect(self.on_sleep)
        self.listen_btn = QPushButton("Start Listening"); self.listen_btn.setCheckable(True); self.listen_btn.clicked.connect(self.on_listen)
        layout.addWidget(self.wake_btn); layout.addWidget(self.sleep_btn); layout.addWidget(self.listen_btn); layout.addStretch()
        return w

    def _users_tab(self):
        w = QWidget(); layout = QHBoxLayout(); w.setLayout(layout)
        self.users_list = QListWidget(); left = QVBoxLayout(); right = QVBoxLayout()
        left.addWidget(self.users_list); btn_reg = QPushButton("Register User"); btn_reg.clicked.connect(self.on_register)
        btn_rm = QPushButton("Remove Selected"); btn_rm.clicked.connect(self.on_remove); btn_refresh = QPushButton("Refresh"); btn_refresh.clicked.connect(self.refresh_users)
        right.addWidget(btn_reg); right.addWidget(btn_rm); right.addWidget(btn_refresh); layout.addLayout(left,3); layout.addLayout(right,1)
        self.refresh_users(); return w

    def _apps_tab(self):
        w = QWidget()
        layout = QVBoxLayout()
        w.setLayout(layout)
        
        # Header with discovery info
        header = QLabel("Comprehensive Application Discovery")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)
        
        # Discovery controls
        controls_layout = QHBoxLayout()
        self.btn_scan = QPushButton("🔍 Discover All Apps")
        self.btn_scan.clicked.connect(self.on_scan)
        self.btn_scan.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px; border-radius: 4px; }")
        
        self.btn_refresh = QPushButton("🔄 Refresh List")
        self.btn_refresh.clicked.connect(self.load_apps)
        self.btn_refresh.setStyleSheet("QPushButton { background-color: #2196F3; color: white; padding: 8px; border-radius: 4px; }")
        
        self.btn_open = QPushButton("📁 Open apps.json")
        self.btn_open.clicked.connect(lambda: webbrowser.open("file://"+os.path.abspath("config/apps.json")))
        self.btn_open.setStyleSheet("QPushButton { background-color: #FF9800; color: white; padding: 8px; border-radius: 4px; }")
        
        controls_layout.addWidget(self.btn_scan)
        controls_layout.addWidget(self.btn_refresh)
        controls_layout.addWidget(self.btn_open)
        layout.addLayout(controls_layout)
        
        # Status label
        self.apps_status = QLabel("Ready to discover applications...")
        self.apps_status.setStyleSheet("color: #666; margin: 5px;")
        layout.addWidget(self.apps_status)
        
        # Apps display
        self.apps_text = QTextEdit()
        self.apps_text.setReadOnly(True)
        self.apps_text.setStyleSheet("font-family: 'Consolas', monospace; font-size: 10px;")
        layout.addWidget(self.apps_text)
        
        # Load initial apps
        self.load_apps()
        return w

    def _accessibility_tab(self):
        w = QWidget(); layout = QVBoxLayout(); w.setLayout(layout)
        
        # Navigation controls
        nav_group = QWidget(); nav_layout = QHBoxLayout(); nav_group.setLayout(nav_layout)
        self.nav_mode_btn = QPushButton("Enable Navigation Mode"); self.nav_mode_btn.clicked.connect(self.toggle_navigation_mode)
        self.read_screen_btn = QPushButton("Read Screen"); self.read_screen_btn.clicked.connect(self.read_screen)
        self.describe_btn = QPushButton("Describe Screen"); self.describe_btn.clicked.connect(self.describe_screen)
        nav_layout.addWidget(self.nav_mode_btn); nav_layout.addWidget(self.read_screen_btn); nav_layout.addWidget(self.describe_btn)
        
        # Visual settings
        visual_group = QWidget(); visual_layout = QHBoxLayout(); visual_group.setLayout(visual_layout)
        self.high_contrast_btn = QPushButton("Toggle High Contrast"); self.high_contrast_btn.clicked.connect(self.toggle_high_contrast)
        self.large_text_btn = QPushButton("Toggle Large Text"); self.large_text_btn.clicked.connect(self.toggle_large_text)
        visual_layout.addWidget(self.high_contrast_btn); visual_layout.addWidget(self.large_text_btn)
        
        # Voice settings
        voice_group = QWidget(); voice_layout = QHBoxLayout(); voice_group.setLayout(voice_layout)
        self.voice_speed_label = QLabel("Voice Speed:"); self.voice_speed_slider = QSlider(Qt.Horizontal)
        self.voice_speed_slider.setRange(50, 200); self.voice_speed_slider.setValue(100)
        self.voice_speed_slider.valueChanged.connect(self.change_voice_speed)
        self.stop_tts_btn = QPushButton("Stop TTS"); self.stop_tts_btn.clicked.connect(self.stop_tts)
        voice_layout.addWidget(self.voice_speed_label); voice_layout.addWidget(self.voice_speed_slider); voice_layout.addWidget(self.stop_tts_btn)
        
        # Status display
        self.accessibility_status = QTextEdit(); self.accessibility_status.setMaximumHeight(100)
        self.status_btn = QPushButton("Check Status"); self.status_btn.clicked.connect(self.check_accessibility_status)
        self.help_btn = QPushButton("Accessibility Help"); self.help_btn.clicked.connect(self.show_accessibility_help)
        
        layout.addWidget(nav_group); layout.addWidget(visual_group); layout.addWidget(voice_group)
        layout.addWidget(self.accessibility_status); layout.addWidget(self.status_btn); layout.addWidget(self.help_btn)
        return w

    def _settings_tab(self):
        w = QWidget(); layout = QFormLayout(); w.setLayout(layout)
        self.model_path = QLineEdit("models/vosk-model-small-en-us-0.15"); btn_dl = QPushButton("Download Vosk Model"); btn_dl.clicked.connect(self.on_download)
        btn_open = QPushButton("Open config folder"); btn_open.clicked.connect(lambda: webbrowser.open(os.path.abspath("config")))
        layout.addRow("Model:", self.model_path); layout.addRow(btn_dl, btn_open); return w

    def on_wake(self):
        self.state_label.setText("State: Authenticating..."); self.tts.say("Please authenticate.")
        th = WorkerThread(self.auth.authenticate_interactive); th.start(); th.wait()
        res = th.result()
        if isinstance(res, Exception) or not res:
            QMessageBox.warning(self, "Auth", "Failed"); self.state_label.setText("State: Sleeping"); self.tts.say("Authentication failed")
        else:
            QMessageBox.information(self, "Auth", "Success"); self.state_label.setText("State: Active"); self.user_label.setText("User: authenticated"); self.tts.say("Welcome")

    def on_sleep(self):
        self.state_label.setText("State: Sleeping"); self.tts.say("Going to sleep")

    def on_listen(self, checked):
        if self.listen_btn.isChecked():
            self.listen_btn.setText("Stop Listening"); self.state_label.setText("State: Listening")
            self.stt_mgr.start_listening(self._stt_callback)
        else:
            self.listen_btn.setText("Start Listening"); self.state_label.setText("State: Active"); self.stt_mgr.stop_listening()

    def _stt_callback(self, text):
        self.last_label.setText("Last: "+text)
        
        try:
            # Load apps for command parsing
            apps = []
            try:
                with open("config/apps.json", "r") as f:
                    import json
                    data = json.load(f)
                    apps = data.get("apps", [])
            except Exception as e:
                print(f"Error loading apps: {e}")
                pass
                
            # Parse the command
            cmd = self.parser.parse(text, apps)
            if cmd is None:
                self.tts.say("Command not recognized")
                return
            
            # Execute the command
            th = WorkerThread(self.executor.execute, cmd)
            th.start()
            
        except Exception as e:
            print(f"STT callback error: {e}")
            self.tts.say("Sorry, I encountered an error processing that command")

    def on_register(self):
        name, ok = QInputDialog.getText(self, "Register", "Enter short username:")
        if not ok or not name: return
        self.tts.say("Recording samples now")
        th = WorkerThread(self.auth.register_user, name); th.start(); th.wait()
        res = th.result()
        if res: QMessageBox.information(self, "Register", "Registered"); self.refresh_users()
        else: QMessageBox.warning(self, "Register", "Failed")

    def on_remove(self):
        item = self.users_list.currentItem()
        if not item: return
        name = item.text()
        if QMessageBox.question(self, "Confirm", f"Remove {name}?") != QMessageBox.Yes: return
        th = WorkerThread(self.auth.remove_user, name); th.start(); th.wait(); self.refresh_users()

    def refresh_users(self):
        self.users_list.clear()
        for u in self.auth.load_users(): self.users_list.addItem(u)

    def on_scan(self):
        if not self.components_loaded:
            self.tts.say("Please wait, components are still loading...")
            self.apps_status.setText("⏳ Components loading... Please wait...")
            return
            
        self.tts.say("Starting comprehensive application discovery. This may take a few minutes.")
        self.apps_status.setText("🔍 Discovering applications... Please wait...")
        self.btn_scan.setEnabled(False)
        self.btn_scan.setText("⏳ Discovering...")
        
        def scan_complete():
            try:
                discovered_apps = self.app_disc.discover_and_save("config/apps.json")
                self.load_apps()
                self.apps_status.setText(f"✅ Discovery complete! Found {len(discovered_apps)} applications")
                self.tts.say(f"Application discovery complete. Found {len(discovered_apps)} applications on your system.")
                QMessageBox.information(self, "Discovery Complete", f"Found {len(discovered_apps)} applications!\n\nYou can now say 'open [app name]' to launch any discovered application.")
            except Exception as e:
                self.apps_status.setText(f"❌ Discovery failed: {str(e)}")
                self.tts.say("Application discovery failed. Please try again.")
                QMessageBox.critical(self, "Discovery Failed", f"Error: {str(e)}")
            finally:
                self.btn_scan.setEnabled(True)
                self.btn_scan.setText("🔍 Discover All Apps")
        
        th = WorkerThread(scan_complete)
        th.start()

    def load_apps(self):
        try:
            with open("config/apps.json","r",encoding="utf-8") as f: self.apps_text.setPlainText(f.read())
        except: self.apps_text.setPlainText("{}")

    def on_save_apps(self):
        try:
            with open("config/apps.json","w",encoding="utf-8") as f: f.write(self.apps_text.toPlainText()); QMessageBox.information(self,"Saved","Saved")
        except Exception as e:
            QMessageBox.critical(self,"Error",str(e))

    def on_download(self):
        from modules.stt import download_vosk_model
        path = self.model_path.text().strip()
        ok = download_vosk_model(path)
        QMessageBox.information(self, "Download", "Completed" if ok else "Failed")

    # Accessibility methods
    def toggle_navigation_mode(self):
        if self.accessibility:
            if self.accessibility.navigation_mode:
                self.accessibility.disable_navigation_mode()
                self.nav_mode_btn.setText("Enable Navigation Mode")
            else:
                self.accessibility.enable_navigation_mode()
                self.nav_mode_btn.setText("Disable Navigation Mode")

    def read_screen(self):
        if self.accessibility:
            self.accessibility.read_screen()

    def describe_screen(self):
        if self.accessibility:
            self.accessibility.describe_screen()

    def toggle_high_contrast(self):
        if self.accessibility:
            self.accessibility.toggle_high_contrast()

    def toggle_large_text(self):
        if self.accessibility:
            self.accessibility.toggle_large_text()

    def change_voice_speed(self, value):
        if self.accessibility:
            speed = value / 100.0  # Convert slider value to speed
            self.accessibility.set_voice_speed(speed)

    def check_accessibility_status(self):
        if self.accessibility:
            status = self.accessibility.get_accessibility_status()
            status_text = f"Navigation Mode: {'On' if status['navigation_mode'] else 'Off'}\n"
            status_text += f"Screen Reading: {'On' if status['screen_reading'] else 'Off'}\n"
            status_text += f"High Contrast: {'On' if status['high_contrast'] else 'Off'}\n"
            status_text += f"Large Text: {'On' if status['large_text'] else 'Off'}\n"
            status_text += f"Voice Speed: {status['voice_speed']:.1f}x"
            self.accessibility_status.setPlainText(status_text)

    def show_accessibility_help(self):
        if self.accessibility:
            self.accessibility.help_accessibility()

    def stop_tts(self):
        """Stop current TTS speech"""
        if self.tts:
            self.tts.stop_speaking()
            print("[TTS] Speech stopped by user")
