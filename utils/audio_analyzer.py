import librosa
import numpy as np
from scipy.signal import find_peaks

def find_energy_peaks(video_path: str) -> list:
    try:
        # Load audio from video
        y, sr = librosa.load(video_path, sr=16000, mono=True)
        
        # Compute RMS energy per frame
        # In librosa 0.10+, rms is under feature
        rms = librosa.feature.rms(y=y, frame_length=2048, 
                                   hop_length=512)[0]
        
        # Find peaks (loud/energetic moments)
        peaks, _ = find_peaks(rms, 
                                  height=np.mean(rms) * 1.5,
                                  distance=sr//512 * 10)
        
        # Convert frame indices to timestamps
        times = librosa.frames_to_time(peaks, sr=sr, hop_length=512)
        return times.tolist()
    except Exception as e:
        print(f"Error in audio analysis: {e}")
        return []
