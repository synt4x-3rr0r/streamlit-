import ee
import streamlit as st
import geemap.foliumap as geemap

# ------------------------------
# 1. Autenticación con Secrets
# ------------------------------
service_account = st.secrets["service_account"]

credentials = ee.ServiceAccountCredentials(
    service_account["client_email"],
    key_data=service_account["private_key"]
)
ee.Initialize(credentials)

# ------------------------------
# 2. Configuración de la app
# ------------------------------
st.set_page_config(page_title="NDBI con GEE", layout="wide")
st.title("📊 Análisis de NDBI con Google Earth Engine")

# ------------------------------
# 3. Parámetros iniciales
# ------------------------------
roi = ee.Geometry.Polygon(
    [[[-75.6, 6.2], [-75.6, 6.4], [-75.4, 6.4], [-75.4, 6.2]]]
)  # Medellín de ejemplo

collection = ee.ImageCollection("COPERNICUS/S2_SR") \
    .filterBounds(roi) \
    .filterDate("2024-01-01", "2024-12-31") \
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))

image = collection.median()

# ------------------------------
# 4. Cálculo del NDBI
# ------------------------------
ndbi = image.normalizedDifference(["B11", "B8"]).rename("NDBI")

# Estadísticas
stats = ndbi.reduceRegion(
    reducer=ee.Reducer.mean().combine(
        reducer2=ee.Reducer.minMax(), sharedInputs=True
    ),
    geometry=roi,
    scale=30,
    maxPixels=1e9
)

# ------------------------------
# 5. Mostrar resultados
# ------------------------------
st.subheader("📈 Estadísticas del NDBI")
st.json(stats.getInfo())

# ------------------------------
# 6. Mapa interactivo
# ------------------------------
m = geemap.Map(center=[6.3, -75.5], zoom=11)
m.addLayer(ndbi, {"min": -1, "max": 1, "palette": ["blue", "white", "green"]}, "NDBI")
m.addLayer(roi, {}, "Región de interés")
m.to_streamlit(width=1000, height=600)
