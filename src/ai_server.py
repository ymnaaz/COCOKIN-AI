import os
import json
import glob
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from predict_skintone_undertone import CocokinSkinAnalyzer

PORT = int(os.environ.get("AI_PORT", "8000"))
DATASET_SKIN_DIR = r"D:\Semester 5\IPPL\COCOKIN-AI\images\images\all_cropped_skin_only_images"
DATASET_FACE_DIR = r"D:\Semester 5\IPPL\COCOKIN-AI\images\images\all_cropped_images_by_class"

analyzer = CocokinSkinAnalyzer()

# Pre-index beberapa sampel foto asli dari dataset COCOKIN-AI untuk pengujian cepat dari UI
SAMPLE_PRESETS = {
    "sample_light": os.path.join(DATASET_FACE_DIR, "1"),
    "sample_medium_warm": os.path.join(DATASET_FACE_DIR, "4"),
    "sample_tan_warm": os.path.join(DATASET_FACE_DIR, "6"),
    "sample_deep": os.path.join(DATASET_FACE_DIR, "9"),
}


def resolve_sample_path(preset_key):
    folder = SAMPLE_PRESETS.get(preset_key)
    if folder and os.path.isdir(folder):
        files = sorted(glob.glob(os.path.join(folder, "*.jpg")))
        if files:
            return files[0]
    # Default fallback sample dari kelas 4
    fallback_files = sorted(glob.glob(os.path.join(DATASET_FACE_DIR, "4", "*.jpg")))
    return fallback_files[0] if fallback_files else None


class CocokinAIHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ["/health", "/api/health"]:
            self._send_json(200, {
                "status": "ok",
                "service": "COCOKIN Python AI Service (Skin Tone & Undertone)",
                "model_loaded": analyzer.model is not None,
                "port": PORT,
            })
            return

        if parsed.path in ["/model-info", "/api/model-info"]:
            self._send_json(200, {
                "status": "ok",
                "model_type": "RandomForestClassifier + CIE-Lab Chromatic Undertone Engine",
                "features": ["R", "G", "B", "H", "S", "V", "L", "a", "b", "ITA"],
                "targets": {
                    "skinTone": ["Light", "Medium", "Deep"],
                    "undertone": ["Warm", "Cool", "Neutral"],
                },
            })
            return

        self._send_json(404, {"status": "error", "message": "Endpoint tidak ditemukan"})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path not in ["/predict", "/api/predict"]:
            self._send_json(404, {"status": "error", "message": "Endpoint tidak ditemukan"})
            return

        content_len = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        try:
            body = json.loads(raw_body.decode("utf-8"))
        except Exception:
            body = {}

        image_base64 = body.get("imageBase64") or body.get("image_base64")
        image_path = body.get("imagePath") or body.get("image_path")
        sample_key = body.get("sampleKey") or body.get("preset")

        # 1. Jika ada kiriman foto asli dalam bentuk Base64 dari Flutter / Backend
        if image_base64:
            try:
                # Bersihkan header data:image/...;base64, jika ada
                if "," in image_base64:
                    image_base64 = image_base64.split(",", 1)[1]
                img_bytes = base64.b64decode(image_base64)
                result = analyzer.analyze_bytes(img_bytes)
                status = 200 if result.get("success") else 400
                self._send_json(status, result)
                return
            except Exception as e:
                self._send_json(400, {
                    "status": "error",
                    "success": False,
                    "message": f"Gagal mendekode base64 foto: {str(e)}",
                })
                return

        # 2. Jika ada path file lokal yang valid di disk
        if image_path and os.path.exists(image_path):
            result = analyzer.analyze(image_path)
            status = 200 if result.get("success") else 400
            self._send_json(status, result)
            return

        # 3. Jika memilih sample foto wajah nyata dari dataset COCOKIN-AI
        resolved = resolve_sample_path(sample_key or "sample_medium_warm")
        if resolved and os.path.exists(resolved):
            result = analyzer.analyze(resolved)
            result["analyzedFile"] = os.path.basename(resolved)
            self._send_json(200, result)
            return

        self._send_json(400, {
            "status": "error",
            "success": False,
            "message": "Tidak ada data foto (imageBase64 / imagePath) yang dikirim.",
        })


def run_server():
    server = HTTPServer(("0.0.0.0", PORT), CocokinAIHandler)
    print("==========================================================")
    print("🎨 COCOKIN Python AI Service Aktif!")
    print(f"URL Predict : http://localhost:{PORT}/predict")
    print(f"URL Health  : http://localhost:{PORT}/health")
    print("==========================================================")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
