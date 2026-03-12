from dash import Output, Input
#from services.data_processor import class_colors
from services.data_processor import DataProcessor
import rasterio
import geopandas as gpd
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
from rasterio.features import geometry_mask

from dash import Output, Input
from services.data_processor import DataProcessor
import numpy as np
import plotly.graph_objects as go
import json

def register_modelos_callbacks(app):
    """Registra callbacks para os rasters"""
    
    processor = DataProcessor()
    pr_geojson = processor.get_pr_geometry()
    geojson_data = json.loads(processor.get_pr_geometry().to_json())
    
    # Agora retorna um dicionário com grupos
    raster_groups = processor.get_raster_data()
    
    @app.callback(
        Output('modelos-map', 'figure'),
        Input('raster-group-dropdown', 'value')
    )
    def update_modelos_map(selected_group):
        # MAPEAMENTO PERSONALIZADO DAS CLASSES
        class_mapping = {
            0: "Atenção",
            1: "Preocupante",
            2: "Vulnerável",
            3: "Muito Vulnerável"
        }
        
        # Definir cores para cada classe
        class_colors = {
            "Muito Vulnerável": "#e41a1c",
            "Vulnerável": "#ff7f00",
            "Preocupante": "#4daf4a",
            "Atenção": "#377eb8"
        }
        
        # Verificar se há grupos disponíveis
        if not raster_groups:
            return create_empty_figure(geojson_data, pr_geojson, 
                                       "Nenhum grupo de dados disponível")
        
        # Se nenhum grupo selecionado ou grupo inválido, usar o primeiro disponível
        if selected_group is None or selected_group not in raster_groups:
            selected_group = list(raster_groups.keys())[0]
        
        # Obter o DataFrame do grupo selecionado
        df_combined = raster_groups[selected_group]
        
        # Verificar se o DataFrame está vazio ou não tem as colunas necessárias
        if df_combined.empty:
            return create_empty_figure(geojson_data, pr_geojson, 
                                       f"Grupo '{selected_group}' não contém dados")
        
        if 'value_a_class' not in df_combined.columns:
            return create_empty_figure(geojson_data, pr_geojson, 
                                       f"Grupo '{selected_group}' com estrutura inválida")
        
        # Obter o label do value_b
        label_b = df_combined['label_b'].iloc[0] if 'label_b' in df_combined.columns else 'Valor B'
        
        # Criar figura
        fig = go.Figure()
        
        # Ordem preferencial das classes
        class_order = ["Atenção", "Preocupante", "Vulnerável", "Muito Vulnerável"]
        
        # Adicionar pontos para cada categoria separadamente
        for class_name in class_order:
            if class_name in df_combined['value_a_class'].values:
                df_category = df_combined[df_combined['value_a_class'] == class_name]
                
                fig.add_trace(go.Scattermapbox(
                    lat=df_category['y_coord'],
                    lon=df_category['x_coord'],
                    mode='markers',
                    marker=dict(
                        size=6,
                        color=class_colors[class_name],
                        opacity=0.85
                    ),
                    customdata=np.column_stack((
                        df_category['name_muni'],
                        df_category['value_a_class'],
                        df_category['value_b']
                    )),
                    hovertemplate=(
                        '<b>%{customdata[0]}</b><br>' +
                        'Classificação: %{customdata[1]}<br>' +
                        f'{label_b}: ' + '%{customdata[2]:.2f}<extra></extra>'
                    ),
                    name=class_name,
                    showlegend=True
                ))
        
        # === CONTORNOS PROFISSIONAIS ===
        # Layer 1: Sombra/base escura
        fig.add_trace(go.Choroplethmapbox(
            geojson=geojson_data,
            locations=pr_geojson.index,
            z=[0] * len(pr_geojson),
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
            marker_line_color='rgba(0, 0, 0, 0.5)',
            marker_line_width=3.5,
            showscale=False,
            hoverinfo='skip',
            showlegend=False,
            name='Contorno Base'
        ))
        
        # Layer 2: Linha clara principal
        fig.add_trace(go.Choroplethmapbox(
            geojson=geojson_data,
            locations=pr_geojson.index,
            z=[0] * len(pr_geojson),
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
            marker_line_color='rgba(200, 200, 200, 0.8)',
            marker_line_width=1.5,
            showscale=False,
            hoverinfo='skip',
            showlegend=False,
            name='Contorno Principal'
        ))
        
        # Layer 3: Linha fina brilhante
        fig.add_trace(go.Choroplethmapbox(
            geojson=geojson_data,
            locations=pr_geojson.index,
            z=[0] * len(pr_geojson),
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
            marker_line_color='rgba(255, 255, 255, 0.4)',
            marker_line_width=0.5,
            showscale=False,
            hoverinfo='skip',
            showlegend=False,
            name='Contorno Realce'
        ))
        
        # Layout
        fig.update_layout(
            mapbox=dict(
                style='carto-darkmatter',
                zoom=6,
                center=dict(lat=-24.845946, lon=-51.557551)
            ),
            font=dict(family='Arial, sans-serif', size=12, color='#ffffff'),
            margin={"r":0, "t":50, "l":0, "b":0},
            paper_bgcolor='#0a0a0a',
            plot_bgcolor='#0a0a0a',
            hoverlabel=dict(
                bgcolor='#1a1a1a',
                bordercolor='#00d9ff',
                font=dict(color='#ffffff', family='Arial, sans-serif')
            ),
            legend=dict(
                title=dict(text='Classificação', font=dict(color='#ffffff', size=14)),
                bgcolor='rgba(26, 26, 26, 0.8)',
                bordercolor='#00d9ff',
                borderwidth=1,
                font=dict(color='#ffffff', size=12),
                itemsizing='constant',
                orientation='v',
                yanchor='top',
                y=0.99,
                xanchor='left',
                x=0.01
            ),
            height=700
        )
        
        return fig


