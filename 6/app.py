import cv2

# Load the image
image = cv2.imread(r'C:\Users\MSTAM\OneDrive\Documents\GitHub\opencv\6\car3.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load the pre-trained cascade classifier for license plates
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# Detect license plates in the image
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around the detected license plates
for (x, y, w, h) in plates:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Display the image with the detected license plates
cv2.imshow('License Plates', image)
cv2.waitKey(0)
cv2.destroyAllWindows()