import numpy as np
from PIL import Image

def compress_image_svd(image_path, k):
    img = Image.open(image_path)
    img = img.convert('RGB')
    img_arr = np.array(img)

    compressed = np.zeros(img_arr.shape, dtype=np.uint8)

    for i in range(3):  # R, G, B
        U, s, VT = np.linalg.svd(img_arr[:, :, i], full_matrices=False)
        S = np.diag(s[:k])
        channel = np.dot(U[:, :k], np.dot(S, VT[:k, :]))
        channel = np.clip(channel, 0, 255)
        compressed[:, :, i] = channel

    return img_arr, compressed
