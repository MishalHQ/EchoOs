"""
Accessibility module for EchoOS
Provides features for differently-abled users including screen reading, navigation, and voice control
"""

import os
import sys
import time
import logging
import numpy as np
from typing import Optional, List, Dict, Any

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("PyAutoGUI not available - some accessibility features will be limited")

try:
    import cv2
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("OCR libraries not available - screen reading will be limited")

try:
    import pygetwindow as gw
    WINDOW_MANAGEMENT_AVAILABLE = True
except ImportError:
    WINDOW_MANAGEMENT_AVAILABLE = False
    print("Window management not available - some features will be limited")

class AccessibilityManager:
    """Manages accessibility features for differently-abled users"""
    
    def __init__(self, tts):
        self.tts = tts
        self.logger = logging.getLogger(__name__)
        self.current_focus = None
        self.navigation_mode = False
        self.high_contrast = False
        self.large_text = False
        self.voice_speed = 1.0
        
        # Screen reading settings
        self.screen_reading_enabled = True
        self.auto_read_changes = True
        
        # Navigation settings
        self.navigation_step = 10  # pixels
        self.click_delay = 0.5  # seconds
        
    def enable_navigation_mode(self):
        """Enable voice-controlled navigation mode"""
        self.navigation_mode = True
        self.tts.say("Navigation mode enabled. Use voice commands to navigate.")
        
    def disable_navigation_mode(self):
        """Disable navigation mode"""
        self.navigation_mode = False
        self.tts.say("Navigation mode disabled.")
        
    def read_screen(self, region=None):
        """Read text content from screen using OCR"""
        if not OCR_AVAILABLE:
            self.tts.say("Screen reading not available. Please install required libraries.")
            return False
            
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
                
            # Convert to OpenCV format
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Perform OCR
            text = pytesseract.image_to_string(img)
            
            if text.strip():
                self.tts.say(f"Screen content: {text[:200]}...")  # Limit to 200 chars
                return text
            else:
                self.tts.say("No readable text found on screen.")
                return ""
                
        except Exception as e:
            self.logger.error(f"Error reading screen: {e}")
            self.tts.say("Could not read screen content.")
            return False
            
    def describe_screen(self):
        """Describe the current screen layout and content"""
        try:
            # Get screen dimensions
            screen_width, screen_height = pyautogui.size()
            self.tts.say(f"Screen size is {screen_width} by {screen_height} pixels.")
            
            # Get active window info
            if WINDOW_MANAGEMENT_AVAILABLE:
                try:
                    active_window = gw.getActiveWindow()
                    if active_window:
                        self.tts.say(f"Active window: {active_window.title}")
                    else:
                        self.tts.say("No active window detected.")
                except:
                    self.tts.say("Could not detect active window.")
            
            # Read screen content
            self.read_screen()
            
        except Exception as e:
            self.logger.error(f"Error describing screen: {e}")
            self.tts.say("Could not describe screen.")
            
    def navigate(self, direction: str):
        """Navigate in the specified direction"""
        if not PYAUTOGUI_AVAILABLE:
            self.tts.say("Navigation not available. Please install PyAutoGUI.")
            return False
            
        try:
            current_x, current_y = pyautogui.position()
            
            if direction.lower() == "up":
                new_y = max(0, current_y - self.navigation_step)
                pyautogui.moveTo(current_x, new_y)
                self.tts.say(f"Moved up to position {current_x}, {new_y}")
                
            elif direction.lower() == "down":
                screen_height = pyautogui.size().height
                new_y = min(screen_height, current_y + self.navigation_step)
                pyautogui.moveTo(current_x, new_y)
                self.tts.say(f"Moved down to position {current_x}, {new_y}")
                
            elif direction.lower() == "left":
                new_x = max(0, current_x - self.navigation_step)
                pyautogui.moveTo(new_x, current_y)
                self.tts.say(f"Moved left to position {new_x}, {current_y}")
                
            elif direction.lower() == "right":
                screen_width = pyautogui.size().width
                new_x = min(screen_width, current_x + self.navigation_step)
                pyautogui.moveTo(new_x, current_y)
                self.tts.say(f"Moved right to position {new_x}, {current_y}")
                
            elif direction.lower() in ["next", "forward"]:
                pyautogui.press('tab')
                self.tts.say("Moved to next element")
                
            elif direction.lower() in ["previous", "back"]:
                pyautogui.hotkey('shift', 'tab')
                self.tts.say("Moved to previous element")
                
            else:
                self.tts.say(f"Unknown direction: {direction}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error navigating: {e}")
            self.tts.say("Navigation failed.")
            return False
            
    def click(self, button='left'):
        """Perform a mouse click"""
        if not PYAUTOGUI_AVAILABLE:
            self.tts.say("Clicking not available. Please install PyAutoGUI.")
            return False
            
        try:
            if button.lower() == 'left':
                pyautogui.click()
                self.tts.say("Left clicked")
            elif button.lower() == 'right':
                pyautogui.rightClick()
                self.tts.say("Right clicked")
            elif button.lower() == 'double':
                pyautogui.doubleClick()
                self.tts.say("Double clicked")
            else:
                self.tts.say(f"Unknown button: {button}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error clicking: {e}")
            self.tts.say("Click failed.")
            return False
            
    def scroll(self, direction: str, amount: int = 3):
        """Scroll in the specified direction"""
        if not PYAUTOGUI_AVAILABLE:
            self.tts.say("Scrolling not available. Please install PyAutoGUI.")
            return False
            
        try:
            if direction.lower() == "up":
                pyautogui.scroll(amount)
                self.tts.say(f"Scrolled up {amount} units")
            elif direction.lower() == "down":
                pyautogui.scroll(-amount)
                self.tts.say(f"Scrolled down {amount} units")
            else:
                self.tts.say(f"Unknown scroll direction: {direction}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error scrolling: {e}")
            self.tts.say("Scroll failed.")
            return False
            
    def zoom(self, direction: str):
        """Zoom in or out"""
        if not PYAUTOGUI_AVAILABLE:
            self.tts.say("Zooming not available. Please install PyAutoGUI.")
            return False
            
        try:
            if direction.lower() == "in":
                pyautogui.hotkey('ctrl', '+')
                self.tts.say("Zoomed in")
            elif direction.lower() == "out":
                pyautogui.hotkey('ctrl', '-')
                self.tts.say("Zoomed out")
            else:
                self.tts.say(f"Unknown zoom direction: {direction}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error zooming: {e}")
            self.tts.say("Zoom failed.")
            return False
            
    def toggle_high_contrast(self):
        """Toggle high contrast mode"""
        try:
            if os.name == "nt":  # Windows
                # Use Windows high contrast mode
                subprocess.run([
                    "powershell", "-c", 
                    "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SystemInformation]::HighContrast"
                ])
                self.tts.say("High contrast mode toggled")
            else:
                self.tts.say("High contrast mode not supported on this platform")
                
            self.high_contrast = not self.high_contrast
            return True
            
        except Exception as e:
            self.logger.error(f"Error toggling high contrast: {e}")
            self.tts.say("Could not toggle high contrast mode")
            return False
            
    def toggle_large_text(self):
        """Toggle large text mode"""
        try:
            if os.name == "nt":  # Windows
                # Use Windows display settings
                subprocess.run([
                    "powershell", "-c",
                    "Set-ItemProperty -Path 'HKCU:\\Control Panel\\Desktop\\WindowMetrics' -Name 'AppliedDPI' -Value 144"
                ])
                self.tts.say("Large text mode toggled")
            else:
                self.tts.say("Large text mode not supported on this platform")
                
            self.large_text = not self.large_text
            return True
            
        except Exception as e:
            self.logger.error(f"Error toggling large text: {e}")
            self.tts.say("Could not toggle large text mode")
            return False
            
    def set_voice_speed(self, speed: float):
        """Set the speed of text-to-speech"""
        if 0.5 <= speed <= 2.0:
            self.voice_speed = speed
            self.tts.say(f"Voice speed set to {speed}")
            return True
        else:
            self.tts.say("Voice speed must be between 0.5 and 2.0")
            return False
            
    def read_selected_text(self):
        """Read currently selected text"""
        try:
            # Copy selected text to clipboard
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)  # Wait for copy to complete
            
            # Get text from clipboard
            if sys.platform == "win32":
                import win32clipboard
                win32clipboard.OpenClipboard()
                text = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
            else:
                # For other platforms, use tkinter
                import tkinter as tk
                root = tk.Tk()
                root.withdraw()
                text = root.clipboard_get()
                root.destroy()
                
            if text.strip():
                self.tts.say(f"Selected text: {text}")
                return text
            else:
                self.tts.say("No text selected")
                return ""
                
        except Exception as e:
            self.logger.error(f"Error reading selected text: {e}")
            self.tts.say("Could not read selected text")
            return False
            
    def announce_focus_change(self):
        """Announce when focus changes to a new element"""
        try:
            # This would require integration with accessibility APIs
            # For now, we'll provide a basic implementation
            current_x, current_y = pyautogui.position()
            self.tts.say(f"Focus at position {current_x}, {current_y}")
            
        except Exception as e:
            self.logger.error(f"Error announcing focus change: {e}")
            
    def get_accessibility_status(self):
        """Get current accessibility settings status"""
        status = {
            "navigation_mode": self.navigation_mode,
            "screen_reading": self.screen_reading_enabled,
            "high_contrast": self.high_contrast,
            "large_text": self.large_text,
            "voice_speed": self.voice_speed,
            "auto_read_changes": self.auto_read_changes
        }
        
        status_text = f"Navigation mode: {'on' if self.navigation_mode else 'off'}, "
        status_text += f"Screen reading: {'on' if self.screen_reading_enabled else 'off'}, "
        status_text += f"High contrast: {'on' if self.high_contrast else 'off'}, "
        status_text += f"Large text: {'on' if self.large_text else 'off'}, "
        status_text += f"Voice speed: {self.voice_speed}"
        
        self.tts.say(status_text)
        return status
        
    def help_accessibility(self):
        """Provide help for accessibility features"""
        help_text = """
        Accessibility features available:
        - Say 'read screen' to read screen content
        - Say 'describe screen' for screen description
        - Say 'navigate up/down/left/right' to move cursor
        - Say 'click', 'double click', or 'right click' to click
        - Say 'scroll up/down' to scroll
        - Say 'zoom in/out' to zoom
        - Say 'high contrast' to toggle high contrast
        - Say 'large text' to toggle large text
        - Say 'navigation mode' to enable voice navigation
        - Say 'accessibility status' to check current settings
        """
        
        self.tts.say(help_text)
        return True
