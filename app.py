import streamlit as st
import pandas as pd
from random import random
import joblib
import logging
import os
import pickle
import gzip
import lzma

logging.warning(joblib.__version__)

# load model from pickle file
current_path = os.getcwd()
# simulador_model = os.path.join(current_path, "RF_compressed.joblib")
# model = joblib.load(simulador_model)
# with gzip.open("compressed_data.pkl.gz", "rb") as file:
#     model = pickle.load(file)

with gzip.open("compressed_data.pkl.gz", "rb") as file:
    model = pickle.load(file)

st.write(
    """
    # Panike

    #### Simulador da dimensão dos produtos acabados 🍞
    """
)
st.markdown("""---""")
ordens_sa = pd.read_csv(os.path.join(current_path, "dimensoes.csv"))

option = st.selectbox(
    "Qual a tipologia de pão que gostava de analisar?", list(ordens_sa.order.unique())
)

st.markdown("""---""")
col1, col2 = st.columns(2)
with col1:
    st.write("""**Condições no forno:**""")
    temperatura_pedra = st.slider("Temperatura pedra 1 (ºC): ", 0, 350, 265)
    tempo_de_cozedura = st.slider("Tempo de cozedura (min): ", 0, 60, 11)

with col2:
    st.write("""**Condições na congelação:**""")
    temperatura_congelacao = st.slider("Temperatura na congelação (ºC): ", -50, 25, -15)
    tempo_arrefecimento = st.slider("Tempo de arrefecimento (min): ", 0, 80, 50)
    tempo_congelacao = st.slider("Tempo de congelação (min): ", 0, 80, 45)


button_click = st.button("Simular", type="primary")
if button_click:
    print(
        temperatura_pedra,
        tempo_de_cozedura,
        temperatura_congelacao,
        tempo_arrefecimento,
        tempo_congelacao,
    )
    y_predict = model.predict(
        [
            [
                temperatura_pedra,
                tempo_de_cozedura,
                temperatura_congelacao,
                tempo_arrefecimento,
                tempo_congelacao,
            ]
        ]
    )
    col3, col4, col5 = st.columns(3)

    comprimento = ordens_sa[ordens_sa.order == option]["c_max"] - y_predict[0][0]
    largura = ordens_sa[ordens_sa.order == option]["l_max"] - y_predict[0][2]
    altura = ordens_sa[ordens_sa.order == option]["a_max"] - y_predict[0][4]
    print(y_predict)
    with col3:
        st.header("Comprimento")
        st.subheader(str(round(comprimento.values[0])) + " (mm)")
        st.write("Max: ", ordens_sa[ordens_sa.order == option]["c_max"].values[0])
        st.write("Min: ", ordens_sa[ordens_sa.order == option]["c_min"].values[0])

    with col4:
        st.header("Largura")
        st.subheader(str(round(largura.values[0])) + " (mm)")
        st.write("Max: ", ordens_sa[ordens_sa.order == option]["l_max"].values[0])
        st.write("Min: ", ordens_sa[ordens_sa.order == option]["l_min"].values[0])

    with col5:
        st.header("Altura")
        st.subheader(str(round(altura.values[0])) + " (mm)")
        st.write("Max: ", ordens_sa[ordens_sa.order == option]["a_max"].values[0])
        st.write("Min: ", ordens_sa[ordens_sa.order == option]["a_min"].values[0])
