"""
Página de Mapas Interativos
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
from services.data_loader import DataLoader
from services.data_processor import DataProcessor
from config import Config

def get_indicator_layout():
    loader = DataLoader()
    habitat_list = loader.get_habitat_list()
    # NOVO: Adiciona opções de ID para dropdown usando função já existente do DataProcessor
    return html.Div([
        dbc.Container([
            # Header
            _create_indicator_header(),
            
            # Seletor de Habitat
            _create_habitat_selector(habitat_list),
            
            # Mapa e Tabela
            _create_map_and_table()
            
        ], fluid=True)
    ], style={'padding': '20px', 'minHeight': '100vh'})



def _create_indicator_header():
    """Cria cabeçalho da página"""
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.H3(
                    "Acompanhe o indicador de vulnerabilidade espacial das espécies exóticas no Paraná",
                    className="text-center mb-4",
                    style={'color': Config.COLORS['text'], 'fontWeight': '300'}
                ),
                dcc.Markdown([
                    """
                    Acompanhe nosso indicador de vulnerabilidade espacial para as espécies exóticas no Paraná.
                    Essa ferramenta foi desenvolvida pelo Observatório para facilitar a visualização de áreas sensíveis à invasão, apoiar decisões estratégicas de conservação e 
                    fortalecer o compromisso coletivo com o manejo e proteção da biodiversidade nativa do estado.
                    """],
                    className="mb-4",
                    style={
                        'color': Config.COLORS['text_secondary'],
                        'fontSize': '18px',
                        'textAlign': 'justify'
                    }
                )
            ], className="page-header")
        ])
    ])

def _create_habitat_selector(habitat_list):
    """Cria seletor de habitat centralizado - versão simples"""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label(
                        "Selecione a forma de vida",
                        className="text-center",
                        style={
                            'fontWeight': '600',
                            'color': '#FFFFFF',
                            'marginBottom': '10px',
                            'display': 'block',
                            'fontSize': '16px'
                        }
                    ),
                    dcc.Dropdown(
                        id='habitat-picker',
                        value=habitat_list[1] if len(habitat_list) > 1 else habitat_list[0],
                        options=[{'label': hab, 'value': hab} for hab in habitat_list],
                        clearable=False,
                        style={
                            'width': '100%', 
                            'maxWidth': '350px', 
                            'margin': '0 auto',
                            'textAlign': 'center',
                        }
                    )
                ], style={'padding': '20px'})
            ], 
            className='custom-dropdown',   # chave para CSS consistente
            #className="shadow-sm", 
              style={
                  'backgroundColor': 'transparent',
                  'border': '1px solid transparent',
                  'borderRadius': '8px'
              }
            )
        ], md=6, lg=4, className="mx-auto")
    ], className="mb-4")

def _create_map_and_table():
    """Cria layout do mapa e tabela"""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(id='map-brazil')])
            ], className="shadow", 
               style={
                   'backgroundColor': 'transparent', 
                   'border': 'none', 
                   'height': '600px'})
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H5("Top 20 Municípios", 
                           style={
                               'color': '#FFFFFF', 
                               'margin': '0', 
                               'fontWeight': '500'}),
                    style={
                        'backgroundColor': '#cbfd02ac', # '#375a7f'
                        'borderBottom': 'none',
                        'padding': '12px 20px'
                    }
                ),
                dbc.CardBody([
                    html.Div(
                        id='mapa-data-table',
                        style={
                            'height': '520px',
                            'overflowY': 'auto',
                            'backgroundColor': 'transparent'  # Transparente
                        }
                    )
                ], style={
                    'backgroundColor': 'transparent', 
                    'padding': '0'})  # Card body transparente
            ], className="shadow", 
               style={
                   'backgroundColor': 'transparent',  # Card transparente
                   'border': 'none',
                   'height': '600px',
                   'borderRadius': '8px'
               })
        ], width=4)
    ])
