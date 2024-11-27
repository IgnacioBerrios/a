import pandas as pd
import plotly.express as px
import streamlit as st

# Función para cargar datos, con manejo de errores y cacheo
@st.cache_data
def datos_cargados():
    ruta = 'spotify_songs_dataset.csv'  # Cambia esto a la ruta real del archivo
    pf = pd.read_csv(ruta, sep=';')
    
    # Convertir release_date a datetime, ignorando errores
    pf['release_date'] = pd.to_datetime(pf['release_date'], errors='coerce') 
    
    # Filtrar filas donde release_date no sea válida
    pf = pf.dropna(subset=['release_date'])
    
    # Agregar columna de año
    pf['year'] = pf['release_date'].dt.year
    return pf

# Carga inicial del dataset
pf = datos_cargados()

# Verificar que los datos están cargados correctamente
if pf.empty:
    st.error("El dataset está vacío o no contiene fechas válidas en la columna 'release_date'.")
else:
    # Título y descripción
    st.title("Reproducciones según fecha de publicación")
    st.markdown(
        "Selecciona un género para observar cómo se distribuyen las reproducciones según la fecha de publicación."
    )

    # Dropdown para seleccionar géneros
    genres = pf['genre'].dropna().unique()  # Obtener géneros únicos
    selected_genre = st.selectbox("Selecciona un género:", options=genres)

    # Filtrar datos por género seleccionado
    filtered_pf = pf[pf['genre'] == selected_genre]

    # Rango de años interactivo
    if not filtered_pf.empty:
        min_year = int(filtered_pf['year'].min())
        max_year = int(filtered_pf['year'].max())
        rango_años = st.slider('Selecciona el rango de años:', min_year, max_year, (min_year, max_year))

        # Filtrar datos por rango de años
        filtered_pf = filtered_pf[
            (filtered_pf['year'] >= rango_años[0]) & (filtered_pf['year'] <= rango_años[1])
        ]

        # Definir mapa de colores para los géneros
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

        # Crear gráfico de dispersión
        fig = px.scatter(
            filtered_pf,
            x='release_date',
            y='stream',
            color='genre',
            color_discrete_map=color_map,
            title=f"Fecha de Publicación vs Reproducciones ({selected_genre}, {rango_años[0]}-{rango_años[1]})",
            labels={"release_date": "Fecha de Publicación", "stream": "Reproducciones", "genre": "Género"},
            template="plotly_white",
            opacity=0.7
        )

        # Personalización del diseño del gráfico
        fig.update_layout(
            xaxis=dict(title="Fecha de Publicación"),
            yaxis=dict(title="Reproducciones"),
            title_font_size=16,
        )

        # Mostrar el gráfico
        st.plotly_chart(fig)
    else:
        st.warning("No hay datos disponibles para el género seleccionado.")
