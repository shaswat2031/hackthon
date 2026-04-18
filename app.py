import streamlit as st
import os
import shutil
import tempfile
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space
import time
from moviepy.editor import VideoFileClip

# Custom imports
import config
from utils.transcriber import transcribe_video
from utils.analyzer import find_viral_moments
from utils.audio_analyzer import find_energy_peaks
from utils.sentiment import get_sentiment
from utils.video_processor import cut_clip
from utils.crop_engine import smart_crop_to_vertical
from utils.caption_engine import add_dynamic_captions
from utils.uploader import upload_to_cloudinary

# Page configuration
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# Sidebar navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("AttentionX")
    
    selected = option_menu(
        menu_title=None,
        options=["Home", "Upload & Process", "Results"],
        icons=["house", "cloud-upload", "play-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#818cf8", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "rgba(255,255,255,0.1)",
            },
            "nav-link-selected": {"background-color": "#6366f1"},
        }
    )
    
    add_vertical_space(2)
    st.info("💡 AttentionX uses Groq (Llama 3) to find 'Golden Nuggets' in your long-form content.")
    
    if st.button("Clear Cache"):
        if os.path.exists(config.TEMP_DIR):
            shutil.rmtree(config.TEMP_DIR)
            os.makedirs(config.TEMP_DIR)
        st.rerun()

