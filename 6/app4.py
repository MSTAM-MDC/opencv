import cv2

def load_video(video_path):
    """Load the video file."""
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise IOError("Error loading video file.")
    return video

def initialize_plate_detector():
    """Load the pre-trained cascade classifier for license plates."""
    classifier_path = cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml'
    plate_cascade = cv2.CascadeClassifier(classifier_path)
    if plate_cascade.empty():
        raise IOError("Failed to load cascade classifier.")
    return plate_cascade

def detect_and_display_plates(video):
    """Detect license plates in video and display the results in real-time."""
    plate_cascade = initialize_plate_detector()

    while True:
        # Read the next frame
        ret, frame = video.read()
        if not ret:
            break  # If no frame is returned, the video has ended

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around detected license plates
        for (x, y, w, h) in plates:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the current frame
        cv2.imshow('License Plates', frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

def main():
    video_path = r'C:\Users\MSTAM\OneDrive\Documents\GitHub\opencv\6\CARUSSR.mp4'
    try:
        video = load_video(video_path)
        detect_and_display_plates(video)
    except IOError as e:
        print(e)
    finally:
        video.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
