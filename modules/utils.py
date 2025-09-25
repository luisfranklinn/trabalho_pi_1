import os
import numpy as np
from PIL import Image

SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}

def pil_to_bool_array(img: Image.Image, threshold: int) -> np.ndarray:
    if img.mode not in ("L", "LA"):
        img = img.convert("L")
    arr = np.asarray(img, dtype=np.uint8)
    return (arr >= threshold).astype(np.uint8)


def bool_array_to_pil(arr: np.ndarray) -> Image.Image:
    arr = (arr * 255).astype(np.uint8)
    return Image.fromarray(arr, mode="L")


def to_gray_array(img: Image.Image) -> np.ndarray:
    """Converte uma imagem PIL para um array numpy de tons de cinza"""
    if img.mode not in ("L", "LA"):
        img = img.convert("L")
    return np.asarray(img, dtype=np.uint16)


def fit_image(img: Image.Image, target_wh: tuple[int, int]) -> Image.Image:
    """Redimensiona a imagem para caber nas dimensões alvo, mantendo a proporção."""
    tw, th = target_wh
    iw, ih = img.size
    scale = min(tw / iw, th / ih)
    scale = max(scale, 1e-6) # Evita divisão por zero se a imagem for 0x0
    nw, nh = max(1, int(iw * scale)), max(1, int(ih * scale))
    return img.resize((nw, nh), Image.NEAREST)


def list_image_files(root_dir: str) -> list[tuple[str, str]]:
    images = []
    if not root_dir:
        return images
    for root, _, files in os.walk(root_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in SUPPORTED_EXTS:
                path = os.path.join(root, f)
                rel_path = os.path.relpath(path, root_dir)
                images.append((path, rel_path))
    images.sort(key=lambda x: x[1].lower())
    return images