# --- PAGE 1: HOME ---
if selected == "Home":
    st.markdown('<h1 class="hero-text">Your Best Moments, Automatically Found</h1>', unsafe_allow_html=True)
    st.markdown("### Repurpose long-form videos into viral shorts in seconds. 100% Free.")
    
    add_vertical_space(2)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>500+</h3>
            <p>Clips Generated</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>1.2k+</h3>
            <p>Hours Saved</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>50+</h3>
            <p>Happy Creators</p>
        </div>
        """, unsafe_allow_html=True)
        
    add_vertical_space(3)
    
    st.markdown("## Features")
    fcol1, fcol2, fcol3 = st.columns(3)
    
    features = [
        {"icon": "🎙️", "title": "Local Transcription", "desc": "Uses Whisper Base to transcribe voice with zero API costs."},
        {"icon": "🎯", "title": "AI Viral Detection", "desc": "Groq Llama 3 identifies high-impact moments for maximum engagement."},
        {"icon": "📱", "title": "Smart Vertical Crop", "desc": "Face tracking with MediaPipe ensures the speaker is always centered."}
    ]
    
    for i, f in enumerate(features):
        with [fcol1, fcol2, fcol3][i]:
            st.markdown(f"""
            <div class="glass-card">
                <div class="feature-icon">{f['icon']}</div>
                <h3>{f['title']}</h3>
                <p>{f['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🛠️ Free Tech Stack")
    st.write("`Whisper LOCAL` • `Groq Llama 3 (Free Tier)` • `MoviePy` • `MediaPipe` • `Librosa`")
    st.success("✅ 100% Free — No Credit Card Required")

# --- PAGE 2: UPLOAD & PROCESS ---
elif selected == "Upload & Process":
    st.title("📥 Upload Long-Form Content")
    
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        video_path = os.path.join(config.TEMP_DIR, uploaded_file.name)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.video(video_path)
        
        # Determine actual video duration for safety
        try:
            with VideoFileClip(video_path) as temp_clip:
                video_duration = temp_clip.duration
            st.sidebar.success(f"Video Loaded: {video_duration:.2f} seconds")
        except Exception as e:
            st.error(f"Error reading video duration: {e}")
            video_duration = 0
        
        st.sidebar.markdown("---")
        st.sidebar.header("Settings")
        clip_duration = st.sidebar.slider("Max Clip Duration", 15, 90, 60)
        num_clips = st.sidebar.slider("Number of Clips", 1, 8, 3)
        whisper_model = st.sidebar.selectbox("Whisper Model", ["tiny", "base", "small"], index=1)
        
        gemini_key = st.sidebar.text_input("Groq API Key", value=config.GROQ_API_KEY, type="password")
        st.sidebar.info("Get a free key at [console.groq.com](https://console.groq.com/)")
        
        if st.button("🚀 Analyze & Generate Clips"):
            if not gemini_key:
                st.error("Please provide a Groq API Key to continue.")
            elif video_duration == 0:
                st.error("Could not determine video length. Check your file.")
            else:
                with st.status("Processing Video...", expanded=True) as status:
                    st.write("🎙️ Transcribing with Whisper (Local)...")
                    transcript_data = transcribe_video(video_path, whisper_model)
                    
                    st.write("📊 Analyzing audio energy...")
                    peaks = find_energy_peaks(video_path)
                    
                    st.write("🧠 Finding viral moments with Groq...")
                    moments = find_viral_moments(transcript_data['text'], transcript_data['segments'], num_clips, gemini_key)
                    
                    st.session_state['processed_clips'] = []
                    
                    for i, moment in enumerate(moments):
                        # SAFETY CHECK: Skip if AI suggested a time past video end
                        if moment['start_time'] >= video_duration:
                            st.write(f"⚠️ Skipping moment {i+1}: Start time past video end.")
                            continue
                            
                        # Adjust end time
                        moment['end_time'] = min(moment['end_time'], video_duration)
                        if (moment['end_time'] - moment['start_time']) < 5:
                            st.write(f"⚠️ Skipping moment {i+1}: Duration too short.")
                            continue

                        st.write(f"✂️ Cutting Clip {i+1}/{len(moments)}...")
                        output_name = f"clip_{i}_{uploaded_file.name}"
                        cut_path = os.path.join(config.TEMP_DIR, f"temp_{output_name}")
                        final_path = os.path.join(config.TEMP_DIR, output_name)

                        # 1. Cut
                        success_cut_path = cut_clip(video_path, float(moment['start_time']), float(moment['end_time']), cut_path)
                        
                        if success_cut_path and os.path.exists(cut_path):
                            # 2. Crop
                            st.write(f"📱 Attempting smart crop for Clip {i+1}...")
                            final_processed_path = smart_crop_to_vertical(cut_path, final_path)
                            
                            # FALLBACK: If specialized cropping failed to write a file, use the temp cut
                            if not os.path.exists(final_processed_path):
                                st.write(f"⚠️ Falling back to original ratio for Clip {i+1}")
                                final_processed_path = cut_path
                            
                            # 3. Upload to Cloudinary
                            st.write(f"☁️ Uploading Clip {i+1} to Cloudinary...")
                            cloudinary_url = upload_to_cloudinary(final_processed_path)
                            
                            # 4. Add to results
                            st.session_state['processed_clips'].append({
                                "path": final_processed_path,
                                "url": cloudinary_url,
                                "headline": moment.get('hook_headline', 'Viral Clip'),
                                "score": moment.get('emotion_score', 8),
                                "emotion": moment.get('emotion_type', 'Inspiring'),
                                "why": moment.get('why_viral', '')
                            })
                        else:
                            st.write(f"❌ Failed to process Clip {i+1}")
                    
                    status.update(label="✅ Processing Complete!", state="complete", expanded=False)
                
                st.balloons()
                st.success(f"Generated {len(st.session_state['processed_clips'])} clips!")
                time.sleep(1)
                st.rerun()

# --- PAGE 3: RESULTS ---
elif selected == "Results":
    st.title("🎬 Generated Clips")
    
    if 'processed_clips' not in st.session_state or not st.session_state['processed_clips']:
        st.warning("No clips generated yet. Please go to 'Upload & Process' first.")
    else:
        for i, clip in enumerate(st.session_state['processed_clips']):
            with st.container():
                st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
                col_v, col_t = st.columns([1, 1.5])
                
                with col_v:
                    if clip.get('url'):
                        st.video(clip['url'])
                        st.caption("🌐 Cloudinary URL: " + clip['url'])
                    elif os.path.exists(clip['path']):
                        st.video(clip['path'])
                    else:
                        st.error("Video file not found.")
                
                with col_t:
                    st.subheader(clip['headline'])
                    st.markdown(f"**Virality Score:** {clip['score']}/10")
                    st.markdown(f"**Emotion:** {clip['emotion']}")
                    st.info(clip['why'])
                    
                    if os.path.exists(clip['path']):
                        with open(clip['path'], "rb") as f:
                            st.download_button(
                                label=f"Download Clip {i+1}",
                                data=f,
                                file_name=os.path.basename(clip['path']),
                                mime="video/mp4",
                                key=f"dl_{i}"
                            )
                st.markdown('</div>', unsafe_allow_html=True)
                add_vertical_space(1)
        
        st.markdown("---")
        if st.button("Start New Project"):
            st.session_state['processed_clips'] = []
            st.rerun()
