"""
Callbacks da Página de Formulários
"""
from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from services.data_processor import DataProcessor
import geopandas as gpd
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import json

# teste slider e dropD
def register_ocorrencia_callbacks(app):
    """Registra callbacks da página de formulários"""
    processor = DataProcessor()
    
    @app.callback(
        [Output('mapa-densidade', 'figure'),
         Output('mapa-distribuicao', 'figure')],
        [Input('slider-ano', 'value'),
         Input('dropdown-id', 'value')]
    )
    def atualizar_mapas(ano_inicial, selected_id):
        # Obter dados processados
        dados = processor.get_oco_data_for_map()
        # Filtra pelo ano do slider
        #dados = dados[dados['ano_final'] >= ano_inicial]
        dados = dados[dados['ano_final'] >= max(1950, ano_inicial)] #Inicia dados a partir de 1950
        # Filtra pelo ID do dropdown, se houver seleção
        if selected_id:
            dados = dados[dados['ID'] == selected_id]
        
        # --- Mapa de densidade ---
        fig_densidade = px.density_mapbox(
            dados,
            lat='Latitude',
            lon='Longitude',
            radius=3,
            mapbox_style='carto-darkmatter',
            center=dict(lat=-24.845946, lon=-51.557551),
            zoom=6.3,
            opacity=0.85,
            color_continuous_scale='Spectral_r',
            hover_data={
                'Municipio': True,
                'Ocorrencia': True,
                'Latitude': ':.4f',
                'Longitude': ':.4f',
            }
        )
        fig_densidade.update_layout(
            coloraxis_showscale=True, 
            margin=dict(l=0, r=0, t=0, b=0), 
            coloraxis_colorbar=dict(
                tickfont=dict(color='white'),
                tickcolor='white',
                title=dict(font=dict(color='white'))
            ),
        )

        # --- Mapa de distribuição ---
        fig_distribuicao = px.scatter_mapbox(
            dados,
            lat="Latitude",
            lon="Longitude",
            hover_name="especie",
            zoom=6.3,
            mapbox_style='carto-darkmatter'
        )
        fig_distribuicao.update_traces(
            marker=dict(
                color='#CCFF00',
                size=8,
                opacity=0.4
            ),
            hovertemplate='%{hovertext}'
        )
        fig_distribuicao.update_layout(
            mapbox=dict(
                center=dict(lat=-24.845946, lon=-51.557551),
                zoom=6.3,
                style='carto-darkmatter'
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial",
                font_color="black"
            ),
            showlegend=False
        )

        return fig_densidade, fig_distribuicao


