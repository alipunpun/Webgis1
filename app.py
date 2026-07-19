import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# 1. Konfigurasi Halaman & Konteks Teks (Tugas 3)
st.set_page_config(page_title="Peta Taman Bermain Banten", layout="wide")
st.title("Peta Aksesibilitas Taman Bermain & Kerentanan Kesehatan Anak Banten")
st.markdown("""
**Ringkasan Eksekutif:** Ditemukan sejumlah kecamatan di Banten yang merupakan blank spot taman bermain dengan populasi balita rentan stunting tinggi. Peta ini memvisualisasikan zonasi aman dan prioritas pembangunan fasilitas anak.
""")

# 2. Membaca Data GeoJSON
# Pastikan nama file sesuai dengan yang Anda ekspor dari QGIS
gdf_batas = gpd.read_file('batas_kesehatan.geojson')
gdf_taman = gpd.read_file('taman_bermain.geojson')
gdf_buffer = gpd.read_file('buffer.geojson')
gdf_blank = gpd.read_file('blank_spot.geojson')

# 3. Membuat Peta Dasar (Berpusat di Banten)
m = folium.Map(location=[-6.3117, 106.1116], zoom_start=10)

# 4. Menambahkan Layer Batas Kesehatan (Gradasi Warna/Choropleth)
# Ganti 'Persentase_Stunting' dan 'Kecamatan' sesuai nama kolom Anda di QGIS
folium.Choropleth(
    geo_data=gdf_batas,
    name="Kerentanan Stunting",
    data=gdf_batas,
    # Ubah baris ini sesuai dengan nama kolom yang muncul di layar:
    columns=['NAME_3', 'Balita_Stunting'], 
    
    # key_on juga HARUS menyesuaikan nama kolom wilayah:
    key_on='feature.properties.NAME_3', 
    
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Jumlah Stunting'
).add_to(m)

# Menambahkan Pop-up pada layer batas
folium.GeoJson(
    gdf_batas,
    name="Info Wilayah",
    style_function=lambda x: {'fillColor': 'transparent', 'color': 'black', 'weight': 1},
    tooltip=folium.GeoJsonTooltip(fields=['Kecamatan', 'Total_Balita', 'Persentase_Stunting'], 
                                  aliases=['Kecamatan:', 'Total Balita:', 'Stunting (%):'])
).add_to(m)

# 5. Menambahkan Layer Blank Spot (Merah)
folium.GeoJson(
    gdf_blank,
    name="Blank Spot Taman Bermain",
    style_function=lambda x: {'fillColor': 'red', 'color': 'red', 'weight': 2, 'fillOpacity': 0.5}
).add_to(m)

# 6. Menambahkan Layer Buffer (Hijau Transparan)
folium.GeoJson(
    gdf_buffer,
    name="Zona Aman Berjalan Kaki (500m)",
    style_function=lambda x: {'fillColor': 'green', 'color': 'green', 'weight': 1, 'fillOpacity': 0.3}
).add_to(m)

# 7. Menambahkan Layer Titik Taman Bermain (Hijau)
# Ganti 'Nama_Taman' sesuai nama kolom atribut Anda
folium.GeoJson(
    gdf_taman,
    name="Taman Bermain Anak",
    marker=folium.CircleMarker(radius=5, fill_color='green', color='black', fill_opacity=1),
    tooltip=folium.GeoJsonTooltip(fields=['Nama_Taman'], aliases=['Nama Taman:'])
).add_to(m)

# 8. Mengaktifkan Layer Control (Tugas 2)
folium.LayerControl().add_to(m)

# 9. Menampilkan Peta di Web Streamlit
st_folium(m, width=1200, height=600)
