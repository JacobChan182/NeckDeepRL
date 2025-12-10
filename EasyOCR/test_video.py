import cv2
import easyocr
import os
from pathlib import Path

# Initialize EasyOCR reader (only once for efficiency)
reader = easyocr.Reader(['en'])

# Load coordinates from files
def load_coords(coords_file):
    """Load coordinates from a text file."""
    coords = {}
    if os.path.exists(coords_file):
        with open(coords_file, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=')
                    coords[key.strip()] = int(value.strip())
    return coords

# Load health and score coordinates
health_coords = load_coords('Health/Coords.txt')
score_coords = load_coords('Score/Coords.txt')

# Health coordinates (x1, y1, x2, y2)
health_x1 = health_coords.get('score_x1', 115)  # Note: file uses score_x1 but it's for health
health_y1 = health_coords.get('score_y1', 150)
health_x2 = health_coords.get('score_x2', 400)
health_y2 = health_coords.get('score_y2', 175)

# Score coordinates (x1, y1, x2, y2)
score_x1 = score_coords.get('score_x1', 100)
score_y1 = score_coords.get('score_y1', 125)
score_x2 = score_coords.get('score_x2', 400)
score_y2 = score_coords.get('score_y2', 150)

def read_text_from_region(frame, x1, y1, x2, y2, region_name=""):
    """Extract text from a specific region of the frame."""
    try:
        # Crop the region
        crop = frame[y1:y2, x1:x2]
        
        if crop.size == 0:
            return None
        
        # Preprocess for better OCR: convert to grayscale and enhance contrast
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        # Apply threshold to make text more readable
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Read text using EasyOCR (try both original and preprocessed)
        results = reader.readtext(thresh, detail=0)
        
        # If no results, try original crop
        if not results:
            results = reader.readtext(crop, detail=0)
        
        if results:
            # Filter out non-numeric strings and extract numbers
            import re
            for text in results:
                # Try to extract numeric value
                text_clean = text.strip().replace(' ', '').replace('O', '0').replace('o', '0').replace('l', '1').replace('I', '1')
                # If it's just numbers, return it
                if text_clean.isdigit():
                    return int(text_clean)
                # Try to extract first number found
                numbers = re.findall(r'\d+', text_clean)
                if numbers:
                    return int(numbers[0])
            
            # If no number found, return first result as string for debugging
            return results[0] if results else None
        return None
    except Exception as e:
        print(f"Error reading {region_name}: {e}")
        return None

def test_video(video_path, frame_interval=30, display=True):
    """
    Test OCR on video frames.
    
    Args:
        video_path: Path to video file
        frame_interval: Process every Nth frame (default: 30)
        display: Whether to display frames with annotations
    """
    # Open video
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    frame_count = 0
    processed_count = 0
    
    print(f"Testing OCR on {video_path}")
    print(f"Processing every {frame_interval} frames...")
    print("-" * 50)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Process every Nth frame
        if frame_count % frame_interval == 0:
            # Read health and score
            health = read_text_from_region(frame, health_x1, health_y1, health_x2, health_y2, "health")
            score = read_text_from_region(frame, score_x1, score_y1, score_x2, score_y2, "score")
            
            processed_count += 1
            
            # Print results
            print(f"Frame {frame_count}: Health={health}, Score={score}")
            
            if display:
                # Create a copy for display
                display_frame = frame.copy()
                
                # Draw rectangles around regions
                cv2.rectangle(display_frame, (health_x1, health_y1), (health_x2, health_y2), (0, 255, 0), 2)
                cv2.rectangle(display_frame, (score_x1, score_y1), (score_x2, score_y2), (0, 0, 255), 2)
                
                # Add text labels
                cv2.putText(display_frame, f"Health: {health}", (health_x1, health_y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(display_frame, f"Score: {score}", (score_x1, score_y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(display_frame, f"Frame: {frame_count}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                # Resize if too large (for display)
                height, width = display_frame.shape[:2]
                if width > 1280:
                    scale = 1280 / width
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    display_frame = cv2.resize(display_frame, (new_width, new_height))
                
                # Try to show frame (may not work with headless opencv)
                try:
                    cv2.imshow('OCR Test - Press Q to quit, Space to pause', display_frame)
                    # Wait for key press
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break
                    elif key == ord(' '):  # Space to pause/unpause
                        cv2.waitKey(0)
                except cv2.error:
                    # Headless mode - just continue processing
                    pass
    
    cap.release()
    try:
        cv2.destroyAllWindows()
    except:
        pass  # Ignore if windows can't be destroyed (headless mode)
    
    print("-" * 50)
    print(f"Processed {processed_count} frames out of {frame_count} total frames")

if __name__ == "__main__":
    import sys
    
    # Get the video path
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        # Try common locations
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(script_dir, "..", "Gameplay.mp4"),  # From EasyOCR to root
            os.path.join(script_dir, "Gameplay.mp4"),  # In EasyOCR directory
            "Gameplay.mp4",  # Current directory
        ]
        
        video_path = None
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                video_path = abs_path
                break
        
        if not video_path:
            print("Could not find Gameplay.mp4. Please specify the path:")
            print("Usage: python test_video.py <path_to_video>")
            video_path = input("Enter path to Gameplay.mp4: ").strip().strip('"')
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        sys.exit(1)
    
    print(f"Using video: {video_path}")
    
    # Test with display (set to False to just print results)
    test_video(video_path, frame_interval=30, display=True)

