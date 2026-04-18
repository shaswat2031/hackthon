import cv2
from moviepy.editor import VideoFileClip, vfx
from .face_tracker import get_face_center

def smart_crop_to_vertical(video_path: str, output_path: str):
    """
    Crops video to 9:16 vertical ratio.
    If a face is detected in the first frame, it centers around the face.
    Otherwise, it centers the crop.
    """
    try:
        with VideoFileClip(video_path) as clip:
            w, h = clip.size
            target_w = int(h * 9 / 16)
            
            if target_w > w:
                # Video is already too vertical or small, just scale or keep as is
                target_w = w
            
            # Get face center from middle frame for better context
            middle_frame = clip.get_frame(clip.duration / 2)
            face_x = get_face_center(middle_frame)
            
            if face_x is None:
                face_x = w / 2
            
            # Calculate crop boundaries
            x1 = max(0, int(face_x - target_w / 2))
            x2 = min(w, x1 + target_w)
            
            # Adjust if we hit the right edge
            if x2 == w:
                x1 = max(0, w - target_w)
                
            cropped_clip = clip.crop(x1=x1, y1=0, x2=x2, y2=h)
            cropped_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
        return output_path
    except Exception as e:
        print(f"Error in smart crop: {e}")
        return video_path # return original if failed
