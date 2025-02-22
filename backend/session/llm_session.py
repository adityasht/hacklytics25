# session/llm_session.py
from typing import List, Dict, Optional
from api.vision_api import vision_api_call
from api.text_api import text_api_call

class LLMSession:
    """Base class for managing LLM interactions with conversation history."""
    
    def __init__(self):
        self.vision_history: List[Dict] = []
        self.text_history: List[Dict] = []
        self.current_image: Optional[str] = None

    async def ask_vision(self, prompt: str, image_input: Optional[str] = None) -> dict:
        """Make a vision API call while maintaining conversation history."""
        if image_input:
            self.current_image = image_input
        
        if not self.current_image:
            raise ValueError("No image provided and no previous image available")
        
        try:
            response = await vision_api_call(prompt, self.current_image)
            
            if "choices" in response and response["choices"]:
                self._update_vision_history(prompt, response, image_input)
            
            return response
            
        except Exception as e:
            raise Exception(f"Vision API call failed: {str(e)}")

    async def ask_text(self, prompt: str) -> dict:
        """Make a text API call while maintaining conversation history."""
        try:
            response = await text_api_call(prompt)
            
            if "choices" in response and response["choices"]:
                self._update_text_history(prompt, response)
            
            return response
            
        except Exception as e:
            raise Exception(f"Text API call failed: {str(e)}")

    def _update_vision_history(self, prompt: str, response: dict, image_input: Optional[str] = None):
        """Update vision conversation history."""
        user_message = {
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        }
        
        if image_input:
            user_message["content"].append({
                "type": "image_url",
                "image_url": {"url": self.current_image}
            })
        
        self.vision_history.append(user_message)
        self.vision_history.append(response["choices"][0]["message"])

    def _update_text_history(self, prompt: str, response: dict):
        """Update text conversation history."""
        self.text_history.append({
            "role": "user",
            "content": prompt
        })
        self.text_history.append(response["choices"][0]["message"])

    def get_vision_history(self) -> List[Dict]:
        """Get the current vision conversation history."""
        return self.vision_history

    def get_text_history(self) -> List[Dict]:
        """Get the current text conversation history."""
        return self.text_history

    def clear_vision_history(self):
        """Clear vision conversation history and current image."""
        self.vision_history = []
        self.current_image = None

    def clear_text_history(self):
        """Clear text conversation history."""
        self.text_history = []

    def clear_all_history(self):
        """Clear all conversation histories and current image."""
        self.clear_vision_history()
        self.clear_text_history()