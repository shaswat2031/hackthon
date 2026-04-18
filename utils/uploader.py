import cloudinary
import cloudinary.uploader
import config

# Initialize Cloudinary
cloudinary.config( 
  cloud_name = config.CLOUDINARY_CLOUD_NAME,
  api_key = config.CLOUDINARY_API_KEY,
  api_secret = config.CLOUDINARY_API_SECRET
)

def upload_to_cloudinary(file_path: str):
    """
    Uploads a video to Cloudinary and returns the secure URL.
    """
    try:
        if not config.CLOUDINARY_CLOUD_NAME:
            return None
            
        print(f"Uploading {file_path} to Cloudinary...")
        response = cloudinary.uploader.upload_video(
            file_path,
            resource_type = "video",
            folder = "attentionx_clips"
        )
        return response.get("secure_url")
    except Exception as e:
        print(f"Cloudinary Upload Error: {e}")
        return None
