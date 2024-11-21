import subprocess
import sys

# Verificar e instalar las dependencias
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Asegurar las bibliotecas necesarias
try:
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import streamlit as st
except ImportError as e:
    missing_package = str(e).split()[-1]
    install(missing_package)
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import streamlit as st

# Configurar el estilo de gráficos
sns.set(style="whitegrid")

# Cargar el archivo CSV
@st.cache
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

# Crear el gráfico de dispersión
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=filtered_data,
    x='release_date',
    y='stream',
    alpha=0.7,
    color='blue'
)
plt.title(f"Fecha de Publicación vs Reproducciones ({selected_genre})", fontsize=16)
plt.xlabel("Fecha de Publicación", fontsize=12)
plt.ylabel("Reproducciones", fontsize=12)
plt.xticks(rotation=45)
st.pyplot(plt)
