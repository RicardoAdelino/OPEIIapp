"""
Callbacks da Página de Mapas
"""
from dash import Input, Output
import plotly.express as px
from services.data_processor import DataProcessor
from services.data_loader import DataLoader
from components.tables import create_data_table
from config import Config

def register_mapa_callbacks(app):
    """Registra callbacks da página de mapas"""
    processor = DataProcessor()
    loader = DataLoader()
    
    @app.callback(
        Output('mapa-data-table', 'children'),
        [Input('habitat-picker', 'value')]
    )
    def update_table_map(selected_habitat):
        """Atualiza tabela de municípios"""
        bar_data = processor.get_top_municipalities(selected_habitat, top_n=20)
        return [create_data_table(bar_data, table_id='mapa-table-data')]
    
    @app.callback(
        Output('map-brazil', 'figure'),
        [Input('habitat-picker', 'value')]
    )
    def update_map_brazil(selected_habitat):
        """Atualiza mapa de distribuição"""
        df_habitat = processor.get_habitat_data_for_map(selected_habitat)
        mapa_ = loader.load_pr_geojson()
        
        fig = px.choropleth_mapbox(
            df_habitat,
            locations='name_muni',
            geojson=mapa_,
            color='quantile_class',
            featureidkey="properties.name_muni",
            mapbox_style=Config.MAPBOX_STYLE,
            center=Config.MAP_CENTER,
            zoom = 6.2,
            #zoom=Config.MAP_ZOOM,
            opacity=0.8,
            hover_name="name_muni",
            hover_data={'quantile_class': True},
            color_discrete_sequence=px.colors.sequential.Reds,
            title=f"Distribuição: {selected_habitat}"
        )
        
        fig.update_layout(
            margin={"r": 10, "t": 50, "l": 10, "b": 10},
            paper_bgcolor=Config.COLORS['background'],
            plot_bgcolor=Config.COLORS['background'],
            legend_title_text="Classificação",
            font=dict(color=Config.COLORS['text'], family="Arial"),
            title={
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': Config.COLORS['text']}
            },
            hoverlabel=dict(
                bgcolor=Config.COLORS['secondary'],
                font_size=12,
                font_family="Arial"
            )
        )
        
        fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Classificação: %{z}")
        return fig
