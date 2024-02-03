import cv2
import numpy as np

# Function to apply motion detection and create artistic display
def motion_capture_art(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # Initialize the previous frame
    if 'previous_frame' not in motion_capture_art.__dict__:
        motion_capture_art.previous_frame = gray
        return image
    
    # Calculate the absolute difference between the current and previous frames
    frame_diff = cv2.absdiff(motion_capture_art.previous_frame, gray)
    
    # Apply thresholding to highlight the motion regions
    ret, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create an artistic effect by drawing contours on the original image
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
    
    # Update the previous frame
    motion_capture_art.previous_frame = gray
    
    return image

# Create a resizable window
cv2.namedWindow('Motion Capture Artistic Display', cv2.WINDOW_NORMAL)

# Load a video file or use the webcam feed
video_capture = cv2.VideoCapture(0)  # Replace 0 with the index of your camera, or provide the video file path

while True:
    # Read a frame from the video feed
    ret, frame = video_capture.read()

    # Apply motion capture art effect
    artistic_frame = motion_capture_art(frame)

    # Display the artistic frame
    cv2.imshow('Motion Capture Artistic Display', artistic_frame)

    # Wait for the 'Esc' key to exit or any other key to continue
    key = cv2.waitKey(1)
    if key == 27:
        break

# Release the video capture and close the window
video_capture.release()
cv2.destroyAllWindows()