import os
import sys
import subprocess
import webbrowser
import random
import shutil
import psutil
import platform
import time
import logging
from pathlib import Path
from datetime import datetime

class Executor:
    def __init__(self, tts, auth=None):
        self.tts = tts
        self.auth = auth
        self.current_directory = os.getcwd()
        self.logger = logging.getLogger(__name__)

    def execute(self, command):
        """Execute a command based on action dictionary"""
        if not command or 'action' not in command:
            return False
        
        action = command['action']
        
        try:
            if action == "open_app":
                return self.open_app(command.get('app', {}).get('exec', ''), 
                                   command.get('app', {}).get('name', 'Unknown App'))
            elif action == "close_all_apps":
                return self.close_all_apps()
            elif action == "close_browser_tabs":
                return self.close_browser_tabs(command.get('browser', 'all'))
            elif action == "close_specific_app":
                return self.close_specific_app(command.get('app', ''))
            elif action == "new_tab":
                return self.new_tab()
            elif action == "new_window":
                return self.new_window()
            elif action == "switch_to_app":
                return self.switch_to_app(command.get('app_name', ''))
            elif action == "close_all_tabs":
                return self.close_all_tabs()
            elif action == "open_website":
                return self.open_website(command.get('url', ''))
            elif action == "search_google":
                return self.search_google(command.get('query', ''))
            elif action == "search_youtube":
                return self.search_youtube(command.get('query', ''))
            elif action == "search_amazon":
                return self.search_amazon(command.get('query', ''))
            elif action == "search_swiggy":
                return self.search_swiggy(command.get('query', ''))
            elif action == "open_file":
                return self.open_file(command.get('filename', ''))
            elif action == "create_file":
                return self.create_file(command.get('filename', ''))
            elif action == "delete_file":
                return self.delete_file(command.get('filename', ''), command.get('confirm', False))
            elif action == "list_files":
                return self.list_files(command.get('directory', ''))
            elif action == "change_directory":
                return self.change_directory(command.get('directory', ''))
            elif action == "system_info":
                return self.get_system_info()
            elif action == "battery_status":
                return self.get_battery_status()
            elif action == "disk_space":
                return self.get_disk_space()
            elif action == "memory_usage":
                return self.get_memory_usage()
            elif action == "cpu_usage":
                return self.get_cpu_usage()
            elif action == "volume_up":
                return self.volume_up()
            elif action == "volume_down":
                return self.volume_down()
            elif action == "mute":
                return self.mute()
            elif action == "shutdown":
                return self.shutdown(command.get('confirm', False))
            elif action == "restart":
                return self.restart(command.get('confirm', False))
            elif action == "sleep":
                return self.sleep()
            elif action == "lock_screen":
                return self.lock_screen()
            elif action == "logout":
                return self.logout()
            elif action == "wake":
                return self.wake()
            elif action == "pause_listening":
                return self.pause_listening()
            else:
                self.tts.say("I don't know how to handle that command.")
                return False
                
        except Exception as e:
            self.logger.error(f"Error executing command {action}: {e}")
            self.tts.say(f"Sorry, I encountered an error: {str(e)}")
            return False

    def open_app(self, app_path, app_name):
        # Check if application is already running
        if self._is_app_running(app_name, app_path):
            return self._handle_running_app(app_name, app_path)
        
        # Launch new instance
        responses = [
            f"Right away, sir. Launching {app_name}.",
            f"As you wish. Opening {app_name}.",
            f"Certainly. Starting {app_name} now."
        ]
        self.tts.say(random.choice(responses))

        try:
            if os.name == "nt":  # Windows
                os.startfile(app_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(["open", app_path])
            else:  # Linux
                subprocess.Popen([app_path])
        except Exception as e:
            self.tts.say(f"Apologies, I could not start {app_name}. Error: {e}")

    def _is_app_running(self, app_name, app_path):
        """Check if an application is already running"""
        try:
            import psutil
            
            # Get the executable name from the path
            exe_name = os.path.basename(app_path).lower()
            
            # Check running processes
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    proc_name = proc.info['name'].lower() if proc.info['name'] else ""
                    proc_exe = proc.info['exe'].lower() if proc.info['exe'] else ""
                    
                    # Check if process matches our app
                    if (exe_name in proc_name or 
                        exe_name in proc_exe or 
                        app_name.lower() in proc_name):
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            return False
            
        except ImportError:
            # Fallback: try using tasklist on Windows
            if os.name == "nt":
                try:
                    result = subprocess.run(
                        ["tasklist", "/FI", f"IMAGENAME eq {exe_name}"],
                        capture_output=True, text=True
                    )
                    return exe_name in result.stdout.lower()
                except:
                    return False
            return False
        except Exception:
            return False

    def _handle_running_app(self, app_name, app_path):
        """Handle when application is already running"""
        # Special handling for browsers
        browser_apps = {
            'chrome': self._open_new_browser_tab,
            'firefox': self._open_new_browser_tab,
            'edge': self._open_new_browser_tab,
            'safari': self._open_new_browser_tab,
            'opera': self._open_new_browser_tab
        }
        
        app_lower = app_name.lower()
        for browser, handler in browser_apps.items():
            if browser in app_lower:
                return handler(app_name)
        
        # For other applications, try to bring to front or open new instance
        return self._bring_app_to_front(app_name, app_path)

    def _open_new_browser_tab(self, browser_name):
        """Open a new tab in the running browser"""
        try:
            import pyautogui
            
            self.tts.say(f"Opening a new tab in {browser_name}.")
            
            # Give user time to switch to browser if needed
            time.sleep(1)
            
            # Use Ctrl+T to open new tab
            pyautogui.hotkey('ctrl', 't')
            
            return True
            
        except ImportError:
            # Fallback: launch new instance
            self.tts.say(f"{browser_name} is already running. Opening a new window.")
            return False
        except Exception as e:
            self.tts.say(f"Could not open new tab in {browser_name}. Error: {e}")
            return False

    def _bring_app_to_front(self, app_name, app_path):
        """Try to bring the running application to the front"""
        try:
            import pyautogui
            
            self.tts.say(f"{app_name} is already running. Bringing it to the front.")
            
            # Try to find and click on the app window
            windows = pyautogui.getWindowsWithTitle(app_name)
            if windows:
                windows[0].activate()
                return True
            else:
                # Fallback: use Alt+Tab to cycle through windows
                pyautogui.hotkey('alt', 'tab')
                return True
                
        except ImportError:
            self.tts.say(f"{app_name} is already running. Please switch to it manually.")
            return False
        except Exception as e:
            self.tts.say(f"Could not bring {app_name} to front. Error: {e}")
            return False

    def open_website(self, url):
        responses = [
            f"Opening {url} for you, sir.",
            f"Certainly. Here is {url}.",
            f"As requested, launching {url}."
        ]
        self.tts.say(random.choice(responses))
        webbrowser.open(url)

    def search_amazon(self, query):
        url = f"https://www.amazon.in/s?k={query}"
        self.tts.say(f"Searching Amazon for {query}, sir.")
        webbrowser.open(url)

    def search_swiggy(self, query):
        url = f"https://www.swiggy.com/search?query={query}"
        self.tts.say(f"Searching Swiggy for {query}, sir.")
        webbrowser.open(url)

    def send_whatsapp(self):
        self.tts.say("Opening WhatsApp Web. Please wait.")
        webbrowser.open("https://web.whatsapp.com")

    def send_email(self):
        self.tts.say("Opening your email client, sir.")
        webbrowser.open("mailto:")

    def search_google(self, query):
        """Search Google"""
        if not query:
            self.tts.say("What would you like me to search for?")
            return False
        url = f"https://www.google.com/search?q={query}"
        self.tts.say(f"Searching Google for {query}.")
        webbrowser.open(url)
        return True

    def search_youtube(self, query):
        """Search YouTube"""
        if not query:
            self.tts.say("What would you like me to search for on YouTube?")
            return False
        url = f"https://www.youtube.com/results?search_query={query}"
        self.tts.say(f"Searching YouTube for {query}.")
        webbrowser.open(url)
        return True

    def open_file(self, filename):
        """Open a file with the default application"""
        if not filename:
            self.tts.say("I need a filename to open.")
            return False
            
        file_path = os.path.join(self.current_directory, filename)
        if not os.path.exists(file_path):
            self.tts.say(f"File {filename} not found.")
            return False
            
        try:
            if os.name == "nt":  # Windows
                os.startfile(file_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(["open", file_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", file_path])
            self.tts.say(f"Opening {filename}.")
            return True
        except Exception as e:
            self.tts.say(f"Could not open {filename}. Error: {e}")
            return False

    def create_file(self, filename):
        """Create a new file"""
        if not filename:
            self.tts.say("I need a filename to create.")
            return False
            
        file_path = os.path.join(self.current_directory, filename)
        try:
            with open(file_path, 'w') as f:
                f.write("")
            self.tts.say(f"Created file {filename}.")
            return True
        except Exception as e:
            self.tts.say(f"Could not create {filename}. Error: {e}")
            return False

    def delete_file(self, filename, confirm=False):
        """Delete a file"""
        if not filename:
            self.tts.say("I need a filename to delete.")
            return False
            
        file_path = os.path.join(self.current_directory, filename)
        if not os.path.exists(file_path):
            self.tts.say(f"File {filename} not found.")
            return False
            
        if confirm:
            self.tts.say(f"Are you sure you want to delete {filename}? Say yes to confirm.")
            
        try:
            os.remove(file_path)
            self.tts.say(f"Deleted {filename}.")
            return True
        except Exception as e:
            self.tts.say(f"Could not delete {filename}. Error: {e}")
            return False

    def list_files(self, directory=None):
        """List files in a directory"""
        target_dir = directory if directory else self.current_directory
        target_path = os.path.join(self.current_directory, target_dir) if directory else self.current_directory
        
        if not os.path.exists(target_path):
            self.tts.say(f"Directory {target_dir} not found.")
            return False
            
        try:
            files = os.listdir(target_path)
            if not files:
                self.tts.say("The directory is empty.")
                return True
                
            file_list = []
            for file in files[:10]:  # Limit to first 10 files
                file_path = os.path.join(target_path, file)
                if os.path.isdir(file_path):
                    file_list.append(f"{file} (folder)")
                else:
                    file_list.append(file)
            
            files_text = ", ".join(file_list)
            if len(files) > 10:
                files_text += f" and {len(files) - 10} more files"
                
            self.tts.say(f"Files in {target_dir}: {files_text}")
            return True
        except Exception as e:
            self.tts.say(f"Could not list files. Error: {e}")
            return False

    def change_directory(self, directory):
        """Change current directory"""
        if not directory:
            self.tts.say("I need a directory name.")
            return False
            
        target_path = os.path.join(self.current_directory, directory)
        if not os.path.exists(target_path):
            self.tts.say(f"Directory {directory} not found.")
            return False
            
        if not os.path.isdir(target_path):
            self.tts.say(f"{directory} is not a directory.")
            return False
            
        try:
            self.current_directory = target_path
            self.tts.say(f"Changed to directory {directory}.")
            return True
        except Exception as e:
            self.tts.say(f"Could not change directory. Error: {e}")
            return False

    def get_system_info(self):
        """Get system information"""
        try:
            info = {
                "Platform": platform.platform(),
                "System": platform.system(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor(),
                "Python": platform.python_version()
            }
            
            info_text = f"System: {info['System']} {info['Release']}, "
            info_text += f"Architecture: {info['Machine']}, "
            info_text += f"Python: {info['Python']}"
            
            self.tts.say(info_text)
            return True
        except Exception as e:
            self.tts.say(f"Could not get system info. Error: {e}")
            return False

    def get_battery_status(self):
        """Get battery status"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = "plugged in" if battery.power_plugged else "not plugged in"
                self.tts.say(f"Battery is at {percent}% and {plugged}.")
            else:
                self.tts.say("Battery information not available.")
            return True
        except Exception as e:
            self.tts.say(f"Could not get battery status. Error: {e}")
            return False

    def get_disk_space(self):
        """Get disk space information"""
        try:
            disk_usage = psutil.disk_usage('/')
            total = disk_usage.total // (1024**3)  # Convert to GB
            used = disk_usage.used // (1024**3)
            free = disk_usage.free // (1024**3)
            
            self.tts.say(f"Disk space: {used} GB used, {free} GB free out of {total} GB total.")
            return True
        except Exception as e:
            self.tts.say(f"Could not get disk space. Error: {e}")
            return False

    def get_memory_usage(self):
        """Get memory usage information"""
        try:
            memory = psutil.virtual_memory()
            total = memory.total // (1024**3)  # Convert to GB
            available = memory.available // (1024**3)
            percent = memory.percent
            
            self.tts.say(f"Memory usage: {percent}% used, {available} GB available out of {total} GB total.")
            return True
        except Exception as e:
            self.tts.say(f"Could not get memory usage. Error: {e}")
            return False

    def get_cpu_usage(self):
        """Get CPU usage information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            self.tts.say(f"CPU usage: {cpu_percent}% across {cpu_count} cores.")
            return True
        except Exception as e:
            self.tts.say(f"Could not get CPU usage. Error: {e}")
            return False

    def volume_up(self):
        """Increase system volume"""
        try:
            if os.name == "nt":  # Windows
                subprocess.run(["powershell", "-c", "(New-Object -comObject WScript.Shell).SendKeys([char]175)"])
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
            else:  # Linux
                subprocess.run(["amixer", "set", "Master", "10%+"])
            self.tts.say("Volume increased.")
            return True
        except Exception as e:
            self.tts.say(f"Could not increase volume. Error: {e}")
            return False

    def volume_down(self):
        """Decrease system volume"""
        try:
            if os.name == "nt":  # Windows
                subprocess.run(["powershell", "-c", "(New-Object -comObject WScript.Shell).SendKeys([char]174)"])
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
            else:  # Linux
                subprocess.run(["amixer", "set", "Master", "10%-"])
            self.tts.say("Volume decreased.")
            return True
        except Exception as e:
            self.tts.say(f"Could not decrease volume. Error: {e}")
            return False

    def mute(self):
        """Mute system volume"""
        try:
            if os.name == "nt":  # Windows
                subprocess.run(["powershell", "-c", "(New-Object -comObject WScript.Shell).SendKeys([char]173)"])
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["osascript", "-e", "set volume output volume 0"])
            else:  # Linux
                subprocess.run(["amixer", "set", "Master", "mute"])
            self.tts.say("Volume muted.")
            return True
        except Exception as e:
            self.tts.say(f"Could not mute volume. Error: {e}")
            return False

    def shutdown(self, confirm=False):
        """Shutdown the system"""
        if confirm:
            self.tts.say("Are you sure you want to shutdown? Say yes to confirm.")
            
        try:
            if os.name == "nt":  # Windows
                subprocess.run(["shutdown", "/s", "/t", "10"])
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["sudo", "shutdown", "-h", "now"])
            else:  # Linux
                subprocess.run(["sudo", "shutdown", "-h", "now"])
            self.tts.say("System will shutdown in 10 seconds.")
            return True
        except Exception as e:
            self.tts.say(f"Could not shutdown system. Error: {e}")
            return False

    def restart(self, confirm=False):
        """Restart the system"""
        if confirm:
            self.tts.say("Are you sure you want to restart? Say yes to confirm.")
            
        try:
            if os.name == "nt":  # Windows
                subprocess.run(["shutdown", "/r", "/t", "10"])
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["sudo", "shutdown", "-r", "now"])
            else:  # Linux
                subprocess.run(["sudo", "shutdown", "-r", "now"])
            self.tts.say("System will restart in 10 seconds.")
            return True
        except Exception as e:
            self.tts.say(f"Could not restart system. Error: {e}")
            return False

    def sleep(self):
        """Put system to sleep"""
        try:
            if os.name == "nt":  # Windows
                subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["pmset", "sleepnow"])
            else:  # Linux
                subprocess.run(["systemctl", "suspend"])
            self.tts.say("System going to sleep.")
            return True
        except Exception as e:
            self.tts.say(f"Could not put system to sleep. Error: {e}")
            return False

    def lock_screen(self):
        """Lock the screen"""
        try:
            if os.name == "nt":  # Windows
                subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["pmset", "displaysleepnow"])
            else:  # Linux
                subprocess.run(["gnome-screensaver-command", "-l"])
            self.tts.say("Screen locked.")
            return True
        except Exception as e:
            self.tts.say(f"Could not lock screen. Error: {e}")
            return False

    def logout(self):
        """Logout current user"""
        if self.auth:
            self.auth.logout()
        else:
            self.tts.say("Logging out.")
        return True

    def wake(self):
        """Wake up the system"""
        self.tts.say("I am back online. At your service.")
        return True

    def pause_listening(self):
        """Pause voice listening"""
        self.tts.say("Going to sleep. Call me when you need me.")
        return True

    def close_all_apps(self):
        """Close all applications except EchoOS"""
        try:
            self.tts.say("Closing all applications except EchoOS. This will close Paint, Word, Excel, browsers, and other apps.")
            
            if os.name == "nt":  # Windows
                # Close common applications
                apps_to_close = [
                    "mspaint.exe", "winword.exe", "excel.exe", "powerpnt.exe", "notepad.exe",
                    "chrome.exe", "firefox.exe", "msedge.exe", "iexplore.exe",
                    "calc.exe", "explorer.exe"  # Note: explorer.exe will restart automatically
                ]
                
                for app in apps_to_close:
                    try:
                        subprocess.run(["taskkill", "/f", "/im", app], capture_output=True)
                    except:
                        pass
                
                self.tts.say("All applications have been closed. EchoOS remains active.")
                return True
                
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["pkill", "-f", "Google Chrome"], capture_output=True)
                subprocess.run(["pkill", "-f", "Firefox"], capture_output=True)
                subprocess.run(["pkill", "-f", "Safari"], capture_output=True)
                subprocess.run(["pkill", "-f", "TextEdit"], capture_output=True)
                subprocess.run(["pkill", "-f", "Preview"], capture_output=True)
                
                self.tts.say("All applications have been closed. EchoOS remains active.")
                return True
                
            else:  # Linux
                subprocess.run(["pkill", "-f", "chrome"], capture_output=True)
                subprocess.run(["pkill", "-f", "firefox"], capture_output=True)
                subprocess.run(["pkill", "-f", "libreoffice"], capture_output=True)
                subprocess.run(["pkill", "-f", "gedit"], capture_output=True)
                
                self.tts.say("All applications have been closed. EchoOS remains active.")
                return True
                
        except Exception as e:
            self.tts.say(f"Could not close all applications. Error: {e}")
            return False

    def close_browser_tabs(self, browser="all"):
        """Close specific browser tabs"""
        try:
            if browser == "all":
                self.tts.say("Closing all browser tabs. Please switch to your browser window first.")
            else:
                self.tts.say(f"Closing {browser} tabs. Please switch to your {browser} window first.")
            
            # Use keyboard shortcuts to close tabs safely
            try:
                import pyautogui
                
                # Give user time to switch to browser
                time.sleep(2)
                
                # Close all tabs using Ctrl+W (close tab) repeatedly
                for i in range(10):  # Try up to 10 times
                    pyautogui.hotkey('ctrl', 'w')
                    time.sleep(0.2)
                
                # Alternative: Close all tabs at once with Ctrl+Shift+W (close all tabs)
                pyautogui.hotkey('ctrl', 'shift', 'w')
                
                self.tts.say(f"{browser.title()} tabs have been closed using keyboard shortcuts.")
                return True
                
            except ImportError:
                # Fallback: Use process killing for specific browser
                if browser == "chrome":
                    subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], capture_output=True)
                elif browser == "firefox":
                    subprocess.run(["taskkill", "/f", "/im", "firefox.exe"], capture_output=True)
                elif browser == "edge":
                    subprocess.run(["taskkill", "/f", "/im", "msedge.exe"], capture_output=True)
                else:  # all browsers
                    subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], capture_output=True)
                    subprocess.run(["taskkill", "/f", "/im", "firefox.exe"], capture_output=True)
                    subprocess.run(["taskkill", "/f", "/im", "msedge.exe"], capture_output=True)
                
                self.tts.say(f"{browser.title()} browser closed.")
                return True
                
        except Exception as e:
            self.tts.say(f"Could not close {browser} tabs. Error: {e}")
            return False

    def close_specific_app(self, app_name):
        """Close a specific application"""
        try:
            app_names = {
                "mspaint": "Paint",
                "winword": "Microsoft Word",
                "excel": "Microsoft Excel", 
                "powerpnt": "Microsoft PowerPoint",
                "notepad": "Notepad"
            }
            
            display_name = app_names.get(app_name, app_name)
            self.tts.say(f"Closing {display_name}.")
            
            if os.name == "nt":  # Windows
                subprocess.run(["taskkill", "/f", "/im", f"{app_name}.exe"], capture_output=True)
            elif sys.platform == "darwin":  # macOS
                if app_name == "notepad":
                    subprocess.run(["pkill", "-f", "TextEdit"], capture_output=True)
                else:
                    subprocess.run(["pkill", "-f", app_name], capture_output=True)
            else:  # Linux
                subprocess.run(["pkill", "-f", app_name], capture_output=True)
            
            self.tts.say(f"{display_name} has been closed.")
            return True
            
        except Exception as e:
            self.tts.say(f"Could not close {app_name}. Error: {e}")
            return False

    def new_tab(self):
        """Open a new tab in the current browser"""
        try:
            import pyautogui
            
            self.tts.say("Opening a new tab.")
            
            # Use Ctrl+T to open new tab
            pyautogui.hotkey('ctrl', 't')
            return True
            
        except ImportError:
            self.tts.say("Could not open new tab. Please install pyautogui for this feature.")
            return False
        except Exception as e:
            self.tts.say(f"Could not open new tab. Error: {e}")
            return False

    def new_window(self):
        """Open a new window in the current application"""
        try:
            import pyautogui
            
            self.tts.say("Opening a new window.")
            
            # Use Ctrl+N to open new window
            pyautogui.hotkey('ctrl', 'n')
            return True
            
        except ImportError:
            self.tts.say("Could not open new window. Please install pyautogui for this feature.")
            return False
        except Exception as e:
            self.tts.say(f"Could not open new window. Error: {e}")
            return False

    def switch_to_app(self, app_name):
        """Switch to a specific application"""
        try:
            import pyautogui
            
            self.tts.say(f"Switching to {app_name}.")
            
            # Try to find the app window
            windows = pyautogui.getWindowsWithTitle(app_name)
            if windows:
                windows[0].activate()
                return True
            else:
                # Fallback: use Alt+Tab to cycle through windows
                pyautogui.hotkey('alt', 'tab')
                return True
                
        except ImportError:
            self.tts.say(f"Could not switch to {app_name}. Please install pyautogui for this feature.")
            return False
        except Exception as e:
            self.tts.say(f"Could not switch to {app_name}. Error: {e}")
            return False

    def close_all_tabs(self):
        """Close all browser tabs and windows (safely, preserving EchoOS)"""
        try:
            self.tts.say("I'll help you close browser tabs safely. Please switch to your browser window first.")
            
            # Use keyboard shortcuts to close tabs safely
            try:
                import pyautogui
                
                # Give user time to switch to browser
                time.sleep(2)
                
                # Close all tabs using Ctrl+W (close tab) repeatedly
                for i in range(10):  # Try up to 10 times
                    pyautogui.hotkey('ctrl', 'w')
                    time.sleep(0.2)
                
                # Alternative: Close all tabs at once with Ctrl+Shift+W (close all tabs)
                pyautogui.hotkey('ctrl', 'shift', 'w')
                
                self.tts.say("Browser tabs have been closed using keyboard shortcuts. EchoOS remains safe.")
                return True
                
            except ImportError:
                # Fallback: Use process killing but with warning
                self.tts.say("Using alternative method to close browser windows.")
                
                if os.name == "nt":  # Windows
                    subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], capture_output=True)
                    subprocess.run(["taskkill", "/f", "/im", "firefox.exe"], capture_output=True)
                    subprocess.run(["taskkill", "/f", "/im", "msedge.exe"], capture_output=True)
                elif sys.platform == "darwin":  # macOS
                    subprocess.run(["pkill", "-f", "Google Chrome"], capture_output=True)
                    subprocess.run(["pkill", "-f", "Firefox"], capture_output=True)
                else:  # Linux
                    subprocess.run(["pkill", "-f", "chrome"], capture_output=True)
                    subprocess.run(["pkill", "-f", "firefox"], capture_output=True)
                
                self.tts.say("Browser windows closed. EchoOS should remain active.")
                return True
                
        except Exception as e:
            self.tts.say(f"Could not close browser tabs. Error: {e}")
            return False
