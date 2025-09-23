import os
import pickle
import random
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import logging
from datetime import datetime, timedelta
import threading
import time

try:
    from resemblyzer import VoiceEncoder, preprocess_wav
    from pathlib import Path
    RESEMBLYZER_AVAILABLE = True
except ImportError:
    RESEMBLYZER_AVAILABLE = False
    print("Resemblyzer not available, falling back to MFCC authentication")

try:
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Scikit-learn not available, using numpy for similarity calculation")

class Authenticator:
    def __init__(self, tts, user_file="config/users.pkl", session_file="config/sessions.pkl"):
        self.tts = tts
        self.user_file = user_file
        self.session_file = session_file
        self.users = self.load_users()
        self.sessions = self.load_sessions()
        self.current_user = None
        self.session_timeout = 30 * 60  # 30 minutes
        self.failed_attempts = {}
        self.max_failed_attempts = 3
        self.lockout_duration = 5 * 60  # 5 minutes
        
        # Initialize Resemblyzer if available
        if RESEMBLYZER_AVAILABLE:
            self.encoder = VoiceEncoder()
            self.sample_rate = 16000
        else:
            self.encoder = None
            self.sample_rate = 16000
            
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def load_users(self):
        """Load user profiles from file"""
        if os.path.exists(self.user_file):
            try:
                with open(self.user_file, "rb") as f:
                    return pickle.load(f)
            except Exception as e:
                self.logger.error(f"Error loading users: {e}")
                return {}
        return {}

    def save_users(self):
        """Save user profiles to file"""
        try:
            with open(self.user_file, "wb") as f:
                pickle.dump(self.users, f)
        except Exception as e:
            self.logger.error(f"Error saving users: {e}")

    def load_sessions(self):
        """Load active sessions from file"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, "rb") as f:
                    return pickle.load(f)
            except Exception as e:
                self.logger.error(f"Error loading sessions: {e}")
                return {}
        return {}

    def save_sessions(self):
        """Save active sessions to file"""
        try:
            with open(self.session_file, "wb") as f:
                pickle.dump(self.sessions, f)
        except Exception as e:
            self.logger.error(f"Error saving sessions: {e}")

    def record_sample(self, seconds=5):
        """Record audio sample for authentication"""
        fs = self.sample_rate
        self.tts.say(f"Recording for {seconds} seconds. Please speak clearly.")
        audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()
        return fs, audio

    def extract_features(self, fs, audio):
        """Extract voice features using Resemblyzer or fallback to MFCC"""
        audio = np.squeeze(audio)
        
        if RESEMBLYZER_AVAILABLE and self.encoder:
            try:
                # Preprocess audio for Resemblyzer
                wav = preprocess_wav(audio, fs)
                # Extract speaker embedding
                embedding = self.encoder.embed_utterance(wav)
                return embedding
            except Exception as e:
                self.logger.warning(f"Resemblyzer failed, falling back to MFCC: {e}")
                return self._extract_mfcc_features(fs, audio)
        else:
            return self._extract_mfcc_features(fs, audio)

    def _extract_mfcc_features(self, fs, audio):
        """Fallback MFCC feature extraction"""
        try:
            from python_speech_features import mfcc
            features = mfcc(audio, samplerate=fs, numcep=13)
            return np.mean(features, axis=0)
        except ImportError:
            # Basic feature extraction if python_speech_features is not available
            return np.mean(audio.reshape(-1, 1), axis=0)

    def calculate_similarity(self, features1, features2):
        """Calculate similarity between two feature vectors"""
        if SKLEARN_AVAILABLE:
            return cosine_similarity([features1], [features2])[0][0]
        else:
            # Fallback to numpy cosine similarity
            dot_product = np.dot(features1, features2)
            norm1 = np.linalg.norm(features1)
            norm2 = np.linalg.norm(features2)
            if norm1 == 0 or norm2 == 0:
                return 0
            return dot_product / (norm1 * norm2)

    def register_user(self, username):
        """Register a new user with voice authentication"""
        if username in self.users:
            self.tts.say(f"User {username} already exists.")
            return False
            
        self.tts.say(f"Registering new user {username}. Please provide three voice samples.")
        samples = []
        
        for i in range(3):
            self.tts.say(f"Sample {i+1} of 3. Please speak clearly.")
            fs, audio = self.record_sample(5)
            features = self.extract_features(fs, audio)
            if features is not None:
                samples.append(features)
            else:
                self.tts.say("Sample failed. Please try again.")
                return False
        
        if len(samples) >= 2:
            # Store multiple samples for better accuracy
            self.users[username] = {
                'embeddings': samples,
                'created_at': datetime.now(),
                'last_used': datetime.now()
            }
            self.save_users()
            self.tts.say(f"Registration complete. Welcome, {username}.")
            self.logger.info(f"User {username} registered successfully")
            return True
        else:
            self.tts.say("Registration failed. Not enough valid samples.")
            return False

    def authenticate_interactive(self):
        """Authenticate user through voice recognition"""
        if not self.users:
            self.tts.say("No registered users found. Please register first.")
            return None
            
        # Check for lockout
        client_ip = "local"  # In a real implementation, you'd get the actual IP
        if self._is_locked_out(client_ip):
            self.tts.say("Account temporarily locked due to multiple failed attempts.")
            return None
            
        self.tts.say("Please speak for authentication.")
        fs, audio = self.record_sample(5)
        features = self.extract_features(fs, audio)
        
        if features is None:
            self.tts.say("Authentication failed. Could not process audio.")
            return None

        best_match = None
        best_score = 0.0
        threshold = 0.7 if RESEMBLYZER_AVAILABLE else 0.8  # Lower threshold for Resemblyzer

        for username, user_data in self.users.items():
            if isinstance(user_data, dict) and 'embeddings' in user_data:
                # New format with multiple embeddings
                embeddings = user_data['embeddings']
                max_similarity = 0
                for embedding in embeddings:
                    similarity = self.calculate_similarity(features, embedding)
                    max_similarity = max(max_similarity, similarity)
                score = max_similarity
            else:
                # Legacy format with single embedding
                score = self.calculate_similarity(features, user_data)

            if score > best_score:
                best_score = score
                best_match = username

        if best_score > threshold:
            self.current_user = best_match
            self._create_session(best_match)
            self._update_user_last_used(best_match)
            self._reset_failed_attempts(client_ip)
            self.tts.say(f"Access granted. Welcome back, {best_match}.")
            self.logger.info(f"User {best_match} authenticated successfully")
            return best_match
        else:
            self._record_failed_attempt(client_ip)
            responses = [
                "Voice authentication failed. Please try again.",
                "I am sorry, your voice does not match any registered user.",
                "Access denied. Identity could not be verified."
            ]
            self.tts.say(random.choice(responses))
            self.logger.warning(f"Authentication failed for IP {client_ip}")
            return None

    def _is_locked_out(self, client_ip):
        """Check if client is locked out due to failed attempts"""
        if client_ip not in self.failed_attempts:
            return False
        
        attempts, last_attempt = self.failed_attempts[client_ip]
        if attempts >= self.max_failed_attempts:
            if datetime.now() - last_attempt < timedelta(seconds=self.lockout_duration):
                return True
            else:
                # Reset after lockout period
                del self.failed_attempts[client_ip]
        return False

    def _record_failed_attempt(self, client_ip):
        """Record a failed authentication attempt"""
        now = datetime.now()
        if client_ip in self.failed_attempts:
            attempts, last_attempt = self.failed_attempts[client_ip]
            if now - last_attempt < timedelta(minutes=10):  # Reset after 10 minutes
                self.failed_attempts[client_ip] = (attempts + 1, now)
            else:
                self.failed_attempts[client_ip] = (1, now)
        else:
            self.failed_attempts[client_ip] = (1, now)

    def _reset_failed_attempts(self, client_ip):
        """Reset failed attempts for successful authentication"""
        if client_ip in self.failed_attempts:
            del self.failed_attempts[client_ip]

    def _create_session(self, username):
        """Create a new session for authenticated user"""
        session_id = f"{username}_{int(time.time())}"
        self.sessions[session_id] = {
            'username': username,
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=self.session_timeout)
        }
        self.save_sessions()

    def _update_user_last_used(self, username):
        """Update last used timestamp for user"""
        if username in self.users and isinstance(self.users[username], dict):
            self.users[username]['last_used'] = datetime.now()
            self.save_users()

    def is_session_valid(self, session_id=None):
        """Check if current session is valid"""
        if not self.current_user:
            return False
            
        if session_id:
            if session_id in self.sessions:
                session = self.sessions[session_id]
                if datetime.now() < session['expires_at']:
                    session['last_activity'] = datetime.now()
                    return True
                else:
                    del self.sessions[session_id]
                    self.save_sessions()
            return False
        else:
            # Check if any session for current user is valid
            for session_id, session in self.sessions.items():
                if (session['username'] == self.current_user and 
                    datetime.now() < session['expires_at']):
                    session['last_activity'] = datetime.now()
                    return True
            return False

    def logout(self):
        """Logout current user and clear session"""
        if self.current_user:
            # Remove all sessions for current user
            sessions_to_remove = [sid for sid, session in self.sessions.items() 
                                if session['username'] == self.current_user]
            for sid in sessions_to_remove:
                del self.sessions[sid]
            self.save_sessions()
            self.tts.say(f"Goodbye, {self.current_user}.")
            self.current_user = None
            self.logger.info(f"User {self.current_user} logged out")

    def remove_user(self, name):
        """Remove a user from the system"""
        if name in self.users:
            del self.users[name]
            # Remove all sessions for this user
            sessions_to_remove = [sid for sid, session in self.sessions.items() 
                                if session['username'] == name]
            for sid in sessions_to_remove:
                del self.sessions[sid]
            self.save_users()
            self.save_sessions()
            self.tts.say(f"User {name} has been removed.")
            self.logger.info(f"User {name} removed from system")
            return True
        return False

    def get_user_info(self, username=None):
        """Get information about a user"""
        if username is None:
            username = self.current_user
        if username and username in self.users:
            return self.users[username]
        return None

    def list_users(self):
        """List all registered users"""
        return list(self.users.keys())

    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        now = datetime.now()
        expired_sessions = [sid for sid, session in self.sessions.items() 
                           if now > session['expires_at']]
        for sid in expired_sessions:
            del self.sessions[sid]
        if expired_sessions:
            self.save_sessions()
            self.logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")