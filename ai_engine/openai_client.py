"""OpenAI Integration Client"""
import logging
import openai
from config import Config

logger = logging.getLogger(__name__)


class OpenAIClient:
    """OpenAI API client for processing conversations"""
    
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.conversation_history = []
    
    def get_response(self, user_input):
        """Get response from OpenAI"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Get response from OpenAI
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=150,
                temperature=0.7
            )
            
            # Extract response
            bot_message = response.choices[0].message.content
            
            # Add bot response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": bot_message
            })
            
            logger.info(f"OpenAI Response: {bot_message}")
            return bot_message
        except Exception as e:
            logger.error(f"Error getting response from OpenAI: {str(e)}")
            return "Sorry, I couldn't process that. Please try again."
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        logger.info("Conversation history reset")
    
    def set_system_prompt(self, prompt):
        """Set system prompt for conversation"""
        self.conversation_history = [{
            "role": "system",
            "content": prompt
        }]
        logger.info(f"System prompt set: {prompt}")
