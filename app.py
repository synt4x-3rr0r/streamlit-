import streamlit as st
import ee
import geemap.foliumap as geemap

# ============================
# Configuración de la página
# ============================
st.set_page_config(page_title="📊 Datos NDBI - Norte de Colombia", layout="wide")
st.title("📊 Datos NDBI - Norte de Colombia")

# ============================
# Autenticación con Google Earth Engine
# ============================
service_account = st.secrets["service_account"]["client_email"]
credentials = ee.ServiceAccountCredentials(service_account, st.secrets["service_account"]["private_key"])
ee.Initialize(credentials, project=st.secrets["service_account"]["project_id"])

# ============================
# Definir región de interés
# ============================
norte_colombia = ee.Geometry.Rectangle([-75, 11, -72, 13])

# ============================
# Cargar colección Landsat 8
# ============================
collection = (
    ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
    .filterBounds(norte_colombia)
    .filterDate("2020-01-01", "2020-12-31")
    .median()
)

# ============================
# Calcular NDBI
# ============================
ndbi = collection.normalizedDifference(["B6", "B5"]).rename("NDBI")

# ============================
# Reducir región para obtener promedio
# ============================
mean_ndbi = ndbi.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=norte_colombia,
    scale=1000
).get("NDBI")

mean_ndbi_value = mean_ndbi.getInfo()

# ============================
# Mostrar métrica
# ============================
st.metric("NDBI Promedio (2020)", f"{mean_ndbi_value:.4f}")

# ============================
# Visualizar en mapa
# ============================
Map = geemap.Map(center=[12, -74], zoom=7)
Map.addLayer(ndbi, {"min": -1, "max": 1, "palette": ["blue", "white", "green"]}, "NDBI")
Map.to_streamlit(height=600)
