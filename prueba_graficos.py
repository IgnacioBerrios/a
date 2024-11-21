# -*- coding: utf-8 -*-
"""prueba_graficos.py

Generación de gráficos interactivos con Streamlit sin seaborn.
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Cargar el archivo CSV
@st.cache_data
def load_data():
    file_path = '/content/spotify_songs_dataset.csv'
    data = pd.read_csv(file_path, sep=';')
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')  # Convertir fechas
    return data

# Cargar datos
pf = load_data()

# Título de la aplicación
st.title("Gráfico de Dispersión por Género")
st.markdown(
    "Selecciona un género para visualizar cómo se distribuyen las reproducciones según la fecha de publicación."
)

# Lista de géneros únicos para el filtro
genres = pf['genre'].dropna().unique()
selected_genre = st.selectbox("Selecciona un género:", options=genres)

# Filtrar datos según el género seleccionado
filtered_data = pf[pf['genre'] == selected_genre]

# Crear el gráfico de dispersión usando solo matplotlib
plt.figure(figsize=(10, 6))
plt.scatter(
    filtered_data['release_date'], 
    filtered_data['stream'], 
    alpha=0.7, 
    color='blue'
)
plt.title(f"Fecha de Publicación vs Reproducciones ({selected_genre})", fontsize=16)
plt.xlabel("Fecha de Publicación", fontsize=12)
plt.ylabel("Reproducciones", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()  # Ajusta la visualización para evitar superposiciones
st.pyplot(plt)
