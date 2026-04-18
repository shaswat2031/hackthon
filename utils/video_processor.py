from moviepy.editor import VideoFileClip
import os

def cut_clip(video_path: str, start_time: float, end_time: float, output_path: str):
    """
    Cuts a clip from the video using MoviePy.
    """
    try:
        with VideoFileClip(video_path) as video:
            clip = video.subclip(start_time, end_time)
            clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        return output_path
    except Exception as e:
        print(f"Error cutting clip: {e}")
        return None
