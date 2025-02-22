import os
import base64
from urllib.parse import urlparse

def is_url(string: str) -> bool:
    """Check if a string is a valid URL."""
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except:
        return False

def encode_image_to_base64(image_path: str) -> str:
    """Encode an image file to base64 string."""
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def prepare_image_input(image_input: str) -> str:
    """Prepare image input for API - handle both URLs and local files."""
    if is_url(image_input):
        return image_input
    
    if not os.path.exists(image_input):
        raise FileNotFoundError(f"Local image file not found: {image_input}")
    
    base64_image = encode_image_to_base64(image_input)
    return f"data:image/jpeg;base64,{base64_image}"