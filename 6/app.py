import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the image
image = cv2.imread(r'C:\Users\MSTAM\OneDrive\Documents\GitHub\opencv\6\car6.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load the pre-trained cascade classifier for license plates
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# Detect license plates in the image
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Initialize an empty list to store the extracted text
extracted_text = []

# Iterate over the detected license plates
for (x, y, w, h) in plates:
    # Extract the license plate region from the grayscale image
    plate_region = gray[y:y+h, x:x+w]
    
    # Apply OCR to the license plate region
    text = pytesseract.image_to_string(plate_region, config='--psm 7')
    
    # Append the extracted text to the list
    extracted_text.append(text)

    # Draw rectangles around the detected license plates
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Save the extracted text to a .txt file
with open('6/extract/extracted_text.txt', 'w') as file:
    file.write('\n'.join(extracted_text))

# Display the image with the detected license plates
cv2.imshow('License Plates', image)
cv2.waitKey(0)
cv2.destroyAllWindows()