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

st.set_page_config(page_title='Visão Empresa', page_icon='📈', layout='wide')

#===================================================================================================
# Funções
#===================================================================================================
def country_maps(df1):
    df1_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
               .groupby(['City', 'Road_traffic_density'])
               .median()
               .reset_index())

    map = folium.Map()

    for index, location_info in df1_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'], 
                     location_info['Delivery_location_longitude']],
                     popup=location_info[['City','Road_traffic_density']]).add_to(map)

    folium_static(map, width=1024, height=600)

def order_share_by_week(df1):
    df1_aux1 = (df1.loc[:, ['ID', 'Week_of_year']]
                .groupby( 'Week_of_year' )
                .count()
                .reset_index())
    df1_aux2 = (df1.loc[:, ['Delivery_person_ID', 'Week_of_year']]
                .groupby( 'Week_of_year')
                .nunique(
                ).reset_index())
    df1_aux = pd.merge( df1_aux1, df1_aux2, how='inner' )
    df1_aux['order_by_delivery'] = df1_aux['ID'] / df1_aux['Delivery_person_ID']
    fig = px.line(df1_aux, x='Week_of_year', y='order_by_delivery')
    return fig

def order_by_week(df1):
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df1_aux = df1.loc[:, ['ID', 'Week_of_year']].groupby('Week_of_year').count().reset_index()
    fig = px.line(df1_aux, x='Week_of_year', y='ID')
    return fig
    

def traffic_order_city(df1):
    df1_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
               .groupby(['City', 'Road_traffic_density'])
               .count()
               .reset_index())
    fig = px.scatter(df1_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    return fig

def traffic_order_share(df1):
    df1_aux = (df1.loc[:, ['ID', 'Road_traffic_density']]
               .groupby('Road_traffic_density')
               .count()
               .reset_index())
    df1_aux = df1_aux.loc[df1_aux['Road_traffic_density'] != 'NaN', :]
    df1_aux['Entregas_perc'] = df1_aux['ID'] / df1_aux['ID'].sum()
    fig = px.pie(df1_aux, values='Entregas_perc', names='Road_traffic_density')
    return fig

def order_metric(df1):
    cols = ['ID', 'Order_Date']   
    # Selecionar linhas
    df1_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()   
    # Desenhar o grafico
    fig = px.bar(df1_aux, x='Order_Date', y='ID')
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

#==============================Incio da Estrutura Lógica do código==================================

# import dataset
df = pd.read_csv('datasets/train.csv')

# Limpando dados
df1 = clean_code(df)

#===================================================================================================
#BARRA LATERAL
#===================================================================================================

#image_path = '/Users/fabiomachida/Comunidade DS/repos/logo.png'
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.header('Marketplace - Visão Cliente')

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


traffic_options = st.sidebar.multiselect(
    'Quais as condições do transito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])
st.sidebar.markdown("""----""")

st.sidebar.markdown('### Powered by Comunidade DS')

#filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)

#=================================================================
#LAYOUT STREAMLIT
#=================================================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geogrpáfica'])

with tab1:
    with st.container():
        # Order metric
        fig = order_metric(df1)
        st.markdown('# Orders by day')
        st.plotly_chart(fig, use_container_width=True)
          
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig = traffic_order_share(df1)
            st.header('Traffic Order Share')
            st.plotly_chart(fig, use_container_width=True)
                
        with col2:
            st.header('Traffic Order City')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)
                                 
with tab2:
    with st.container():
        st.header('Order by Week')
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_countainer_width=True)
        
    with st.container():
        st.header('Order Share by Week')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
             
with tab3:
    st.header('Country Maps')
    country_maps(df1)
    