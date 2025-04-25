import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import random

# Görüntüyü yükle ve gri tonlamaya çevir
def load_grayscale_image(path):
    img = imageio.imread(path)
    if len(img.shape) == 3:
        # Renkli ise griye çevir
        img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    return img.astype(np.uint8)

# Eşikleme
def threshold(image, thresh):
    return np.where(image >= thresh, 255, 0).astype(np.uint8)

# Sobel kenar algılama
def sobel_edge_detection(image):
    Gx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])

    Gy = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]])

    img = image.astype(float)
    height, width = img.shape
    result = np.zeros((height, width))

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            region = img[i-1:i+2, j-1:j+2]
            sx = np.sum(Gx * region)
            sy = np.sum(Gy * region)
            result[i, j] = np.sqrt(sx**2 + sy**2)

    return np.clip(result, 0, 255).astype(np.uint8)

# Gürültü ekleme (Tuz ve karabiber)
def add_salt_and_pepper_noise(image, amount=0.05):
    noisy = image.copy()
    total = image.size
    num_noise = int(total * amount)

    for _ in range(num_noise):
        i = random.randint(0, image.shape[0] - 1)
        j = random.randint(0, image.shape[1] - 1)
        noisy[i, j] = 0 if random.random() < 0.5 else 255
    return noisy

# Ortalama filtre
def mean_filter(image):
    padded = np.pad(image, ((1, 1), (1, 1)), mode='edge')
    filtered = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded[i:i+3, j:j+3]
            filtered[i, j] = np.mean(region)

    return filtered.astype(np.uint8)



