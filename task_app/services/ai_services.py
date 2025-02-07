import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv('AI_API_KEY')
        if not self.api_key:
            raise ValueError("AI_API_KEY is not set in the .env file")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_response(self, prompt):
        """Generate a response from the AI model."""
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_response_with_personality(self, personality, prompt):
        """Generate a response from the AI model with a personality."""
        persona_prompt = f"You are {personality}. {prompt}"
        response = self.model.generate_content(persona_prompt)
        return response.text
