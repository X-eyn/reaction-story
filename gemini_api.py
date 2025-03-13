import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

# Configure the Gemini API
genai.configure(api_key=API_KEY)

async def generate_text(prompt, max_tokens=2000):
    """
    Generate text using Google's Gemini 2.0 Flash API
    
    Args:
        prompt (str): The prompt to send to the API
        max_tokens (int): Maximum number of tokens to generate
        
    Returns:
        str: The generated text response
    """
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    try:
        # Set up the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Run the API call in a thread pool to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: model.generate_content(prompt)
        )
        
        # Extract the text from the response
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Failed to generate text: {str(e)}")
