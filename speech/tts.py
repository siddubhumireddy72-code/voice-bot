"""Text-to-Speech Processing"""
import logging
from gtts import gTTS
from config import Config

logger = logging.getLogger(__name__)


class TextToSpeech:
    """Convert text to speech using gTTS"""
    
    def __init__(self):
        self.language = Config.SPEECH_LANGUAGE.split('-')[0]  # Extract language code
    
    def synthesize(self, text, output_file):
        """Synthesize text to speech and save to file"""
        try:
            logger.info(f"Synthesizing text to speech: {text}")
            
            tts = gTTS(text=text, lang=self.language, slow=False)
            tts.save(output_file)
            
            logger.info(f"Speech saved to: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"Error synthesizing speech: {str(e)}")
            return None
    
    def synthesize_and_play(self, text):
        """Synthesize and play text"""
        try:
            logger.info(f"Synthesizing and playing: {text}")
            tts = gTTS(text=text, lang=self.language, slow=False)
            # Play audio logic
            return True
        except Exception as e:
            logger.error(f"Error synthesizing and playing: {str(e)}")
            return False
