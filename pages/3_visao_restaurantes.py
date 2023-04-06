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
import numpy as np

st.set_page_config(page_title='Visão Restaurantes', page_icon='🍽', layout='wide')

#===================================================================================================
# Funções
#===================================================================================================
def avg_std_time_on_traffic(df1):
    df_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Time_taken(min)']]
              .groupby(['City', 'Road_traffic_density'])
              .agg( {'Time_taken(min)': ['mean', 'std']} ))
    
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time',
                color='std_time', color_continuous_scale='RdBu',
                color_continuous_midpoint=np.average(df_aux['std_time']))
    fig.update_layout(width=400, height=400 )
    return fig

def avg_time_delivery_grafh(df1):
    df_aux = (df1.loc[:, ['City', 'Time_taken(min)']]
              .groupby('City')
              .agg({'Time_taken(min)': ['mean', 'std']}))
                    
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control',
                         x=df_aux['City'],
                         y=df_aux['avg_time'],
                         error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group',width=350, height=350 )
    return fig

def avg_std_time_delivery(df1, festival, op):
    """
        Esta função calcula o tempo medio e o desvio padaro de tempo de entrega.
        Parametros:
            Input:
                - df: Dataframe com os dados necessários para o cálculo
                - op: Tipo de operação que precisa ser calculado
                    'avg_time': Calcula o tempo médio
                    'std_time': Calcula o desvio padrão do tempo
                - festival: Filtro de pesquisa 'Yes', ou 'No'
            Output:
                - df: Dataframe com 2 colunas e 1 linha
        
    """
    df_aux = df1.loc[:, ['Festival', 'Time_taken(min)']].groupby(['Festival']).agg( {'Time_taken(min)': ['mean', 'std']} )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == 'Yes', op])
    return df_aux

def distance(df1, fig):
    if fig == False:
        cols = ['Restaurant_latitude','Restaurant_longitude', 'Delivery_location_latitude',	'Delivery_location_longitude']
        df1['distance'] = (df1.loc[:, cols].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                      (x['Delivery_location_latitude'],x['Delivery_location_longitude'])), axis=1))
        
        avg_distance = np.round(df1['distance'].mean(), 2)
        return avg_distance
    else:
        df1['distance'] = (df1.loc[:, ['Restaurant_latitude',	
                              'Restaurant_longitude', 
                              'Delivery_location_latitude',	
                              'Delivery_location_longitude']].apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1))

        avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0])])
        fig.update_layout(width=400, height=400 )
        return fig

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
# BARRA LATERAL
#=====================================================================================

#image_path = '/Users/fabiomachida/Comunidade DS/repos/logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.title('Marketplace - Visão Resturantes')

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

with st.container():
    with st.container():
        st.header('Overall Metrics')
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Entregadores únicos', delivery_unique)
            
        with col2:
            avg_distance = distance(df1, fig=False)
            col2.metric('A distância média das entrega', avg_distance)   
            
        with col3:
            df_aux = avg_std_time_delivery(df1, festival='Yes', op='avg_time')
            col3.metric('TME com Festivais.', df_aux)
                  
        with col4:
            df_aux = avg_std_time_delivery(df1, festival='Yes', op='std_time')
            col4.metric('STD entrega c/ Festivais.', df_aux)
            
        with col5:
            df_aux = avg_std_time_delivery(df1, festival='No', op='avg_time')
            col5.metric('TME sem Festivais.', df_aux)
                 
        with col6:
            df_aux = avg_std_time_delivery(df1, festival='No', op='std_time')
            col6.metric('STD entrega s/ Festivais.', df_aux)
      
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('### Tempo Médio de entrega por cidade')
            fig = avg_time_delivery_grafh(df1)
            st.plotly_chart(fig)       
        
        with col2:
            st.markdown('### Distribução da Distancia')
            df_aux = (df1.loc[:, ['City', 'Type_of_order', 'Time_taken(min)']]
                      .groupby(['City', 'Type_of_order'])
                      .agg( {'Time_taken(min)': ['mean', 'std']} ))
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            st.dataframe(df_aux)
            
    with st.container():
        st.header('Distribução de tempo')
        col1, col2 = st.columns(2)
        
        with col1:
            fig = distance(df1, fig=True)
            st.plotly_chart(fig)
            
        with col2:
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart(fig)
        