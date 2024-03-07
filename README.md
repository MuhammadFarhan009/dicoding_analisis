# dicoding_analisis

**Tugas Akhir Proyek Analisis Data**

## Setup environment

```
conda create --name python=Python 3.9.18
conda activate --name
pip install pandas matplotlib seaborn plotly streamlit
```

## Run steamlit app

```
streamlit run dashboard.py
```

## Dataset overview

### Introduction

Dataset ini merupakan dataset tentang polusi udara di beberapa statiun

## Data Structure

-`No`: Identifikasi numerik untuk setiap baris.
-`tahun, bulan, hari, jam`: Indikator tanggal dan waktu.
-`PM2.5, PM10, SO2, NO2, CO, O3`: Konsentrasi berbagai polutan udara.
-`TEMP`: Suhu dalam derajat Celsius.
-`PRES`: Tekanan atmosfer dalam hPa.
-`DEWP`: Suhu titik rosak dalam derajat Celsius.
-`RAIN`: Jumlah curah hujan dalam mm.
-`wd`: Arah angin.
-`WSPM`: Kecepatan angin dalam m/s.
-`station`: Nama stasiun pemantauan.