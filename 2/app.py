import cv2
import numpy as np

# Function to track the mouse click event
def mouse_event(event, x, y, flags, param):
    global hsv_img, selected_color

    if event == cv2.EVENT_LBUTTONDOWN:
        selected_color = hsv_img[y, x]

# Function to apply color filtering
def color_filter(image, lower_color, upper_color):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result

# Create a resizable window
cv2.namedWindow('Dynamic Color Filtering Art', cv2.WINDOW_NORMAL)

# Load an image
image = cv2.imread(r'C:\Users\MSTAM\OneDrive\Documents\GitHub\open-cv-projects\2\screenshot.png')  # Replace 'path_to_image' with the path to your image

if image is None:
    raise ValueError("Image not found or cannot be loaded.")

# Convert the image to HSV color space
hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Initialize the selected color variable
selected_color = np.uint8([[[0, 0, 0]]])

# Set the mouse event callback function
cv2.setMouseCallback('Dynamic Color Filtering Art', mouse_event)

while True:
    # Apply color filtering based on the selected color range
    lower_color = selected_color - np.array([20, 50, 50])
    upper_color = selected_color + np.array([20, 50, 50])
    filtered_image = color_filter(image, lower_color, upper_color)

    # Display the original and filtered images
    cv2.imshow('Dynamic Color Filtering Art', np.hstack([image, filtered_image]))

    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit the program
        break

cv2.destroyAllWindows()