import os
import io
import glob
import base64
import numpy as np
import pandas as pd
from PIL import Image

def rgb_to_lab(rgb_norm):
    """
    Konversi RGB [0, 1] ke CIE-L*a*b* standar (sRGB D65)
    Mendukung input 1D array [R, G, B]
    """
    mask = rgb_norm > 0.04045
    rgb_lin = np.where(mask, ((rgb_norm + 0.055) / 1.055) ** 2.4, rgb_norm / 12.92)
    
    M = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])
    xyz = np.dot(rgb_lin, M.T)
    
    ref = np.array([0.95047, 1.00000, 1.08883])
    xyz_ref = xyz / ref
    
    delta = 6.0 / 29.0
    f_mask = xyz_ref > (delta ** 3)
    f = np.where(f_mask, xyz_ref ** (1.0 / 3.0), (xyz_ref / (3 * delta ** 2)) + (4.0 / 29.0))
    
    L = 116.0 * f[1] - 16.0
    a = 500.0 * (f[0] - f[1])
    b = 200.0 * (f[1] - f[2])
    return float(L), float(a), float(b)

def _extract_skin_pixels_from_rgb_array(rgb):
    """
    Mengekstrak piksel kulit dari array RGB (H, W, 3):
    1. Jika gambar sudah di-masking (background hitam > 30% piksel), ambil semua piksel non-hitam.
    2. Jika foto wajah utuh (memiliki background), ambil ROI wajah bagian tengah (dahi & pipi kiri-kanan)
       dan terapkan filter kromatik kulit (YCbCr skin range & non-shadow/highlight) agar rambut/background tidak ikut.
    """
    h, w, _ = rgb.shape
    non_black_mask = (rgb[:, :, 0] > 15) | (rgb[:, :, 1] > 15) | (rgb[:, :, 2] > 15)
    black_ratio = 1.0 - (np.count_nonzero(non_black_mask) / float(h * w))

    if black_ratio > 0.25:
        # Gambar skin-only (background hitam seperti pada dataset all_cropped_skin_only_images)
        skin_pixels = rgb[non_black_mask]
    else:
        # Foto potret wajah utuh: ambil ROI tengah wajah (area dahi + pipi, 25%..75% vertikal & 25%..75% horizontal)
        y1, y2 = int(h * 0.22), int(h * 0.78)
        x1, x2 = int(w * 0.22), int(w * 0.78)
        roi = rgb[y1:y2, x1:x2]

        r = roi[:, :, 0]
        g = roi[:, :, 1]
        b = roi[:, :, 2]

        # Konversi ke YCbCr untuk mendeteksi kandidat piksel kulit manusia (terang maupun gelap)
        y_val = 0.299 * r + 0.587 * g + 0.114 * b
        cb = 128.0 - 0.168736 * r - 0.331264 * g + 0.5 * b
        cr = 128.0 + 0.5 * r - 0.418688 * g - 0.081312 * b

        skin_mask = (
            (y_val > 20) & (y_val < 245) &
            (cb >= 75) & (cb <= 135) &
            (cr >= 130) & (cr <= 180) &
            (r > b)
        )
        if np.count_nonzero(skin_mask) >= 40:
            skin_pixels = roi[skin_mask]
        else:
            # Fallback ke ROI tengah tanpa piksel ekstrem gelap/putih silau
            valid_mask = (y_val > 18) & (y_val < 245)
            skin_pixels = roi[valid_mask] if np.count_nonzero(valid_mask) >= 20 else roi.reshape(-1, 3)

    if len(skin_pixels) < 20:
        skin_pixels = rgb.reshape(-1, 3)

    return skin_pixels

