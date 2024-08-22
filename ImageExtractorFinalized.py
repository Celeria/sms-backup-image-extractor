# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 20:31:49 2024

@author: patm3
"""

import xml.etree.ElementTree as ET
from PIL import Image
import os
import base64
import io
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from binascii import Error
from timeit import default_timer as timer

start = timer()

def process_image(mms, part, output_folder, input_contact):
    image_data = base64.b64decode(part.get('data'))
    timestamp = datetime.fromtimestamp(int(mms.get('date')) / 1000)
    image_format = part.get('ct').split('/')[-1]
    contact_name = mms.get('contact_name') or "Unknown Contact"

    # Determine if the image should be processed based on contact name
    if input_contact and input_contact != contact_name:
        return None  # Skip if specific contact is given and doesn't match

    # Filter invalid characters from contact name for folder creation
    valid_contact_name = re.sub(r'[<>:"/\\|?*]', '_', contact_name)

    # Create output path directly (no separate if-else blocks)
    contact_output_folder = os.path.join(output_folder, valid_contact_name)
    os.makedirs(contact_output_folder, exist_ok=True)
    output_path = os.path.join(contact_output_folder, f"{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.{image_format}")

    try:
        image_data = base64.b64decode(part.get('data'))
        
        # Load image using Image.open
        with Image.open(io.BytesIO(image_data)) as img:
            # Handle RGBA images by converting to RGB if necessary
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # Save directly to file (avoid extra in-memory BytesIO)
            img.save(output_path, format=image_format.upper())
            img.close()  # Ensure data is flushed to disk
            print(output_path)
            return output_path
    
    except Error as e: #catch base64 errors
        print(f"Warning: Invalid base64 data in image: {e}")
        return None
    except Exception as e:  # Catch other potential errors
        print(f"Warning: Error processing image data: {e}")
        return None
    
def extract_images(xml_file_path, contact_name, output_folder):
    """Extracts base64 encoded images from an XML file, decodes them, and saves them into
    folders named after the contacts with human-readable filenames based on the MMS date.

    Args:
        xml_file_path (str): The path to the XML file.
        output_folder (str): The base path where contact-specific folders will be created.
        max_workers (int, optional): The maximum number of threads to use for parallel processing. Defaults to 10.

    Returns:
        list: A list of paths to the saved image files.
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    os.makedirs(output_folder, exist_ok=True)

    with ThreadPoolExecutor(max_workers=1) as executor:
        [executor.submit(process_image, mms, part, output_folder, contact_name)
                   for mms in root.findall('mms')
                   for part in mms.findall('parts/part')
                   if part.get('ct').startswith('image/')]

    return True


# Example usage:
xml_file_path = "sms-20240818054310.xml"
contact_name = ""  # Leave empty to extract images from all contacts
output_folder = f"extracted_images_{contact_name or 'all'}"

extract_images(xml_file_path, contact_name, output_folder)

print(timer() - start)