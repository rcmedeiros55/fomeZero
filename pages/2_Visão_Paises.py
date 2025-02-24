#######      BIBLIOTECAS     ##########

import pandas as pd
import inflection 
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import folium_static
from PIL import Image #import PIL.Image as imgpil

########      FUNCOES     ##########

def country_name(country_id):
    COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
    }
    return COUNTRIES[country_id]
    

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
        

def color_name(color_code):
    COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }
    return COLORS[color_code]
    

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df
    

def remove_duplicatas(dataframe):
    duplicado = df1.duplicated()
    linhas_nao_duplicadas = duplicado == False
    dataframe = dataframe.loc [ linhas_nao_duplicadas, :]
    return dataframe.reset_index(drop = True) ## Drop = True server para derrubar a coluna com o índice antigo
    


def convert_to_dollar(valor, moeda):
    moedas_em_dolar = {
   
    'Botswana Pula(P)'       : 0.084,
    'Brazilian Real(R$)'     : 0.35,
    'Dollar($)'              : 1.00,
    'Emirati Diram(AED)'     : 0.30,
    'Indian Rupees(Rs.)'     : 0.024,
    'Indonesian Rupiah(IDR)' : 0.000075,
    'NewZealand($)'          : 0.68098,
    'Pounds(£)'              : 1.357523,
    'Qatari Rial(QR)'        : 0.35,
    'Rand(R)'                : 0.085,
    'Sri Lankan Rupee(LKR)'  : 0.0075,
    'Turkish Lira(TL)'       : 0.085
    }
    return valor * moedas_em_dolar[moeda]


########      CARREGANDO DADOS     ##########


df = pd.read_csv('zomato.csv')
df1 = df.copy()

########      TRATANDO DADOS     ##########

#RENOMEANDO COLUNAS DO DATA FRAME
df1 = rename_columns(df1) 

#RENOMEANDO COLUNAS COM APENAS UM VALOR
df1 = df1.drop(['switch_to_order_menu'], axis = 1) 

#DELETANDO VALORES
df1 = df1.dropna(subset=['cuisines']) ##deletando valores nan

#REMOVENDO VALORES DUPLICADOS
df1 = remove_duplicatas(df1)

#CATEGORIZANDO A COLUNA cuisiners PELO PRIMENTO ARGUMENTO DA STRING (italian, japanese, brazilian -- > italian)
df1['cuisines'] = df1.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else x)

#CRIANDO A COLUNA 'country_names'
df1['country_name'] = df1['country_code'].apply(country_name)

#CONVERTENDO TODOS OS VALORES PARA DOLAR
df1['average_cost_for_two(USD)'] = df1.apply(lambda row: convert_to_dollar(row['average_cost_for_two'], row['currency']), axis=1) 

#CRIANDO A COLUNA 'color_name'
df1['color_name'] = df1['rating_color'].apply(color_name)


#DEFININDO O  EMOTICON E O TITULO DA PAGINA
st.set_page_config( page_title = 'Visão Países', page_icon ='🌎', layout = 'wide')

st.markdown("<h1 style='text-align: center;'>Visão Países 🌎</h1>", unsafe_allow_html=True)


########      BARRA LATERAL     ##########

st.sidebar.markdown( """---""" )
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        st.image('logo1.jpeg', width = 150)
    with col2:
        st.image('fomeZero.png', width = 137)
    st.sidebar.markdown( """---""" )

    country = st.multiselect(
        'Selecione os Países',
        sorted(['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey']),
        default = ['Australia', 'Brazil', 'Canada', 'England', 'Qatar', 'South Africa']
        )

########      LIGANDO OS FILTROS     ##########

linhas_selecionadas = df1['country_name'].isin(country)
df1 = df1.loc[linhas_selecionadas, :]


st.tabs(['Países'])

with st.container():
    
    st.markdown("<h1 style='text-align: center;'>Restaurantes Cadastrados Por País</h1>", unsafe_allow_html=True)
    df_aux = df1[['restaurant_id', 'country_name']].groupby('country_name').count().reset_index()
    fig = px.bar(df_aux, x = 'country_name', y = 'restaurant_id', text = 'restaurant_id' )
    st.plotly_chart(fig)
    
with st.container():
    
    st.markdown("<h1 style='text-align: center;'>Quantidade de Cidades Registradas Por País</h1>", unsafe_allow_html=True)
    df_aux = df1[['city', 'country_name']].groupby(['country_name']).agg({'city' : ['nunique']}).reset_index()
    df_aux.columns = ['country_name', 'qtd_cidades']
    fig = px.bar(df_aux, x = 'country_name', y = 'qtd_cidades', text = 'qtd_cidades' )
    st.plotly_chart(fig)
    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
       
        st.markdown("<h1 style='text-align: center;'>Média de Aval. Por País</h1>", unsafe_allow_html=True)
        df_aux = round( df1[['votes', 'country_name']].groupby('country_name').agg({'votes': ['mean']}).reset_index(), 2)
        df_aux.columns = ['country_name', 'avg_vote']
        df_aux = df_aux.sort_values('avg_vote', ascending = False)
        fig = px.bar(df_aux, x = 'country_name', y = 'avg_vote' , text = 'avg_vote')
        st.plotly_chart(fig)
        
    with col2:
        st.markdown("<h1 style='text-align: center;'>Média de Preço Prato Para 2</h1>", unsafe_allow_html=True)
        df1 = df1.loc [df1['average_cost_for_two(USD)'] != 25000017.0, :].reset_index(drop = True)
        df_aux = round (df1[['country_name','average_cost_for_two(USD)']].groupby('country_name').mean().sort_values('average_cost_for_two(USD)', ascending = False).reset_index(), 2 )
        df_aux.columns = ['country_name', 'avg_cost_for_two(USD)']
        fig = px.bar(df_aux, x = 'country_name', y = 'avg_cost_for_two(USD)', text = 'avg_cost_for_two(USD)')
        st.plotly_chart(fig)

            


    







