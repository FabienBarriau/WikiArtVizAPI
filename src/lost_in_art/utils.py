import random
from PIL import Image
from io import BytesIO


def sorted_random_sample(population_size: int, k: int):
    return sorted(random.sample(list(range(population_size)), k))


def convert_bytes_to_img(file: bytes) -> Image:
    try:
        img = Image.open(BytesIO(file))
        img = img.convert('RGB')
        return img
    except:
        print("Failed to load as image")
        return -1
