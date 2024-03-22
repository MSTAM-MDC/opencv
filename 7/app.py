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


def display_comparison(original_dir, enhanced_dir, filename):
    
    """
    Display a side-by-side comparison of the original and enhanced image.
    
    Parameters:
    - original_dir: Directory containing the original images.
    - enhanced_dir: Directory containing the enhanced images.
    - filename: The filename of the image to compare.
    """
    original_image_path = os.path.join(original_dir, filename)
    enhanced_image_path = os.path.join(enhanced_dir, 'enhanced_' + filename)

    # Load both images
    original_img = cv2.imread(original_image_path)
    enhanced_img = cv2.imread(enhanced_image_path)

    if original_img is None or enhanced_img is None:
        print(f"Failed to load one of the images: {original_image_path} or {enhanced_image_path}")
        return

    # Resize images to the same height if necessary for a better comparison
    if original_img.shape[0] != enhanced_img.shape[0]:
        height = min(original_img.shape[0], enhanced_img.shape[0])
        original_img = cv2.resize(original_img, (int(original_img.shape[1] * height / original_img.shape[0]), height))
        enhanced_img = cv2.resize(enhanced_img, (int(enhanced_img.shape[1] * height / enhanced_img.shape[0]), height))

    # Concatenate images horizontally (side by side)
    comparison_img = cv2.hconcat([original_img, enhanced_img])

    # Create a resizable window to display the comparison image
    cv2.namedWindow('Comparison', cv2.WINDOW_NORMAL)

    # Display the comparison image
    cv2.imshow('Comparison', comparison_img)

    # Wait for any key to be pressed
    cv2.waitKey(0)

    # Close all OpenCV windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Assuming the other parts of the script remain unchanged
    url = 'https://www.loc.gov/collections/world-war-i-and-1920-election-recordings/'
    base_dir = r'C:\Users\MSTAM\OneDrive\Documents\GitHub\opencv\7'
    download_images(url)
    enhance_images(os.path.join(base_dir, 'images'))
    enhanced_dir = os.path.join(base_dir, 'enhanced')

    original_images_dir = os.path.join(base_dir, 'images')
    enhanced_images_dir = os.path.join(base_dir, 'enhanced')
    # Display a side-by-side comparison of image_4.jpg and its enhanced version
    display_comparison(original_images_dir, enhanced_images_dir, 'image_4.jpg')