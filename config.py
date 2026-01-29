"""
Environment configuration file
Store API keys and sensitive data here (add to .gitignore)
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.getenv('OPENROUTER_MODEL', 'meta-llama/llama-2-7b-chat')

# Chatbot Configuration
MAX_TOKENS = 1000
TEMPERATURE = 0.7
TOP_P = 0.9

# Validation
if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found in environment variables. "
        "Please set it in your .env file or system environment."
    )