def create_empty_figure(geojson_data, pr_geojson, message):
    """Cria uma figura vazia com mensagem de erro"""
    fig = go.Figure()
    
    # Adicionar apenas os contornos
    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=pr_geojson.index,
        z=[0] * len(pr_geojson),
        colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
        marker_line_color='rgba(200, 200, 200, 0.8)',
        marker_line_width=2,
        showscale=False,
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Layout com mensagem
    fig.update_layout(
        mapbox=dict(
            style='carto-darkmatter',
            zoom=6.5,
            center=dict(lat=-24.845946, lon=-51.557551)
        ),
        annotations=[
            dict(
                text=message,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=20, color='#ffffff'),
                bgcolor='rgba(26, 26, 26, 0.8)',
                bordercolor='#ff4444',
                borderwidth=2,
                borderpad=10
            )
        ],
        font=dict(family='Arial, sans-serif', size=12, color='#ffffff'),
        margin={"r":0, "t":50, "l":0, "b":0},
        paper_bgcolor='#0a0a0a',
        plot_bgcolor='#0a0a0a',
        height=700
    )
    
    return fig

#def register_modelos_callbacks(app):
#    """Registra callbacks para os rasters"""
#    
#    processor = DataProcessor()
#    pr_geojson = processor.get_pr_geometry()
#    geojson_data = json.loads(processor.get_pr_geometry().to_json())
#    
#    # Agora retorna um dicionário com grupos
#    raster_groups = processor.get_raster_data()
#    
#    @app.callback(
#        Output('modelos-map', 'figure'),
#        Input('raster-group-dropdown', 'value')
#    )
#    def update_modelos_map(selected_group):
#        # Se nenhum grupo selecionado, usar o primeiro disponível
#        if selected_group is None:
#            selected_group = list(raster_groups.keys())[0]
#        
#        # Obter o DataFrame do grupo selecionado
#        df_combined = raster_groups[selected_group]
#        
#        # MAPEAMENTO PERSONALIZADO DAS CLASSES
#        class_mapping = {
#            0: "Atenção",
#            1: "Preocupante",
#            2: "Vulnerável",
#            3: "Muito Vulnerável"
#        }
#        
#        # Definir cores para cada classe
#        class_colors = {
#            "Muito Vulnerável": "#e41a1c",
#            "Vulnerável": "#ff7f00",
#            "Preocupante": "#4daf4a",
#            "Atenção": "#377eb8"
#        }
#        
#        # Obter o label do value_b
#        label_b = df_combined['label_b'].iloc[0] if not df_combined.empty else 'Valor B'
#        
#        # Criar figura
#        fig = go.Figure()
#        
#        # Ordem preferencial das classes
#        class_order = ["Atenção", "Preocupante", "Vulnerável", "Muito Vulnerável"]
#        
#        # Adicionar pontos para cada categoria separadamente
#        for class_name in class_order:
#            if class_name in df_combined['value_a_class'].values:
#                df_category = df_combined[df_combined['value_a_class'] == class_name]
#                
#                fig.add_trace(go.Scattermapbox(
#                    lat=df_category['y_coord'],
#                    lon=df_category['x_coord'],
#                    mode='markers',
#                    marker=dict(
#                        size=6,
#                        color=class_colors[class_name],
#                        opacity=0.85
#                    ),
#                    customdata=np.column_stack((
#                        df_category['name_muni'],
#                        df_category['value_a_class'],
#                        df_category['value_b']
#                    )),
#                    hovertemplate=(
#                        '<b>%{customdata[0]}</b><br>' +
#                        'Classificação: %{customdata[1]}<br>' +
#                        f'{label_b}: ' + '%{customdata[2]:.2f}<extra></extra>'
#                    ),
#                    name=class_name,
#                    showlegend=True
#                ))
#        
#        # === CONTORNOS PROFISSIONAIS ===
#        # Layer 1: Sombra/base escura
#        fig.add_trace(go.Choroplethmapbox(
#            geojson=geojson_data,
#            locations=pr_geojson.index,
#            z=[0] * len(pr_geojson),
#            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
#            marker_line_color='rgba(0, 0, 0, 0.5)',
#            marker_line_width=3.5,
#            showscale=False,
#            hoverinfo='skip',
#            showlegend=False,
#            name='Contorno Base'
#        ))
#        
#        # Layer 2: Linha clara principal
#        fig.add_trace(go.Choroplethmapbox(
#            geojson=geojson_data,
#            locations=pr_geojson.index,
#            z=[0] * len(pr_geojson),
#            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
#            marker_line_color='rgba(200, 200, 200, 0.8)',
#            marker_line_width=1.5,
#            showscale=False,
#            hoverinfo='skip',
#            showlegend=False,
#            name='Contorno Principal'
#        ))
#        
#        # Layer 3: Linha fina brilhante
#        fig.add_trace(go.Choroplethmapbox(
#            geojson=geojson_data,
#            locations=pr_geojson.index,
#            z=[0] * len(pr_geojson),
#            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
#            marker_line_color='rgba(255, 255, 255, 0.4)',
#            marker_line_width=0.5,
#            showscale=False,
#            hoverinfo='skip',
#            showlegend=False,
#            name='Contorno Realce'
#        ))
#        
#        # Layout
#        fig.update_layout(
#            mapbox=dict(
#                style='carto-darkmatter',
#                zoom=6,
#                center=dict(lat=-24.845946, lon=-51.557551)
#            ),
#            font=dict(family='Arial, sans-serif', size=12, color='#ffffff'),
#            margin={"r":0, "t":50, "l":0, "b":0},
#            paper_bgcolor='#0a0a0a',
#            plot_bgcolor='#0a0a0a',
#            hoverlabel=dict(
#                bgcolor='#1a1a1a',
#                bordercolor='#00d9ff',
#                font=dict(color='#ffffff', family='Arial, sans-serif')
#            ),
#            legend=dict(
#                title=dict(text='Classificação', font=dict(color='#ffffff', size=14)),
#                bgcolor='rgba(26, 26, 26, 0.8)',
#                bordercolor='#00d9ff',
#                borderwidth=1,
#                font=dict(color='#ffffff', size=12),
#                itemsizing='constant',
#                orientation='v',
#                yanchor='top',
#                y=0.99,
#                xanchor='left',
#                x=0.01
#            ),
#            height=700
#        )
#        
#        return fig
#
#
## def register_modelos_callbacks(app):
##     """Registra callbacks para os rasters"""
##     processor = DataProcessor()
##     pr_geojson = processor.get_pr_geometry()
##     geojson_data = json.loads(processor.get_pr_geometry().to_json())
##     df_combined = processor.get_raster_data()

