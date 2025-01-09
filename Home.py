import streamlit as st
from PIL import Image

#seting the emoticon and the title of the page
st.set_page_config( page_title = 'Home', page_icon ='🏠', layout = 'wide')
st.markdown("<h1 style='text-align: center;'>HOME 🏠</h1>", unsafe_allow_html=True)


#########  BARRA LATERAL  ########## 

#st.sidebar.divider()

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        st.image('logo1.jpeg', width = 150)
    with col2:
        st.image('fomeZero.png', width = 137)
    st.sidebar.markdown( """---""" )


st.markdown (
    """
    Bem vindo(a) ao Fome Zero!
    
    ### Como utilizar esse Growth Dashboard?
    - #### Visão Geral:
        - Quantidade de países registrados na base de dados;
        - Total de restaurantes registrados na base de dados;
        - Total de avaliações registradas na base de dados;
        - Tipos de Culinária;
        - Mapa; 
        - Filtro de Países.
        
    - #### Visão Países:
        - Quantidade de restaurantes cadastrados por país;
        - Quantidade de cidades registradas por país;
        - Média de Avaliações por país;
        - Média de preço de um prato para 2 por país;
        - Filtro de Países.
        
    - #### Visão Cidades:
        - Top 10 cidades com mais restaurantes;
        - Cidades com restaurantes com média acima de 4,0;
        - Cidades com restaurantes com media abaixo de 4,0;
        - Top 10 cidades com restaurantes com tipos culinários distintos;
        - Filtro de Países.
        
    - #### Visão Culinária:
        - Top 10 restaurantes;
        - Top 10 melhores culinárias;
        - Top 10 piores culinárias;
        - Top 10 cidades com restaurantes com tipos culinários distintos;
        - Filtr de culinárias;
        - Filtro de Países.
        
    
    """
)