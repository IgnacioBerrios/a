import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

@st.cache_data
def load_data():
    file_path = 'spotify_songs_dataset.csv'
    data = pd.read_csv(file_path, sep=';')
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce') 
    return data



cambia el matplotlib por otra libreria que cumpla la misma funcion

pf = load_data()
pf = pf.dropna(subset=['release_date']) 
pf['year'] = pf['release_date'].dt.year  

st.title("Gráfico de Dispersión por Género")
st.markdown(
    "Selecciona un género para visualizar cómo se distribuyen las reproducciones según la fecha de publicación."
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

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(
    filtered_data['release_date'],
    filtered_data['stream'],
    alpha=0.7,
    color='blue'
)
ax.set_title(
    f"Fecha de Publicación vs Reproducciones ({selected_genre}, {rango_años[0]}-{rango_años[1]})",
    fontsize=16
)
ax.set_xlabel("Fecha de Publicación", fontsize=12)
ax.set_ylabel("Reproducciones", fontsize=12)
ax.grid(True)
plt.xticks(rotation=45)

st.pyplot(fig)
