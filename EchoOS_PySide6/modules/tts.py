import threading
import queue
import time
import logging

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    print("pyttsx3 not available - TTS will be text-only")

class TTS:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        if PYTTSX3_AVAILABLE:
            self.logger.info("TTS system initialized (using separate engines approach)")
        else:
            self.logger.warning("pyttsx3 not available - TTS disabled")
    
    # Threading methods removed - using separate engines approach instead
    
    def say(self, text, async_mode=True):
        """Speak text - can be synchronous or asynchronous"""
        if not text:
            self.logger.warning("Empty text provided to TTS")
            return
            
        print(f"[TTS] {text}")
        
        if async_mode:
            # Use separate engine approach for reliability
            self._speak_with_separate_engine(text)
        else:
            # Synchronous mode (blocking) - also use separate engine
            self._speak_with_separate_engine(text)
    
    def _speak_with_separate_engine(self, text):
        """Speak using a separate engine instance for reliability"""
        try:
            import pyttsx3
            
            # Create fresh engine instance
            engine = pyttsx3.init()
            
            # Configure engine
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 0.9)
            
            # Try to use a female voice if available
            voices = engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            # Speak the text
            engine.say(text)
            engine.runAndWait()
            
            # Clean up
            del engine
            
            self.logger.info(f"TTS completed: {text[:30]}...")
            
        except Exception as e:
            self.logger.error(f"TTS separate engine error: {e}")
            print(f"[TTS Error] {e}")
    
    def say_sync(self, text):
        """Synchronous TTS (blocking)"""
        self.say(text, async_mode=False)
    
    def say_async(self, text):
        """Asynchronous TTS (non-blocking)"""
        self.say(text, async_mode=True)
    
    def is_busy(self):
        """Check if TTS is currently speaking"""
        if self.engine:
            try:
                return self.engine._inLoop
            except:
                return False
        return False
    
    def stop_speaking(self):
        """Stop current speech"""
        if self.engine:
            try:
                self.engine.stop()
            except Exception as e:
                self.logger.error(f"Error stopping TTS: {e}")
    
    def set_rate(self, rate):
        """Set speech rate (words per minute)"""
        if self.engine:
            try:
                self.engine.setProperty('rate', rate)
            except Exception as e:
                self.logger.error(f"Error setting TTS rate: {e}")
    
    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        if self.engine:
            try:
                self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
            except Exception as e:
                self.logger.error(f"Error setting TTS volume: {e}")
    
    def get_voices(self):
        """Get available voices"""
        if self.engine:
            try:
                return self.engine.getProperty('voices')
            except:
                return []
        return []
    
    def set_voice(self, voice_id):
        """Set specific voice by ID"""
        if self.engine:
            try:
                self.engine.setProperty('voice', voice_id)
            except Exception as e:
                self.logger.error(f"Error setting TTS voice: {e}")
    
    def __del__(self):
        """Cleanup when TTS object is destroyed"""
        # No cleanup needed for separate engines approach
        pass
