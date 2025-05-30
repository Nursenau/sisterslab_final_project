# sisterslab_final_project

# 📈 Bitcoin Kapanış Fiyatı Tahmini (2018–2025)

Bu proje, 2018–2025 yılları arasındaki günlük Bitcoin verilerini kullanarak, geçmiş fiyat hareketlerinden yola çıkarak **gelecekteki kapanış fiyatlarını tahmin etmeyi** amaçlamaktadır. Proje ayrıca bu tahminleri **Streamlit** ile görselleştiren interaktif bir uygulama içerir.

---

## 🎯 Proje Amacı

Kripto para piyasalarına olan ilgi ve yüksek volatilite, bu alanda **tahminleme modellerinin geliştirilmesini** önemli hale getirmiştir.  
Bu projede amacımız:

- Geçmiş fiyat desenlerini analiz etmek
- Günlük veriler üzerinden tahminleme algoritmaları uygulamak
- Modelin çıktısını gerçek verilerle karşılaştırmak
- Kullanıcıya interaktif bir arayüz sunarak kendi tahminlerini yapmasına olanak sağlamak

---

## 🗂️ Kullanılan Veri Setleri

1. `btc_1d_data_2018_to_2025.csv`  
   > 2018-01-01 ile 2025-05-23 arası Bitcoin günlük verileri.  
   Model bu verilerle eğitilmiştir.

2. `new.csv`  
   > 2025-05-24 ile 2025-05-28 arasındaki veriler.  
   Tahmin sonrası **gerçek değerlerle karşılaştırma** için kullanılmıştır.

---

## 🛠️ Kullanılan Teknolojiler

- Python
- Pandas, NumPy
- Scikit-Learn (`LinearRegression`)
- Streamlit (interaktif web arayüzü)
- Matplotlib

---

## 🔁 Kullanılan Yöntemler

### 1. **Lag-Based Regression (Zaman Serisi Yaklaşımı)**  
Model, her günün `Open`, `High`, `Low`, `Volume`, `Number of trades` gibi özelliklerine bakarak, **ertesi günün kapanış fiyatını (Close)** tahmin etmeyi öğrenir.

### 2. **Recursive Forecasting (Zincirleme Tahmin)**  
- Model ilk olarak 23 Mayıs 2025 verilerini kullanarak 24 Mayıs’ı tahmin eder.
- Ardından 24 Mayıs tahminini kullanarak 25 Mayıs’ı…
- Böylece 5 gün ileriye kadar tahmin yapılır.

---

## 📊 Model Performansı

- Kullanılan model: `LinearRegression`
- Başlıca metrikler:
  - MAE: Ortalama mutlak hata
  - RMSE: Kök ortalama kare hata
  - R²: Açıklanan varyans

Recursive tahmin sonucunda:
- Gün geçtikçe hata artışı gözlemlenmiştir.
- Modelin overfitting eğilimi düşük, ancak basitliği nedeniyle uzun vadede bozulma olabilir.

---

## 🖥️ Streamlit Uygulaması

Projede ayrıca bir `Streamlit` uygulaması geliştirildi:

- Model 23 Mayıs 2025'e kadar olan verilerle eğitilir
- Kullanıcı, tahmin etmek istediği günü belirtir
- Uygulama tahminleri üretir ve varsa gerçek kapanışla karşılaştırır
- Sonuçlar tablo ve grafikle sunulur

### Başlatmak için:

```bash
streamlit run feature_engineering_predict.py 
streamlit run model_own_prediction_success.py 