#def register_ocorrencia_callbacks(app):
#    """Registra callbacks da página de formulários"""
#    processor = DataProcessor()
#    
#    # Callback para o Mapa de Densidade
#    @app.callback(
#        Output('mapa-densidade', 'figure'),
#        Input('mapa-densidade', 'id')
#    )
#
#    def update_mapa_densidade(_):
#        """Atualiza o mapa de densidade"""
#        # Obter dados processados
#        dados = processor.get_oco_data_for_map()
#            
#        # Criar mapa de densidade
#        # Criar o mapa de densidade, passando o valor do KDE no popup
#        fig = px.density_mapbox(
#            dados,
#            lat='Latitude',
#            lon='Longitude',
#            radius=3,
#            mapbox_style='carto-darkmatter',
#            center=dict(lat=-24.845946, lon=-51.557551),
#            zoom = 6.3,
#            opacity=0.85,
#            color_continuous_scale='Spectral_r',
#            hover_data={
#                'Municipio': True,            # Coluna shapefile primeiro
#                'Ocorrencia':True,
#                #'Densidade': True,     # Coluna shapefile segundo
#                'Latitude': ':.4f',     # Latitude formatada
#                'Longitude': ':.4f',    # Longitude formatada
#                }
#            )
#        #
#        ## Adiciona um caption de informação
#        #fig.add_annotation(
#        #    text="Fonte: Observatório de Espécies Exóticas do Paraná, 2025",
#        #    xref="paper",
#        #    yref="paper",
#        #    x=0.5,
#        #    y=-0.05,  # Posição abaixo do gráfico
#        #    showarrow=False,
#        #    font=dict(size=1, color="black"),
#        #    xanchor="center",
#        #    yanchor="top"
#        #)
#        fig.update_layout(
#            coloraxis_showscale=True, 
#            margin=dict(l=0, r=0, t=0, b=0), 
#            coloraxis_colorbar=dict(
#                tickfont=dict(color='white'),      # Cor dos números (ticks)
#                tickcolor='white',                  # Cor das linhas dos ticks
#                title=dict(
#                    font=dict(color='white')
#                ) # Cor do título (se tiver)
#            ),
#        )
#        return fig
#    
#    
#    # Callback para o Mapa de Distribuição
#    @app.callback(
#        Output('mapa-distribuicao', 'figure'),
#        Input('mapa-distribuicao', 'id')
#    )
#
#    def update_mapa_distribuicao(_):
#        """Atualiza o mapa de distribuição"""
#        # Obter dados processados
#        dados = processor.get_oco_data_for_map()
#        # Criar figura vazia
#
#        fig = px.scatter_map(
#            dados, 
#            lat="Latitude", 
#            lon="Longitude", 
#            hover_name="especie",
#            zoom=6.3
#        )
#
#        fig.update_traces(
#            marker=dict(
#                color='#CCFF00',      # Verde limão neon
#                size=8,              # Bem maior
#                opacity=0.4           # Transparência média
#            ),
#            hovertemplate='%{hovertext}<extra></extra>'
#        )
#
#        fig.update_layout(
#            map=dict(
#                center=dict(lat=-24.845946, lon=-51.557551),
#                zoom=6.3,
#                style='carto-darkmatter'
#            ),
#            margin=dict(l=0, r=0, t=0, b=0),
#            hoverlabel=dict(
#                bgcolor="white",
#                font_size=12,
#                font_family="Arial",
#                font_color="black"
#            ),
#            showlegend=False
#        )
#        # Trace 1: Círculos maiores (borda)
#        #trace_border = go.Scattermapbox(
#        #    lat=dados['Latitude'],
#        #    lon=dados['Longitude'],
#        #    mode='markers',
#        #    marker=dict(
#        #        size=8,  # Tamanho maior para a borda
#        #        color='rgba(255, 255, 255, 0.9)'  # Cor da borda (branco)
#        #    ),
#        #    showlegend=False,
#        #    hoverinfo='skip'  # Não mostrar hover neste trace
#        #)
##
#        ## Trace 2: Círculos menores (preenchimento)
#        #trace_fill = go.Scattermapbox(
#        #    lat=dados['Latitude'],
#        #    lon=dados['Longitude'],
#        #    mode='markers',
#        #    marker=dict(
#        #        size=7,  # Tamanho menor para o preenchimento
#        #        color='rgba(178, 34, 34, 0.2)'  # Cor do preenchimento
#        #    ),
#        #    text=dados['especie'],
#        #    hovertemplate='<b>%{text}</b><br>Lat: %{lat:.4f}<br>Lon: %{lon:.4f}<extra></extra>',
#        #    showlegend=False
#        #)
##
#        ## Criar figura com os dois traces
#        #fig = go.Figure(data=[trace_border, trace_fill])
##
#        #fig.update_layout(
#        #    mapbox=dict(
#        #        style='carto-darkmatter',
#        #        center=dict(lat=-24.845946, lon=-51.557551),
#        #        zoom= 5.2
#        #    ),
#        #    margin=dict(l=0, r=0, t=0, b=0),
#        #    height=600
#        #)
#        ## Imagem dos pontos no espaço
#        ## Essa imagem deve ser usada para mostrar os pontos por classe
#        ##fig = px.scatter_mapbox(
#        #    dados, 
#        #    lat="Latitude", 
#        #    lon="Longitude", 
#        #    hover_name="especie",
#        #    zoom = 5.5, 
#        #    mapbox_style='carto-darkmatter'
#        #)
#        ## Estilo neon
#        #fig.update_traces(
#        #    marker=dict(
#        #        size=10,
#        #        color='rgba(0, 255, 255, 0.5)',    # Ciano brilhante
#        #        line=dict(
#        #            width=2,
#        #            color='rgba(255, 0, 255, 0.8)'  # Magenta brilhante
#        #        )
#        #    )
#        #)
#            #fig.show()
#
#        ## Add the GeoJSON as a layer
#        #fig.update_layout(
#        #    mapbox_style="carto-darkmatter", # Or any other Mapbox style
#            #mapbox_layers=[
#            #    {
#            #        "sourcetype": "geojson",
#            #        "source": json.loads(load_pr_geojson),
#            #        "type": "fill",
#            #        "color": "lightblue",
#            #        "opacity": 0.5,
#            #        "below": 'traces' # Ensure GeoJSON is below the points
#            #    }
#            #]
#        #)
#        return fig
#