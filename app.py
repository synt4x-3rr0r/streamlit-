import ee
import json
from google.oauth2 import service_account
import streamlit as st

# Leer credenciales
credentials_dict = st.secrets["service_account"]
credentials = service_account.Credentials.from_service_account_info(
    credentials_dict,
    scopes=["https://www.googleapis.com/auth/earthengine"]
)

# Inicializar
ee.Initialize(credentials)

# Probar con un dataset público
image = ee.Image("LANDSAT/LC08/C01/T1/LC08_044034_20140318")
info = image.getInfo()

print("✅ Autenticación correcta, se pudo acceder a Earth Engine")
print("Nombre:", info["id"])
