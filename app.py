import ee
import streamlit as st
import json

# ============================
# Inicializar credenciales GEE
# ============================
service_account = st.secrets["service_account"]

# Autenticación con Google Earth Engine
credentials = ee.ServiceAccountCredentials(
    email=service_account["santiago-630@geomatica-470001.iam.gserviceaccount.com"],
    key_data=service_account["private_key"]
)
ee.Initialize(credentials, project=service_account["geomatica-470001"])


# ============================
# Interfaz Streamlit
# ============================
st.set_page_config(page_title="Análisis NDBI - Colombia", layout="wide")
st.title("📊 Datos NDBI - Norte de Colombia")

# Área de estudio
norte_colombia = ee.Geometry.Rectangle([-75.5, 11.5, -74.5, 12.5])

# Imagen fija (ejemplo Landsat 8 TOA)
image = ee.Image('LANDSAT/LC08/C02/T1_TOA/LC08_008059_20230102')

# Calcular NDBI
ndbi = image.normalizedDifference(['B6', 'B5']).rename('NDBI')

# Reducir región (estadísticas)
stats = ndbi.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=norte_colombia,
    scale=1000
).getInfo()

# Mostrar resultados
st.subheader("📈 Estadísticas NDBI")
st.metric("NDBI Promedio", f"{stats['NDBI']:.4f}")

# Interpretación
st.subheader("📝 Interpretación de valores:")
st.write("🔵 **-1.0 a -0.2:** Vegetación densa / Agua")
st.write("⚪ **-0.2 a 0.2:** Suelo sin construcción")
st.write("🔴 **0.2 a 1.0:** Áreas construidas / Urbanas")

st.success("¡Análisis completado en segundos con Google Earth Engine ⚡!")
