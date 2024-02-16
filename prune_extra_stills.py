# function that compares images in a directory and removes images where nothing in the image has changed

import os
import cv2
import numpy as np
from PIL import Image
import imagehash
import matplotlib.pyplot as plt

def image_hash(image_path, hash_size=8):
    with Image.open(image_path) as img:
        hash = imagehash.average_hash(img, hash_size)
    return hash

def prune_extra_stills(directory):
    image_hashes = {}
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".jpg"):
            image_path = os.path.join(directory, filename)
            hash = image_hash(image_path, hash_size=8)
            if hash in image_hashes:
                print(f"Removing duplicate image: {filename}")
                os.remove(image_path)
            else:
                print(f"Keeping image: {filename}")
                image_hashes[hash] = image_path

path = os.path.join('captures', 'pruning')
prune_extra_stills(path)