from groq import Groq
import json
import os

def find_viral_moments(transcript: str, segments: list, 
                       num_clips: int = 5, api_key: str = ""):
    """
    Uses Groq (Llama 3) to find viral moments.
    """
    if not api_key:
        # Fallback to env if not provided via UI
        api_key = os.getenv("GROQ_API_KEY", "")
        
    if not api_key:
        raise ValueError("Groq API Key is required.")
        
    client = Groq(api_key=api_key)
    
    prompt = f"""
    Analyze this video transcript and find the TOP {num_clips} 
    most viral-worthy moments for TikTok/Reels (30-90 seconds).
    
    CRITERIA:
    - Emotional peaks (passion, surprise, inspiration)
    - Standalone golden nuggets (make sense without context)
    - Strong hook potential (bold claim or question opening)
    - Complete thought within 30-90 seconds
    
    Transcript with timestamps:
    {transcript}
    
    IMPORTANT: Return ONLY a valid JSON array, no markdown intro, no backticks.
    Expected Format:
    [
      {{
        "start_time": 45.2,
        "end_time": 98.7,
        "hook_headline": "Why 90% of creators fail at this",
        "why_viral": "One sentence explanation",
        "emotion_score": 8,
        "emotion_type": "Inspiring",
        "caption_style": "bold_white"
      }}
    ]
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a viral content expert. Respond ONLY with raw JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=2048,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"}
        )
        
        content = completion.choices[0].message.content
        # Groq usually returns clean JSON with response_format, but we'll be safe
        data = json.loads(content)
        
        # If the model wraps it in a key (like "moments"), extract it
        if isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list):
                    return data[key]
            return [data] # if single object
            
        return data
        
    except Exception as e:
        print(f"Groq Analysis Error: {e}")
        return []
