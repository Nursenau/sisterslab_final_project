import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Bitcoin Tahmini", layout="centered")
st.title("📅 Bitcoin Kapanış Fiyatı Tahmini")

# Veri yükle
df = pd.read_csv("data/new.csv")
df['Open time'] = pd.to_datetime(df['Open time'])

# Özellik ve hedef belirle
features = ['Open', 'High', 'Low', 'Volume', 'Number of trades']
X = df[features]
y = df['Close']

# Modeli eğit
model = LinearRegression()
model.fit(X, y)

# Tahmin yapılacak tarih
tahmin_tarihi = st.date_input("Tahmin Yapılacak Tarih", pd.to_datetime("2025-05-24"))

# Bir önceki günün verisini al
prev_day = tahmin_tarihi - pd.Timedelta(days=1)
row_prev = df[df['Open time'] == pd.to_datetime(prev_day)]

# Eğer önceki günün verisi yoksa uyar
if row_prev.empty:
    st.warning(f"⚠️ {prev_day} tarihli veriler bulunamadı. Tahmin yapılamaz.")
else:
    # Tahmin yap
    input_features = row_prev[features].values
    prediction = model.predict(input_features)[0]
    
    st.success(f"📈 {tahmin_tarihi} için tahmini kapanış fiyatı: **${prediction:,.2f}**")

    # Gerçek değer varsa karşılaştır
    row_actual = df[df['Open time'] == pd.to_datetime(tahmin_tarihi)]
    if not row_actual.empty:
        real_price = row_actual['Close'].values[0]
        st.info(f"✅ Gerçek kapanış fiyatı: **${real_price:,.2f}**")
        fark = abs(real_price - prediction)
        st.write(f"📊 Tahmin – Gerçek farkı: **${fark:,.2f}**")
    else:
        st.warning("🔍 Bu tarihe ait gerçek kapanış fiyatı veri setinde bulunamadı.")