#     @app.callback(
#         Output('modelos-map', 'figure'),
#         Input('raster-group-dropdown', 'value')
#     )
    
#     def update_modelos_map(selected_raster):
#         # MAPEAMENTO PERSONALIZADO DAS CLASSES
#         class_mapping = {
#             0: "Atenção",
#             1: "Preocupante", 
#             2: "Vulnerável",
#             3: "Muito Vulnerável"
#         }
        
#         # Definir cores para cada classe
#         class_colors = {
#             "Muito Vulnerável": "#e41a1c",
#             "Vulnerável": "#ff7f00",
#             "Preocupante": "#4daf4a",
#             "Atenção": "#377eb8"    
#         }

#         # Criar figura
#         fig = go.Figure()

#         # Ordem preferencial das classes (do menos ao mais vulnerável)
#         class_order = ["Atenção", "Preocupante", "Vulnerável", "Muito Vulnerável"]

#         # Adicionar pontos para cada categoria separadamente
#         for class_name in class_order:
#             if class_name in df_combined['value_a_class'].values:
#                 df_category = df_combined[df_combined['value_a_class'] == class_name]

#                 fig.add_trace(go.Scattermapbox(
#                     lat=df_category['y_coord'],
#                     lon=df_category['x_coord'],
#                     mode='markers',
#                     marker=dict(
#                         size=6,
#                         color=class_colors[class_name],
#                         opacity=0.85
#                     ),
#                     customdata=np.column_stack((df_category['name_muni'], 
#                                                  df_category['value_a_class'],
#                                                  df_category['value_b'])),
#                     hovertemplate='<b>%{customdata[0]}</b><br>' +
#                                   'Classificação: %{customdata[1]}<br>' +
#                                   'Pressão de Colonização: %{customdata[2]:.2f}<extra></extra>', #<- rotulo hover B
#                     name=class_name,
#                     showlegend=True
#                 ))

