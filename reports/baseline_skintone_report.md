# Laporan Hasil Baseline Model Skin Tone

**Model:** Random Forest Classifier (n_estimators=100, balanced)  
**Fitur Masukan:** RGB, HSV, CIE-L*a*b*, dan ITA (Individual Typology Angle)  
**Kelas Target:** Light, Medium, Deep (Pemetaan dari Skala Monk Skin Tone 1–10)  
**Total Sampel:** 986 gambar kulit  
**Akurasi Test Set (20%):** 76.26%  

### Confusion Matrix:
```
               Pred Deep  Pred Light  Pred Medium
Actual Deep           27           1            1
Actual Light           2          50           20
Actual Medium          3          20           74
```

### Classification Report:
```
              precision    recall  f1-score   support

        Deep       0.84      0.93      0.89        29
       Light       0.70      0.69      0.70        72
      Medium       0.78      0.76      0.77        97

    accuracy                           0.76       198
   macro avg       0.78      0.80      0.79       198
weighted avg       0.76      0.76      0.76       198

```
