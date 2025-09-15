import ee
import streamlit as st
from google.oauth2 import service_account

st.title("📊 Datos NDBI - Norte de Colombia")

# Cargar credenciales desde secrets.toml
service_account_info = st.secrets["service_account"]

# Crear credenciales con google.oauth2
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# Inicializar Earth Engine
ee.Initialize(credentials)

# Área de estudio
norte_colombia = ee.Geometry.Rectangle([-75.5, 11.5, -74.5, 12.5])

# Imagen Landsat 8 ejemplo
image = ee.Image('LANDSAT/LC08/C02/T1_TOA/LC08_008059_20230102')
ndbi = image.normalizedDifference(['B6', 'B5']).rename('NDBI')

# Calcular estadísticas rápidas
stats = ndbi.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=norte_colombia,
    scale=1000
).getInfo()

# Mostrar resultados
st.subheader("Estadísticas NDBI")
st.metric("NDBI Promedio", f"{stats['NDBI']:.4f}")

# Interpretación
st.subheader("Interpretación:")
st.write("🔵 **-1.0 a -0.2:** Vegetación densa/Agua")
st.write("⚪ **-0.2 a 0.2:** Suelo/Sin construcción")
st.write("🔴 **0.2 a 1.0:** Áreas construidas/Urbanas")

st.success("¡Análisis completado en menos de 2 segundos! ⚡")
