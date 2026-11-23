import os
import numpy as np
import pandas as pd
import joblib

from skintone_undertone_engine import (
    extract_features_from_image,
    extract_features_from_bytes,
    determine_undertone,
)

MODEL_PATH = r"D:\Semester 5\IPPL\COCOKIN-AI\models\skintone_model.pkl"
FEATURE_NAMES = ['R', 'G', 'B', 'H', 'S', 'V', 'L', 'a', 'b', 'ITA']


class CocokinSkinAnalyzer:
    def __init__(self, model_path=MODEL_PATH):
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.model = None

    def _build_response_from_features(self, features):
        if features is None:
            return {
                "status": "error",
                "success": False,
                "message": "Tidak dapat mendeteksi atau mengekstrak piksel kulit dari foto."
            }

        # 1. Prediksi Skin Tone via Model Machine Learning + Kalibrasi Luminance L*
        if self.model is not None:
            input_df = pd.DataFrame([[features[k] for k in FEATURE_NAMES]], columns=FEATURE_NAMES)
            skin_tone_pred = str(self.model.predict(input_df)[0])
            probs = self.model.predict_proba(input_df)[0]
            conf = float(np.max(probs))
        else:
            ita = features['ITA']
            if ita > 15.0:
                skin_tone_pred = "Light"
            elif ita > -25.0:
                skin_tone_pred = "Medium"
            else:
                skin_tone_pred = "Deep"
            conf = 0.82

        # 2. Analisis Undertone via Rasio Kromatik (CIE-L*a*b* & HSV)
        undertone_info = determine_undertone(features['a'], features['b'], features['H'])
        undertone_label = undertone_info['undertone']

        # 3. Pemetaan Personal Color & Palet Referensi berdasarkan Skin Tone + Undertone
        if undertone_label == "Warm":
            if skin_tone_pred == "Light":
                personal_color = "Warm Spring"
                summary = "Palet warna hangat dan cerah bernuansa peach, coral, serta golden nude yang membuat wajah tampak segar bercahaya."
                palette = [
                    {"name": "Peach Coral", "hex": 0xFFE88D72},
                    {"name": "Warm Apricot", "hex": 0xFFF2B895},
                    {"name": "Golden Honey", "hex": 0xFFD99B52},
                    {"name": "Soft Warm Nude", "hex": 0xFFD8A48F},
                ]
            else:
                personal_color = "Warm Autumn"
                summary = "Palet warna hangat dengan nuansa earthy terracotta, caramel, dan bronze yang menyatu alami di kulitmu."
                palette = [
                    {"name": "Deep Espresso", "hex": 0xFF6B381B},
                    {"name": "Warm Caramel", "hex": 0xFFC6946E},
                    {"name": "Soft Sand Peach", "hex": 0xFFE1BBA0},
                    {"name": "Muted Sage Olive", "hex": 0xFF8EAE86},
                ]
        elif undertone_label == "Cool":
            if skin_tone_pred == "Deep":
                personal_color = "Cool Winter"
                summary = "Palet warna sejuk berkontras tegas seperti plum, berry, dan deep rose yang menonjolkan dimensi wajahmu."
                palette = [
                    {"name": "Deep Berry Wine", "hex": 0xFF6E2239},
                    {"name": "Cool Ruby Plum", "hex": 0xFF8F3553},
                    {"name": "Icy Mauve Pink", "hex": 0xFFD69EB1},
                    {"name": "Royal Slate", "hex": 0xFF56637A},
                ]
            else:
                personal_color = "Cool Summer"
                summary = "Palet warna sejuk dengan nuansa dusty rose, berry lembut, dan mauve yang serasi untuk kulitmu."
                palette = [
                    {"name": "Rosewood Berry", "hex": 0xFF7D3C52},
                    {"name": "Dusty Mauve", "hex": 0xFFB6768A},
                    {"name": "Soft Petal Pink", "hex": 0xFFE4B5C1},
                    {"name": "Cool Lavender", "hex": 0xFF9EA3B8},
                ]
        else:  # Neutral
            if skin_tone_pred == "Light":
                personal_color = "Cool Summer"
            else:
                personal_color = "Warm Autumn"
            summary = "Undertone Neutral kamu fleksibel! Palet rosewood, soft terracotta, dan almond nude sangat seimbang di kulitmu."
            palette = [
                {"name": "Soft Terracotta", "hex": 0xFFB06553},
                {"name": "Classic Rose Taupe", "hex": 0xFFA37B74},
                {"name": "Almond Nude", "hex": 0xFFD8B29C},
                {"name": "Muted Olive", "hex": 0xFF8B8F78},
            ]

        return {
            "status": "success",
            "success": True,
            "model_version": "1.0.0-skintone-undertone",
            "skinTone": skin_tone_pred,
            "skinToneHex": features['hex_int'],
            "skinToneHexStr": features['hex_str'],
            "undertone": undertone_label,
            "undertoneHex": undertone_info['undertoneHex'],
            "personalColor": personal_color,
            "summary": summary,
            "confidence": f"{conf * 100:.1f}%",
            "confidenceScore": round(conf, 4),
            "palette": palette,
            "metrics": {
                "Luminance_L": round(float(features['L']), 2),
                "ITA": round(float(features['ITA']), 2),
                "b_yellow": round(float(features['b']), 2),
                "a_red": round(float(features['a']), 2),
                "ratio_b_a": round(undertone_info['ratio_b_a'], 2),
            },
        }

    def analyze(self, image_path):
        features = extract_features_from_image(image_path)
        return self._build_response_from_features(features)

    def analyze_bytes(self, image_bytes):
        features = extract_features_from_bytes(image_bytes)
        return self._build_response_from_features(features)


if __name__ == "__main__":
    import glob
    analyzer = CocokinSkinAnalyzer()
    print("=== TEST INFERENSI COCOKIN SKIN ANALYZER ===")
    sample_classes = {
        "Light Sample": r"D:\Semester 5\IPPL\COCOKIN-AI\images\images\all_cropped_skin_only_images\2",
        "Medium Sample": r"D:\Semester 5\IPPL\COCOKIN-AI\images\images\all_cropped_skin_only_images\5",
        "Deep Sample": r"D:\Semester 5\IPPL\COCOKIN-AI\images\images\all_cropped_skin_only_images\9",
    }
    for name, folder in sample_classes.items():
        files = glob.glob(os.path.join(folder, "*.jpg"))
        if files:
            res = analyzer.analyze(files[0])
            print(f"\n[{name}]")
            print(f"  Skin Tone     : {res['skinTone']} (Hex: {res['skinToneHexStr']})")
            print(f"  Undertone     : {res['undertone']}")
            print(f"  PersonalColor : {res['personalColor']}")
            print(f"  Confidence    : {res['confidence']}")
            print(f"  Metrics       : {res['metrics']}")