#                 # === CONTORNOS PROFISSIONAIS ===
#                 # Layer 1: Sombra/base escura (mais grossa)
#                 fig.add_trace(go.Choroplethmapbox(
#                     geojson=geojson_data,
#                     locations=pr_geojson.index,
#                     z=[0] * len(pr_geojson),
#                     colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
#                     marker_line_color='rgba(0, 0, 0, 0.5)',
#                     marker_line_width=3.5,
#                     showscale=False,
#                     hoverinfo='skip',
#                     showlegend=False,
#                     name='Contorno Base'
#                 ))

#                 # Layer 2: Linha clara principal
#                 fig.add_trace(go.Choroplethmapbox(
#                     geojson=geojson_data,
#                     locations=pr_geojson.index,
#                     z=[0] * len(pr_geojson),
#                     colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
#                     marker_line_color='rgba(200, 200, 200, 0.8)',
#                     marker_line_width=1.5,
#                     showscale=False,
#                     hoverinfo='skip',
#                     showlegend=False,
#                     name='Contorno Principal'
#                 ))

#             # Layer 3: Linha fina brilhante no topo (opcional - para efeito extra)
#             fig.add_trace(go.Choroplethmapbox(
#                 geojson=geojson_data,
#                 locations=pr_geojson.index,
#                 z=[0] * len(pr_geojson),
#                 colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
#                 marker_line_color='rgba(255, 255, 255, 0.4)',
#                 marker_line_width=0.5,
#                 showscale=False,
#                 hoverinfo='skip',
#                 showlegend=False,
#                 name='Contorno Realce'
#             ))

#             # Layout
#             fig.update_layout(
#                 mapbox=dict(
#                     style='carto-darkmatter',
#                     zoom=6,
#                     center=dict(lat=-24.845946, lon=-51.557551)
#                 ),
#                 #title=dict(
#                 #    text="Análise de Vulnerabilidade por Município",
#                 #    x=0.5,
#                 #    xanchor='center',
#                 #    font=dict(size=20, color='#ffffff', family='Arial, sans-serif')
#                 #),
#                 font=dict(family='Arial, sans-serif', size=12, color='#ffffff'),
#                 margin={"r":0, "t":50, "l":0, "b":0},
#                 paper_bgcolor='#0a0a0a',
#                 plot_bgcolor='#0a0a0a',
#                 hoverlabel=dict(
#                     bgcolor='#1a1a1a',
#                     bordercolor='#00d9ff',
#                     font=dict(color='#ffffff', family='Arial, sans-serif')
#                 ),
#                 legend=dict(
#                     title=dict(text='Classificação', font=dict(color='#ffffff', size=14)),
#                     bgcolor='rgba(26, 26, 26, 0.8)',
#                     bordercolor='#00d9ff',
#                     borderwidth=1,
#                     font=dict(color='#ffffff', size=12),
#                     itemsizing='constant',
#                     orientation='v',
#                     yanchor='top',
#                     y=0.99,
#                     xanchor='left',
#                     x=0.01
#                 ),
#                 height=700
#             )
#         return fig