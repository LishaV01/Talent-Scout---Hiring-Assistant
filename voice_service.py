import pyttsx3
import speech_recognition as sr
import threading
import queue
import time
import re
from typing import Optional, Callable

class VoiceService:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Configure voice properties
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to use a different voice if available
            self.engine.setProperty('voice', voices[0].id)
            print(f"Using voice: {voices[0].name}")
        
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Maximum volume
        
        # Test the engine silently
        self._test_engine()
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Minimum audio energy to consider for recording
        self.recognizer.dynamic_energy_threshold = True
        
        # Message queue for text-to-speech
        self.tts_queue = queue.Queue()
        self.is_speaking = False
        self.stop_speaking_flag = False
        
        # Start the TTS thread
        self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.tts_thread.start()

    def _test_engine(self):
        """Test if the TTS engine is working (silently)"""
        try:
            print("Testing TTS engine...")
            # Just test the engine properties without speaking
            voices = self.engine.getProperty('voices')
            rate = self.engine.getProperty('rate')
            volume = self.engine.getProperty('volume')
            print(f"TTS engine test successful - {len(voices) if voices else 0} voices available")
            print(f"Current settings - Rate: {rate}, Volume: {volume}")
        except Exception as e:
            print(f"TTS engine test failed: {e}")
            import traceback
            traceback.print_exc()

    def speak(self, text: str):
        """Add text to the speech queue"""
        print(f"Adding to queue: {text[:50]}...")
        self.tts_queue.put(text)

    def speak_direct(self, text: str):
        """Directly speak text without using the queue (for testing)"""
        try:
            print(f"Direct speaking: {text[:50]}...")
            cleaned_text = self._clean_text_for_speech(text)
            self.engine.say(cleaned_text)
            self.engine.runAndWait()
            print("Direct speak completed")
        except Exception as e:
            print(f"Direct speak error: {e}")
            import traceback
            traceback.print_exc()

    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text by removing markdown and special formatting"""
        # Remove markdown bold markers
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        # Remove markdown italic markers
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        # Remove markdown headers
        text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
        # Remove markdown code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Remove inline code
        text = re.sub(r'`(.*?)`', r'\1', text)
        # Remove horizontal rules
        text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
        # Replace multiple newlines with single space
        text = re.sub(r'\n+', ' ', text)
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _split_into_chunks(self, text: str) -> list:
        """Split text into speakable chunks"""
        # Clean the text first
        text = self._clean_text_for_speech(text)
        
        # Split by various punctuation marks and newlines
        # This regex splits on periods, exclamation marks, question marks, colons, semicolons
        # But keeps the punctuation with the sentence
        sentences = re.split(r'(?<=[.!?:;])\s+', text)
        
        # Further split very long sentences at commas if needed
        chunks = []
        for sentence in sentences:
            if len(sentence) > 200:  # If sentence is too long
                # Split at commas but keep reasonable chunks
                parts = sentence.split(',')
                current_chunk = ""
                for part in parts:
                    if len(current_chunk) + len(part) < 200:
                        current_chunk += part + ","
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.rstrip(','))
                        current_chunk = part + ","
                if current_chunk:
                    chunks.append(current_chunk.rstrip(','))
            else:
                chunks.append(sentence)
        
        # Filter out empty chunks
        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def _tts_worker(self):
        """Background worker for text-to-speech"""
        while True:
            try:
                text = self.tts_queue.get()
                if text is None:
                    break
                
                self.is_speaking = True
                self.stop_speaking_flag = False
                
                # Clean the text
                cleaned_text = self._clean_text_for_speech(text)
                
                # Debug: print the full text to be spoken
                print(f"Full text to speak: {cleaned_text[:100]}...")
                
                # Make sure we have text to speak
                if not cleaned_text:
                    print("Warning: No text to speak after cleaning")
                    self.is_speaking = False
                    self.tts_queue.task_done()
                    continue
                
                # Try speaking the entire text at once
                try:
                    self.engine.say(cleaned_text)
                    self.engine.runAndWait()
                    print("Successfully spoke entire text")
                except Exception as e:
                    print(f"Error speaking full text, will try chunks: {e}")
                    
                    # If that fails, fall back to chunks
                    chunks = self._split_into_chunks(text)
                    
                    # If no chunks were created, use the original text
                    if not chunks:
                        chunks = [cleaned_text]
                    
                    print(f"Speaking in {len(chunks)} chunks")
                    
                    # Speak each chunk
                    for i, chunk in enumerate(chunks):
                        if self.stop_speaking_flag:
                            break
                        
                        # Debug print to see what's being spoken
                        print(f"Speaking chunk {i+1}/{len(chunks)}: {chunk[:50]}...")
                        
                        try:
                            self.engine.say(chunk)
                            self.engine.runAndWait()
                            time.sleep(0.2)  # Slightly longer pause between chunks
                        except Exception as chunk_error:
                            print(f"Error speaking chunk {i+1}: {chunk_error}")
                            continue
                
                self.is_speaking = False
                self.tts_queue.task_done()
                
            except Exception as e:
                print(f"Error in TTS worker: {str(e)}")
                import traceback
                traceback.print_exc()
                self.is_speaking = False
                if hasattr(self.tts_queue, 'task_done'):
                    self.tts_queue.task_done()

    def stop_speaking(self):
        """Stop the current speech"""
        self.stop_speaking_flag = True
        self.engine.stop()

    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen for speech and convert to text"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout)
                print("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                return text.lower()
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {str(e)}")
            return None
        except Exception as e:
            print(f"Error in speech recognition: {str(e)}")
            return None

    def cleanup(self):
        """Clean up resources"""
        self.stop_speaking()
        self.tts_queue.put(None)  # Signal the worker thread to stop
        self.tts_thread.join()