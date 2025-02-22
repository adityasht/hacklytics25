# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPEN-ROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("API key not found in environment variables")

# API URLs and Headers
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://localhost:3000",
    "X-Title": "LocalDevelopment",
}

# Model Configuration
VISION_MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"
TEXT_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'