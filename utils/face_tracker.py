import cv2

def get_face_center(frame):
    """
    Detects face and returns the center X coordinate.
    Uses the most basic MediaPipe structure to avoid Windows module errors.
    """
    try:
        import mediapipe as mp
        # Use a local reference to ensure solutions is accessible
        mp_solutions = getattr(mp, "solutions", None)
        if mp_solutions is None:
            return None
            
        mp_face = mp_solutions.face_detection
        
        with mp_face.FaceDetection(min_detection_confidence=0.5) as fd:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = fd.process(rgb)
            if results.detections:
                det = results.detections[0]
                bbox = det.location_data.relative_bounding_box
                h, w = frame.shape[:2]
                cx = int((bbox.xmin + bbox.width/2) * w)
                return cx
            return None
    except Exception as e:
        # Silently fail so the engine can fallback to center-crop
        return None
