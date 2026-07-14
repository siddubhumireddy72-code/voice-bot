"""Speech-to-Text Processing"""
import logging
import openai
from config import Config

logger = logging.getLogger(__name__)


class SpeechToText:
    """Convert speech to text using OpenAI Whisper API"""
    
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.language = Config.SPEECH_LANGUAGE
    
    def transcribe(self, audio_file):
        """Transcribe audio file to text"""
        try:
            logger.info(f"Transcribing audio file: {audio_file}")
            
            with open(audio_file, 'rb') as f:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=f,
                    language=self.language
                )
            
            text = transcript.get('text')
            logger.info(f"Transcription complete: {text}")
            return text
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            return None
    
    def transcribe_from_url(self, audio_url):
        """Transcribe audio from URL"""
        try:
            logger.info(f"Transcribing audio from URL: {audio_url}")
            # Implementation for URL-based transcription
            return None
        except Exception as e:
            logger.error(f"Error transcribing from URL: {str(e)}")
            return None
