import os
import glob
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

from skintone_undertone_engine import extract_features_from_image, determine_undertone

def map_class_to_skintone(class_num):
    """
    Pemetaan kelas Monk Skin Tone 1-10 ke format aplikasi COCOKIN:
    - Kelas 1 - 3: Light (Fair)
    - Kelas 4 - 7: Medium
    - Kelas 8 - 10: Deep
    """
    c = int(class_num)
    if c <= 3:
        return "Light"
    elif c <= 7:
        return "Medium"
    else:
        return "Deep"

def prepare_dataset_features(base_dir, max_per_class=120):
    """
    Mengekstrak fitur dari sampel per kelas secara seimbang untuk training & evaluasi
    """
    rows = []
    print(f"Mengekstrak fitur dari {base_dir} (maks {max_per_class} per kelas)...")
    for cls in range(1, 11):
        cls_dir = os.path.join(base_dir, str(cls))
        if not os.path.isdir(cls_dir):
            continue
        files = glob.glob(os.path.join(cls_dir, "*.jpg"))
        np.random.seed(42)
        selected_files = np.random.choice(files, size=min(len(files), max_per_class), replace=False)
        
        for f in selected_files:
            feat = extract_features_from_image(f)
            if feat is not None:
                feat['raw_class'] = cls
                feat['skin_tone'] = map_class_to_skintone(cls)
                feat['file_path'] = f
                rows.append(feat)
                
    df = pd.DataFrame(rows)
    print(f"Total data terproses: {len(df)} sampel")
    return df

def train_and_evaluate():
    data_dir = r"D:\Semester 5\IPPL\COCOKIN-AI\images\images\all_cropped_skin_only_images"
    df = prepare_dataset_features(data_dir, max_per_class=120)
    
    # Feature columns
    features = ['R', 'G', 'B', 'H', 'S', 'V', 'L', 'a', 'b', 'ITA']
    X = df[features]
    y_3class = df['skin_tone']
    y_10class = df['raw_class']
    
    # Stratified split 80% Train, 20% Test
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y_3class, df.index, test_size=0.20, random_state=42, stratify=y_3class
    )
    
    print("\n--- Training Model Random Forest untuk Skin Tone (Light, Medium, Deep) ---")
    clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, class_weight='balanced')
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred) * 100
    
    print(f"\n🎯 Akurasi Model Evaluasi (Test Set): {acc:.2f}%")
    print("\nLaporan Klasifikasi:")
    print(classification_report(y_test, y_pred))
    
    print("Confusion Matrix:")
    labels = sorted(list(set(y_test)))
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=[f"Actual {l}" for l in labels], columns=[f"Pred {l}" for l in labels])
    print(cm_df)
    
    # Simpan model
    os.makedirs(r"D:\Semester 5\IPPL\COCOKIN-AI\models", exist_ok=True)
    model_path = r"D:\Semester 5\IPPL\COCOKIN-AI\models\skintone_model.pkl"
    joblib.dump(clf, model_path)
    print(f"\n✅ Model Skin Tone berhasil disimpan ke: {model_path}")
    
    # Simpan laporan baseline
    report_content = f"""# Laporan Hasil Baseline Model Skin Tone

**Model:** Random Forest Classifier (n_estimators=100, balanced)  
**Fitur Masukan:** RGB, HSV, CIE-L*a*b*, dan ITA (Individual Typology Angle)  
**Kelas Target:** Light, Medium, Deep (Pemetaan dari Skala Monk Skin Tone 1–10)  
**Total Sampel:** {len(df)} gambar kulit  
**Akurasi Test Set (20%):** {acc:.2f}%  

### Confusion Matrix:
```
{cm_df.to_string()}
```

### Classification Report:
```
{classification_report(y_test, y_pred)}
```
"""
    with open(r"D:\Semester 5\IPPL\COCOKIN-AI\reports\baseline_skintone_report.md", "w") as f:
        f.write(report_content)
    print("✅ Laporan evaluasi disimpan ke: reports/baseline_skintone_report.md")

if __name__ == "__main__":
    train_and_evaluate()
