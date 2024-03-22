import cv2
import numpy as np

# Load the three input images
image1 = cv2.imread(r'C:\Users\MSTAM\OneDrive\Documents\GitHub\opencv\9\1.jpg')
image2 = cv2.imread(r'C:\Users\MSTAM\OneDrive\Documents\GitHub\opencv\9\2.jpg')
image3 = cv2.imread(r'C:\Users\MSTAM\OneDrive\Documents\GitHub\opencv\9\3.jpg')

# Resize the images (optional)
# image1 = cv2.resize(image1, (800, 600))
# image2 = cv2.resize(image2, (800, 600))
# image3 = cv2.resize(image3, (800, 600))

# Stitch the images together
stitcher = cv2.Stitcher_create()
status, panorama = stitcher.stitch([image1, image2, image3])

# Check if stitching was successful
if status == cv2.Stitcher_OK:
    # Display the panoramic view
    cv2.imshow('Panorama', panorama)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print('Stitching failed')