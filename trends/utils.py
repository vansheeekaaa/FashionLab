import requests
from pygltflib import GLTF2
from io import BytesIO
import tempfile
import numpy as np
from PIL import Image
import base64
import pandas as pd
import cv2
from skimage.metrics import structural_similarity as ssim
import os

# Define path for storing extracted images
EXTRACTED_IMAGES_DIR = 'data/extracted_images'
os.makedirs(EXTRACTED_IMAGES_DIR, exist_ok=True)

# Function to fetch the GLB file content
def fetch_glb_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise Exception(f"Failed to fetch file: {response.status_code}")

# Function to load and parse the GLB file from content
def load_glb_from_content(content):
    with tempfile.NamedTemporaryFile(delete=True, suffix=".glb") as temp_file:
        temp_file.write(content.read())
        temp_file.flush()
        gltf = GLTF2().load_binary(temp_file.name)
    return gltf

# Function to extract the 6th texture image from the GLB file (index 5)
def extract_sixth_texture_image(gltf):
    if len(gltf.textures) > 5:
        image_index = gltf.textures[5].source  # 6th texture (index 5)
        image = gltf.images[image_index]
        
        if image.uri:
            image_data = decode_base64_data_uri(image.uri)
        else:
            buffer_view = gltf.bufferViews[image.bufferView]
            buffer = gltf.buffers[buffer_view.buffer]
            data = gltf.get_data_from_buffer_uri(buffer.uri)
            start = buffer_view.byteOffset
            end = start + buffer_view.byteLength
            image_data = data[start:end]
        
        # Save and return the image path
        path = os.path.join(EXTRACTED_IMAGES_DIR, 'sixth_texture.png')
        with open(path, 'wb') as f:
            f.write(image_data)
        return path
    else:
        raise Exception("Less than 6 textures in the GLB file")

# Function to decode base64 data URIs
def decode_base64_data_uri(data_uri):
    header, encoded = data_uri.split(",", 1)
    return base64.b64decode(encoded)

# Function to fetch and preprocess an image from a file path
def fetch_and_preprocess_image(image_path, size=(100, 100)):
    try:
        image = Image.open(image_path).convert('RGB')
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        return cv2.resize(image, size)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

# Function to compare color histograms using Lab color space
def compare_color_histograms(image1, image2):
    image1_lab = cv2.cvtColor(image1, cv2.COLOR_BGR2Lab)
    image2_lab = cv2.cvtColor(image2, cv2.COLOR_BGR2Lab)
    
    hist1 = cv2.calcHist([image1_lab], [0, 1, 2], None, [16, 16, 16], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist([image2_lab], [0, 1, 2], None, [16, 16, 16], [0, 256, 0, 256, 0, 256])
    
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

# Function to compare structural similarity with SSIM and MSE
def compare_structural_similarity(image1, image2):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    ssim_score = ssim(gray1, gray2)
    mse_score = np.mean((gray1 - gray2) ** 2)
    
    return ssim_score, mse_score

# Function to process the GLB file and compare with dataset
def process_glb_and_compare(glb_url, dataset_csv):
    # Fetch the GLB content
    glb_content = fetch_glb_content(glb_url)

    # Load and parse the GLB file from content
    gltf = load_glb_from_content(glb_content)

    # Extract the 6th texture image
    sixth_texture_image_path = extract_sixth_texture_image(gltf)
    extracted_texture_image = fetch_and_preprocess_image(sixth_texture_image_path)

    # Load dataset
    df = pd.read_csv(dataset_csv)

    best_score = float('-inf')
    best_match_img = None
    best_match_link = None

    # Compare each image in the dataset with the extracted texture image
    for index, row in df.iterrows():
        try:
            image_url = row['img'].strip()  # Remove any extra spaces
            link = row['link '].strip()     # Remove any extra spaces
            
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content)).convert('RGB')
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            image = cv2.resize(image, (100, 100))

            if image is not None:
                color_score = compare_color_histograms(extracted_texture_image, image)
                ssim_score, mse_score = compare_structural_similarity(extracted_texture_image, image)
                similarity_score = 0.7 * color_score + 0.3 * ssim_score

                if similarity_score > best_score:
                    best_score = similarity_score
                    best_match_img = image_url
                    best_match_link = link
                
        except Exception as e:
            print(f"Error processing row {index}: {e}")

    return best_match_img, best_match_link
