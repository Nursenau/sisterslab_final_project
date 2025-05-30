import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

st.set_page_config(page_title="Recursive Bitcoin Tahmini", layout="centered")
st.title("🔁 Lag-Based ile Bitcoin Tahmini")

# Veriyi yükle
df = pd.read_csv("data/btc_1d_data_2018_to_2025.csv")
df['Open time'] = pd.to_datetime(df['Open time'])

# Model eğitimi için lagged dataset
features = ['Open', 'High', 'Low', 'Volume', 'Number of trades']
df_lagged = df[features].shift(1)
df_lagged['Target_Close'] = df['Close']
df_lagged = df_lagged.dropna()
X = df_lagged[features]
y = df_lagged['Target_Close']
model = LinearRegression()
model.fit(X, y)

# Tahmin başlangıç günü: 2025-05-23
start_date = pd.to_datetime("2025-05-23")
latest_row = df[df['Open time'] == start_date].iloc[0].copy()

# Tahmin yapılacak gün sayısı
n_days = st.slider("Tahmin edilecek gün sayısı", 1, 10, 5)

# Recursive tahmin döngüsü
future_preds = []
dates = pd.date_range(start=start_date + pd.Timedelta(days=1), periods=n_days)

for date in dates:
    X_input = pd.DataFrame([{
        'Open': latest_row['Open'],
        'High': latest_row['High'],
        'Low': latest_row['Low'],
        'Volume': latest_row['Volume'],
        'Number of trades': latest_row['Number of trades']
    }])
    pred = model.predict(X_input)[0]
    future_preds.append({'Tarih': date.date(), 'Tahmin': pred})

    # Tahmin edilen değerlerle yeni gün oluştur
    latest_row['Open'] = pred
    latest_row['High'] = pred * 1.01
    latest_row['Low'] = pred * 0.99
    latest_row['Close'] = pred

# new.csv'den gerçek kapanışları karşılaştır
try:
    df_real = pd.read_csv("data/new.csv")
    df_real['Open time'] = pd.to_datetime(df_real['Open time'])
    for row in future_preds:
        date = pd.to_datetime(row['Tarih'])
        match = df_real[df_real['Open time'] == date]
        if not match.empty:
            real = match['Close'].values[0]
            row['Gerçek'] = real
            row['Fark'] = abs(real - row['Tahmin'])
        else:
            row['Gerçek'] = None
            row['Fark'] = None
except:
    for row in future_preds:
        row['Gerçek'] = None
        row['Fark'] = None

# DataFrame'e çevir
results = pd.DataFrame(future_preds)
st.dataframe(results, use_container_width=True)

# Grafik
if not results.empty:
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(results['Tarih'], results['Tahmin'], label='Tahmin', marker='o')
    if results['Gerçek'].notnull().all():
        ax.plot(results['Tarih'], results['Gerçek'], label='Gerçek', marker='x')
    ax.set_title("Bitcoin Tahmini vs Gerçek Değerler")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Kapanış Fiyatı (USD)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

st.markdown("---")
st.caption("Model yalnızca geçmiş desenlere göre öğrenme yapar. Tahmin edilen günlerin gerçek değerleri new.csv'den alınır (varsa).")
