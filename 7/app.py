import os
import requests
from bs4 import BeautifulSoup
import cv2

def create_directory_if_not_exists(directory_path):
    """Ensure the specified directory exists."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def download_images(base_url, num_images=5):
    """
    Download a specified number of images from a URL.
    
    Parameters:
    - base_url: The web page URL from which to scrape images.
    - num_images: The maximum number of images to download.
    """
    images_dir = os.path.join(base_dir, 'images')
    create_directory_if_not_exists(images_dir)

    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to retrieve content from {base_url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img', limit=num_images)

    for i, img in enumerate(images):
        try:
            img_url = img['src']
            img_data = requests.get(requests.compat.urljoin(base_url, img_url)).content
            with open(os.path.join(images_dir, f'image_{i}.jpg'), 'wb') as file:
                file.write(img_data)
        except Exception as e:
            print(f"Failed to download image {img_url}: {e}")

def enhance_images(input_dir):
    """
    Enhance all JPEG images in the specified directory.
    
    Parameters:
    - input_dir: Directory containing images to enhance.
    """
    enhanced_dir = os.path.join(base_dir, 'enhanced')
    create_directory_if_not_exists(enhanced_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg'):
            try:
                img_path = os.path.join(input_dir, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    equalized_img = cv2.equalizeHist(gray_img)
                    cv2.imwrite(os.path.join(enhanced_dir, f'enhanced_{filename}'), equalized_img)
                else:
                    print(f'Failed to load image {img_path}. Skipping.')
            except Exception as e:
                print(f"Error processing image {filename}: {e}")

def display_enhanced_image(image_path):
    """
    Display the specified image in a resizeable window.
    
    Parameters:
    - image_path: Path to the image to be displayed.
    """
    # Check if the image exists
    if not os.path.exists(image_path):
        print(f"The file {image_path} does not exist.")
        return
    
    # Load the image
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Failed to load image {image_path}.")
        return

    # Create a resizable window
    cv2.namedWindow('Enhanced Image', cv2.WINDOW_NORMAL)
    
    # Display the image in the window
    cv2.imshow('Enhanced Image', img)
    
    # Wait for any key to be pressed
    cv2.waitKey(0)
    
    # Close all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    url = 'https://www.loc.gov/collections/world-war-i-and-1920-election-recordings/'
    base_dir = r'C:\Users\MSTAM\OneDrive\Documents\GitHub\opencv\7'
    download_images(url)
    enhance_images(os.path.join(base_dir, 'images'))

    # Display the first enhanced image as an example
    enhanced_dir = os.path.join(base_dir, 'enhanced')
    first_image_path = os.listdir(enhanced_dir)[0]  # Get the first image in the enhanced directory
    display_enhanced_image(os.path.join(enhanced_dir, first_image_path))    