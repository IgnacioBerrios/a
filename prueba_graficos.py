import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_data
def datos_cargados():
    ruta = 'spotify_songs_dataset.csv'
    pf = pd.read_csv(ruta, sep=';')
    pf['release_date'] = pd.to_datetime(pf['release_date'], errors='coerce')  # Convertir a datetime
    return pf

# Cargar datos
pf = datos_cargados()
pf = pf.dropna(subset=['release_date'])  # Eliminar filas con fechas nulas
pf['year'] = pf['release_date'].dt.year  # Extraer año de la fecha

# Título y descripción
st.title("Reproducciones según fecha de publicación")
st.markdown(
    "Selecciona un género para observar cómo se distribuyen las reproducciones según la fecha de publicación."
)

# Selección de género
genres = sorted(pf['genre'].dropna().unique())
selected_genre = st.selectbox("Selecciona un género:", options=genres)

# Filtrar por género
filtered_pf = pf[pf['genre'] == selected_genre]

# Verificar si hay datos para el género seleccionado
if filtered_pf.empty:
    st.warning(f"No hay datos disponibles para el género '{selected_genre}'.")
    st.stop()

# Selección del rango de años
min_year = int(filtered_pf['year'].min())
max_year = int(filtered_pf['year'].max())
rango_años = st.slider(
    'Selecciona el rango de años:',
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filtrar por rango de años
filtered_pf = filtered_pf[
    (filtered_pf['year'] >= rango_años[0]) & (filtered_pf['year'] <= rango_años[1])
]

# Verificar si hay datos después del filtro por años
if filtered_pf.empty:
    st.warning(f"No hay datos disponibles para el rango de años {rango_años[0]}-{rango_años[1]}.")
    st.stop()

# Mapa de colores
color_map = {
    "R&B": "red",
    "Electronic": "yellow",
    "Pop": "blue",
    "Folk": "green",
    "Hip-Hop": "purple",
    "Jazz": "orange",
    "Classical": "brown",
    "Country": "skyblue",
    "Reggae": "white",
}

# Gráfico
fig = px.scatter(
    filtered_pf,
    x='release_date',
    y='stream',
    color='genre',  # Usar la columna género para asignar color
    color_discrete_map=color_map,  # Aplicar colores personalizados si aplica
    title=f"Fecha de Publicación vs Reproducciones ({selected_genre}, {rango_años[0]}-{rango_años[1]})",
    labels={"release_date": "Fecha de Publicación", "stream": "Reproducciones", "genre": "Género"},
    template="plotly_white",
    opacity=0.7
)

# Personalizar diseño
fig.update_layout(
    xaxis=dict(title="Fecha de Publicación"),
    yaxis=dict(title="Reproducciones"),
    title_font_size=16,
)

# Mostrar gráfico
st.plotly_chart(fig)
