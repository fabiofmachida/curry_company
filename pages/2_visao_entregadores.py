# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# bibliotecas necessarias
import pandas as pd
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Empregadores', page_icon='🚚', layout='wide')

#===================================================================================================
# Funções
#===================================================================================================
def top_delivers(df1, top_asc):
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
           .groupby(['City', 'Delivery_person_ID'])
           .mean().sort_values(['City', 'Time_taken(min)'], ascending=top_asc)
           .reset_index())
    df_aux1 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux3 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    df3 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
    return df3

def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o dataframe
    
        Tipos de limpeza
        1. Remioção dos dados NaN
        2. Mudança do tipo da columa de dados
        3. Remoção dos espaços das variaveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
        
        Input: dataframe
        Output: dataframe
    
    """
    # convertendo a coluna age de texto para numero
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN ' 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = df1['Road_traffic_density'] != 'NaN ' 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = df1['City'] != 'NaN ' 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = df1['Festival'] != 'NaN ' 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    #df1.shape
    
    # convertendo a coluna Rating de texto para numero decimal
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    
    # convertendo a coluna Order Date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    # converter multiple_deliveries de texto para numero inteiro
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    #removendo os espaços dentro de strings/textos/objetos
    #df1 = df1.reset_index(drop=True)
    #for i in range(41419):
      #df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()
      #df1.loc[i, 'Delivery_person_ID'] = df1.loc[i, 'Delivery_person_ID'].strip()
      #df1.loc[i, 'Type_of_order'] = df1.loc[i, 'Type_of_order'].strip()
      #df1.loc[i, 'Type_of_vehicle'] = df1.loc[i, 'Type_of_vehicle'].strip()
      #df1.loc[i, 'Festival'] = df1.loc[i, 'Festival'].strip()
      #df1.loc[i, 'City'] = df1.loc[i, 'City'].strip()
      #df1.loc[i, 'Road_traffic_density'] = df1.loc[i, 'Road_traffic_density'].strip()
    
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    #df1.loc[:, 'Time_taken(min)'] = df1.loc[0, 'Time_taken(min)'].split(' ')[1]
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1

# Importar o dataset
df = pd.read_csv('datasets/train.csv')

# Limpando dados
df1 = clean_code(df)

#=====================================================================================
#BARRA LATERAL
#=====================================================================================

#image_path = '/Users/fabiomachida/Comunidade DS/repos/logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.header('Marketplace - Visão Entregadores')

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Deliviery in Town')
st.sidebar.markdown("""----""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime(2022, 4, 13),
    min_value=pd.datetime(2022, 2, 11),
    max_value=pd.datetime(2022, 4, 6),
    format='DD-MM-YYYY'
   )

st.sidebar.markdown("""----""")

# Opção de transito
traffic_options = st.sidebar.multiselect(
    'Quais as condições do transito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""----""")

# Opção de clima
weather_options = st.sidebar.multiselect(
    'Quais as condições Climaticas',
    ['Cloudy', 'Fog', 'Sandstorms', 'Stormy', 'Sunny', 'Windy'],
    default=['Cloudy', 'Fog', 'Sandstorms', 'Stormy', 'Sunny', 'Windy'])

st.sidebar.markdown("""----""")

st.sidebar.markdown('### Powered by Comunidade DS')

#filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)

#======================================================================================
#LAYOUT STREAMLIT
#======================================================================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '', ''])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            
            # Maior de idade dos entregadores
            #st.subheader('Maior de idade')
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior de idade', maior_idade)
        
        with col2:
            # Menor de idade dos entregadores
            #st.subheader('Menor de idade')
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Maior de idade', menor_idade)
            
        with col3:
            # Melhor condição de veículos
            #st.subheader('Melhor condição de veículos')
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_condicao)
            
        with col4:
            # Pior condição de veículos
            #st.subheader('Pior condição de veículos')
            pior_condicao=df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição', pior_condicao)
            
    with st.container():
        st.markdown("""____""")
        st.title('Avaliações')
        
        col1, col2 = st.columns(2)
        with col1:
            # Avaliação médias por entregador
            st.markdown('##### Avaliação médias por entregador')
            df_avg_ratings_per_deliviery = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                        .groupby('Delivery_person_ID')
                                        .mean()
                                        .reset_index())
            st.dataframe(df_avg_ratings_per_deliviery)
            
        with col2:
            # Avalição média por transito
            st.markdown('##### Avalição média por transito')
            df_avg_per_traffic = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                  .groupby('Road_traffic_density')
                                  .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            df_avg_per_traffic.columns = ['Delivery_mean', 'Delivery_std']
            df_avg_per_traffic.reset_index()
            st.dataframe(df_avg_per_traffic)
            
            # Avaliação média por clima
            st.markdown('##### Avaliação média por clima')
            df_avg_per_weather = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                       .groupby('Weatherconditions')
                       .agg({'Delivery_person_Ratings': ['mean', 'std']}))
            df_avg_per_weather.columns = ['Delivery_mean', 'Delivery_std']
            df_avg_per_weather.reset_index()
            st.dataframe(df_avg_per_weather)
            
    with st.container():
        st.markdown("""___""")
        st.title('Velocidade de Entrega')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('##### Top Entregadores mais rápidos')
            df3 = top_delivers(df1, top_asc=True)
            st.dataframe(df3)
        
        with col2:
            st.markdown('##### Top Entregadores mais lentos')
            df3 = top_delivers(df1, top_asc=False)
            st.dataframe(df3)
            
            
               
            