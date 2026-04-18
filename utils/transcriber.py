import whisper
import os

def transcribe_video(video_path: str, model_size: str = "base"):
    # Load Whisper model locally (no API key needed)
    print(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)
    
    # Transcribe with word-level timestamps
    print(f"Transcribing {video_path}...")
    result = model.transcribe(
        video_path,
        word_timestamps=True,
        verbose=False
    )
    
    return {
        "text": result["text"],
        "segments": result["segments"],  # has start/end times
        "words": [
            word 
            for seg in result["segments"] 
            for word in seg.get("words", [])
        ]
    }
