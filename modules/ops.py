import numpy as np
from PIL import Image
from . import utils

def _align_shapes(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    h = min(a.shape[0], b.shape[0])
    w = min(a.shape[1], b.shape[1])
    return a[:h, :w], b[:h, :w]


def perform_operation(op: str, imgA: Image.Image, imgB: Image.Image | None, thrA: int, thrB: int, modo: str) -> Image.Image | None:
    if op == "not":
        a = utils.pil_to_bool_array(imgA, thrA)
        res_arr = 1 - a
        return utils.bool_array_to_pil(res_arr)

    if imgB is None:
        return None 

    if op in {"and", "or", "xor"} or modo == "logico":
        a = utils.pil_to_bool_array(imgA, thrA)
        b = utils.pil_to_bool_array(imgB, thrB)
        a, b = _align_shapes(a, b)

        if op == "and": res_arr = a & b
        elif op == "or": res_arr = a | b
        elif op == "xor": res_arr = a ^ b
        elif op == "add": res_arr = np.clip(a + b, 0, 1)
        elif op == "sub": res_arr = np.clip(a - b, 0, 1)
        elif op == "mul": res_arr = a * b
        elif op == "div": res_arr = np.where(b == 1, a, 0).astype(np.uint8)
        else: return None

        return utils.bool_array_to_pil(res_arr)

    if modo == "aritmetico":
        a = utils.to_gray_array(imgA)
        b = utils.to_gray_array(imgB)
        a, b = _align_shapes(a, b)

        if op == "add":
            res_arr = np.clip(a + b, 0, 255)
        elif op == "sub":
            res_arr = np.clip(a - b, 0, 255)
        elif op == "mul":
            res_arr = np.clip((a * b) / 255.0, 0, 255)
        elif op == "div":
            a1 = a.astype(np.uint32) + 1
            b1 = b.astype(np.uint32) + 1
            res_arr = np.clip((a1 * 255) / b1, 0, 255)
        else:
            return None

        return Image.fromarray(res_arr.astype(np.uint8), mode="L")

    return None