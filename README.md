# 🚀 AttentionX: Automated Video Repurposing Engine

**AttentionX** is a state-of-the-art AI platform that transforms long-form video content into viral, snackable clips for TikTok, Reels, and YouTube Shorts. 

Built for the **AI Hackathon**, it uses a "Hybrid Free Stack"—combining heavyweight local models with ultra-fast cloud inference to provide a 100% free solution for creators.

## ✨ Key Features
- **🎙️ Local Transcription**: Zero-cost speech-to-text using OpenAI Whisper.
- **🧠 Viral Intelligence**: Uses **Groq Llama 3.3 (70B)** to identify "Golden Nuggets" with high emotional impact.
- **📱 Smart Vertical Cropping**: Dynamic face-tracking via **MediaPipe** ensures the speaker is always centered in 9:16.
- **📊 Audio Energy Analysis**: Uses **Librosa** to detect high-energy peaks for perfect clip timing.
- **☁️ Cloud Publishing**: Automatic result hosting on **Cloudinary** for easy sharing.

## 🛠️ Tech Stack
- **Dashboard**: Streamlit (Premium Glassmorphic UI)
- **AI/ML**: Groq, OpenAI Whisper, MediaPipe
- **Video Logic**: MoviePy, OpenCV
- **Storage**: Cloudinary

## ⚙️ Installation & Setup

1. **Clone & Install Dependencies**
```bash
# Clone the repository
git clone <your-repo-link>
cd attentionx

# Install requirements
pip install -r requirements.txt
```

2. **Configure Environment Variables**
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_key_here
CLOUDINARY_CLOUD_NAME=your_name
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret
```

3. **Run Locally**
```bash
streamlit run app.py
```

## 🌐 Deployment (Streamlit Community Cloud)
1. Push your code to a GitHub repository.
2. Connect the repo to Streamlit Cloud.
3. Add your environment variables to **Advanced Settings > Secrets** in TOML format:
   ```toml
   GROQ_API_KEY = "..."
   CLOUDINARY_CLOUD_NAME = "..."
   CLOUDINARY_API_KEY = "..."
   CLOUDINARY_API_SECRET = "..."
   ```

## 🏆 Hackathon Notes
- **Zero Cost**: Our architecture ensures creators never pay for expensive APIs.
- **Privacy First**: Heavy transcription logic runs locally on the user's hardware.
- **Speed**: Optimized processing pipeline turns a 1-hour job into minutes.

---
*Built with ❤️ for the AI Hackathon 2026. Powered by Groq & Streamlit.*
