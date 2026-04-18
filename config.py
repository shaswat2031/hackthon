import os
from dotenv import load_dotenv

load_dotenv()

# App Configuration
APP_NAME = "AttentionX"
ASSETS_DIR = "assets"
UTILS_DIR = "utils"
TEMP_DIR = "temp_data"

# Model Configuration
WHISPER_MODEL_SIZE = "base"  # options: tiny, base, small, medium, large
GEMINI_MODEL_NAME = "gemini-1.5-flash"
SENTIMENT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment"

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Groq Model
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"

# Cloudinary Config
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

# UI Configuration
PAGE_TITLE = "AttentionX - Automated Content Repurposing"
PAGE_ICON = "🚀"

# Create temp dir if it doesn't exist
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
