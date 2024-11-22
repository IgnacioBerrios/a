import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_data
def datos_cargados():
    ruta = 'spotify_songs_dataset.csv'
    data = pd.read_csv(ruta, sep=';')
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce') 
    return data

pf = datos_cargados()
pf = pf.dropna(subset=['release_date']) 
pf['year'] = pf['release_date'].dt.year  

st.title("Reproducciones según fecha de publicación")
st.markdown(
    "Selecciona un género para observar cómo se distribuyen las reproducciones según la fecha de publicación."
)

genres = pf['genre'].dropna().unique()
selected_genre = st.selectbox("Selecciona un género:", options=genres)

filtered_data = pf[pf['genre'] == selected_genre]

min_year = int(filtered_data['year'].min())
max_year = int(filtered_data['year'].max())
rango_años = st.slider('Selecciona el rango de años:', min_year, max_year, (min_year, max_year))

filtered_data = filtered_data[
    (filtered_data['year'] >= rango_años[0]) & (filtered_data['year'] <= rango_años[1])
]

color_map = { 
    "R&B": "red",
    "Electronic": "yellow",
    "Pop": "blue",
    "Folk": "green",
    "Hip-Hop": "purple",
    "Jazz": "orange",
    "Classical":"brown",
    "Country":"skyblue",
    "Reggae":"white",
}    

fig = px.scatter(
    filtered_data,
    x='release_date',
    y='stream',
    color='genre',
    color_discrete_map=color_map,
    title=f"Fecha de Publicación vs Reproducciones ({selected_genre}, {rango_años[0]}-{rango_años[1]})",
    labels={"release_date": "Fecha de Publicación", "stream": "Reproducciones", "genre": "Genero"},
    template="plotly_white",
    opacity=0.7
)

fig.update_layout(
    xaxis=dict(title="Fecha de Publicación"),
    yaxis=dict(title="Reproducciones"),
    title_font_size=16,
)

st.plotly_chart(fig)