def extract_features_from_pil(pil_img):
    """
    Mengekstrak fitur RGB, HSV, CIE-Lab, ITA, dan Hex dari objek PIL.Image
    """
    rgb = np.array(pil_img.convert('RGB'), dtype=np.float32)
    skin_pixels = _extract_skin_pixels_from_rgb_array(rgb)

    mean_rgb = np.mean(skin_pixels, axis=0)
    r, g, b = float(mean_rgb[0]), float(mean_rgb[1]), float(mean_rgb[2])

    rgb_norm = np.clip(mean_rgb / 255.0, 0.0, 1.0)
    L, a_val, b_val = rgb_to_lab(rgb_norm)

    # Individual Typology Angle (ITA)
    ita = float(np.arctan2(L - 50.0, b_val) * (180.0 / np.pi))

    max_c = float(np.max(rgb_norm))
    min_c = float(np.min(rgb_norm))
    delta = max_c - min_c
    v = max_c * 255.0
    s = (delta / max_c * 255.0) if max_c > 0 else 0.0
    if delta == 0:
        h = 0.0
    elif max_c == rgb_norm[0]:
        h = float((60.0 * ((rgb_norm[1] - rgb_norm[2]) / delta) + 360.0) % 360.0)
    elif max_c == rgb_norm[1]:
        h = float((60.0 * ((rgb_norm[2] - rgb_norm[0]) / delta) + 120.0) % 360.0)
    else:
        h = float((60.0 * ((rgb_norm[0] - rgb_norm[1]) / delta) + 240.0) % 360.0)

    r_i = int(np.clip(round(r), 0, 255))
    g_i = int(np.clip(round(g), 0, 255))
    b_i = int(np.clip(round(b), 0, 255))
    hex_color = f"#{r_i:02x}{g_i:02x}{b_i:02x}"
    hex_int = int(f"0xFF{r_i:02x}{g_i:02x}{b_i:02x}", 16)

    return {
        'R': r, 'G': g, 'B': b,
        'H': h, 'S': s, 'V': v,
        'L': L, 'a': a_val, 'b': b_val,
        'ITA': ita,
        'hex_str': hex_color,
        'hex_int': hex_int
    }

def extract_features_from_image(image_path):
    """
    Ekstraksi rata-rata piksel RGB, HSV, dan CIE-Lab dari file gambar di disk
    """
    try:
        with Image.open(image_path) as img:
            return extract_features_from_pil(img)
    except Exception:
        return None

def extract_features_from_bytes(image_bytes):
    """
    Ekstraksi rata-rata piksel RGB, HSV, dan CIE-Lab langsung dari byte gambar (base64 / upload)
    """
    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            return extract_features_from_pil(img)
    except Exception:
        return None

def determine_undertone(a_val, b_val, h_val):
    """
    Aturan Pengolahan Citra Digital (PCD) untuk Undertone pada ruang warna CIE-L*a*b*:
    - Sumbu b* (kuning vs biru) terhadap a* (merah):
      * Warm: rasio b*/a* tinggi (pigmen keemasan/kuning dominan)
      * Cool: rasio b*/a* rendah atau b* rendah (pigmen pink/merah/kebiruan dominan)
      * Neutral: rasio b*/a* berada di zona keseimbangan
    """
    ratio = b_val / (max(abs(a_val), 1e-4))
    
    if b_val >= 14.5 and ratio >= 1.35:
        label = "Warm"
        desc = "Rona hangat dengan pigmen kuning/keemasan alami."
        hex_undertone = 0xFFDEC4A1
    elif b_val < 12.0 or ratio <= 1.15:
        label = "Cool"
        desc = "Rona sejuk dengan nuansa rosy pink atau kebiruan lembut."
        hex_undertone = 0xFFE8C7C8
    else:
        label = "Neutral"
        desc = "Keseimbangan harmonis antara rona hangat keemasan dan sejuk."
        hex_undertone = 0xFFE4D2C5
        
    return {
        'undertone': label,
        'description': desc,
        'undertoneHex': hex_undertone,
        'ratio_b_a': float(ratio)
    }

if __name__ == "__main__":
    print("Mengecek modul ekstraksi...")
    sample_dir = r"D:\Semester 5\IPPL\COCOKIN-AI\images\images\all_cropped_skin_only_images"
    test_files = glob.glob(os.path.join(sample_dir, "*", "*.jpg"))[:5]
    for f in test_files:
        feats = extract_features_from_image(f)
        ut = determine_undertone(feats['a'], feats['b'], feats['H'])
        cls = os.path.basename(os.path.dirname(f))
        print(f"File Class {cls}: L={feats['L']:.1f}, b*={feats['b']:.1f}, a*={feats['a']:.1f} -> {ut['undertone']} ({feats['hex_str']})")
    print("Ekstraksi modul berhasil berjalan!")
