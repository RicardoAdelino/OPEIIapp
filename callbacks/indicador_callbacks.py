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

    # Nova seção
    def _resolve_habitat(selected_habitat):
        """Se nada foi selecionado ainda, usa o primeiro habitat disponível
        apenas para popular o gráfico/tabela — sem marcar nada no dropdown."""
        if selected_habitat is None and habitat_list:
            return habitat_list[0]
        return selected_habitat
    
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

        # 1. Garanta que a coluna seja tratada como texto/categoria
        df_habitat['quantile_class'] = df_habitat['quantile_class'].astype(str)

        # 2. Pegue as classes únicas ordenadas (ex: ['1', '2', '3', '4'])
        # Substitua 'Classe_Que_Sera_Cinza' pelo nome real da sua classe (ex: '0' ou 'Sem dados')
        classe_cinza = 'Deficiente de dados' 
        classes_restantes = [c for c in sorted(df_habitat['quantile_class'].unique()) if c != classe_cinza]

        # 3. Pega as cores vermelhas necessárias para as classes restantes
        cores_vermelhas = px.colors.sample_colorscale(px.colors.sequential.Reds, len(classes_restantes))

        # 4. Cria o mapeamento manual de cores (Color Discrete Map)
        mapa_cores = {classe_cinza: "#1f293365"}  # #808080 é o código hexadecimal para cinza
        for classe, cor in zip(classes_restantes, cores_vermelhas):
            mapa_cores[classe] = cor
        
        fig = px.choropleth_map(
            df_habitat,
            locations='name_muni',
            geojson=mapa_,
            color='quantile_class',
            featureidkey="properties.name_muni",
            map_style=Config.MAPBOX_STYLE,
            center=Config.MAP_CENTER,
            zoom = 6.2,
            #zoom=Config.MAP_ZOOM,
            opacity=0.8,
            hover_name="name_muni",
            hover_data={'quantile_class': True},
            #color_discrete_sequence= px.colors.sequential.Reds,
            color_discrete_map=mapa_cores,  # Usa o mapeamento customizado aqui
            category_orders={'quantile_class': [classe_cinza] + classes_restantes}, # Organiza a legenda
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
                bgcolor= "rgba(0,0,0,0)", #Config.COLORS['secondary'],
                font_size=12,
                font_family="Arial"
            )
        )
        
        #fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Classificação: %{z}")
        fig.update_traces(
            hovertemplate='<b>Município</b>: %{hovertext}<br>'
            '<b>Classificação</b>: %{z}'
            '<extra></extra>',
            hoverinfo='text'  # ← Remove a divis~ao de cores!
        )
        return fig
