# """
# Página de Mapas Interativos
# """
# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from services.data_loader import DataLoader
# from config import Config

# def get_mapa_layout():
#     """Retorna layout da página de mapas"""
#     loader = DataLoader()
#     habitat_list = loader.get_habitat_list()
    
#     return html.Div([
#         dbc.Container([
#             # Header
#             _create_page_header(),
            
#             # Seletor de Habitat
#             _create_habitat_selector(habitat_list),
            
#             # Mapa e Tabela
#             _create_map_and_table()
            
#         ], fluid=True)
#     ], style={'padding': '20px', 'minHeight': '100vh'})

# def _create_page_header():
#     """Cria cabeçalho da página"""
#     return dbc.Row([
#         dbc.Col([
#             html.Div([
#                 html.H2(
#                     "Indicador de Vulnerabilidade",
#                     className="text-center mb-4",
#                     style={'color': Config.COLORS['text'], 'fontWeight': '300'}
#                 ),
#                 html.P(
#                     "Visualize o status de vulnerabilidade espacial para os municípios do Paraná",
#                     className="text-center mb-4",
#                     style={'color': Config.COLORS['text_secondary'], 'fontSize': '20px'}
#                 )
#             ], className="page-header")
#         ])
#     ])

# def _create_habitat_selector(habitat_list):
#     """Cria seletor de habitat centralizado - versão simples"""
#     return dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     html.Label(
#                         "Selecione o Habitat",
#                         className="text-center",
#                         style={
#                             'fontWeight': '600',
#                             'color': '#FFFFFF',
#                             'marginBottom': '10px',
#                             'display': 'block',
#                             'fontSize': '16px'
#                         }
#                     ),
#                     dcc.Dropdown(
#                         id='habitat-picker',
#                         value=habitat_list[1] if len(habitat_list) > 1 else habitat_list[0],
#                         options=[{'label': hab, 'value': hab} for hab in habitat_list],
#                         clearable=False,
#                         className='custom-dropdown',   # chave para CSS consistente
#                         style={
#                             'width': '100%', 
#                             'maxWidth': '350px', 
#                             'margin': '0 auto',
#                             'textAlign': 'center',
#                             # não precisa repetir 'color' aqui, deixe para o CSS
#                         }
#                     )
#                 ], style={'padding': '20px'})
#             ], className="shadow-sm", 
#                style={
#                    'backgroundColor': '#2C3E50',
#                    'border': '1px solid #375a7f',
#                    'borderRadius': '8px'
#                })
#         ], md=6, lg=4, className="mx-auto")
#     ], className="mb-4")

# #def _create_habitat_selector(habitat_list):
# #    """Cria seletor de habitat"""
# #    return dbc.Row([
# #        dbc.Col([
# #            dbc.Card([
# #                dbc.CardBody([
# #                    html.Label(
# #                        "Selecione o Habitat",
# #                        style={
# #                            'fontWeight': '600', 
# #                            'color': Config.COLORS['text'], 
# #                            'marginBottom': '10px'
# #                        }
# #                    ),
# #                    dcc.Dropdown(
# #                        id='habitat-picker',
# #                        value=habitat_list[1] if len(habitat_list) > 1 else habitat_list[0],
# #                        options=[{'label': hab, 'value': hab} for hab in habitat_list],
# #                        clearable=False,
# #                        className='custom-dropdown'
# #                    )
# #                ])
# #            ], className="shadow-sm", 
# #               style={'backgroundColor': Config.COLORS['secondary'], 'border': 'none'})
# #        ], width=6)
# #    ], className="mb-4")

# def _create_map_and_table():
#     """Cria layout do mapa e tabela"""
#     return dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([dcc.Graph(id='map-brazil')])
#             ], className="shadow", 
#                style={'backgroundColor': 'transparent', 'border': 'none', 'height': '600px'})
#         ], width=8),
        
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardHeader(
#                     html.H5("Top 20 Municípios", 
#                            style={'color': '#FFFFFF', 'margin': '0', 'fontWeight': '500'}),
#                     style={
#                         'backgroundColor': '#375a7f',
#                         'borderBottom': 'none',
#                         'padding': '12px 20px'
#                     }
#                 ),
#                 dbc.CardBody([
#                     html.Div(
#                         id='mapa-data-table',
#                         style={
#                             'height': '520px',
#                             'overflowY': 'auto',
#                             'backgroundColor': 'transparent'  # Transparente
#                         }
#                     )
#                 ], style={'backgroundColor': 'transparent', 'padding': '0'})  # Card body transparente
#             ], className="shadow", 
#                style={
#                    'backgroundColor': 'transparent',  # Card transparente
#                    'border': 'none',
#                    'height': '600px',
#                    'borderRadius': '8px'
#                })
#         ], width=4)
#     ])


# #def _create_map_and_table():
# #    """Cria layout do mapa e tabela"""
# #    return dbc.Row([
# #        dbc.Col([
# #            dbc.Card([
# #                dbc.CardBody([dcc.Graph(id='map-brazil')])
# #            ], className="shadow", 
# #               style={'backgroundColor': 'transparent', 'border': 'none', 'height': '600px'})
# #        ], width=8),
# #        
# #        dbc.Col([
# #            dbc.Card([
# #                dbc.CardHeader(
# #                    html.H5("Top 20 Municípios", 
# #                           style={'color': Config.COLORS['text'], 'margin': '0', 'fontWeight': '500'}),
# #                    style={'backgroundColor': Config.COLORS['primary'], 'borderBottom': '1px solid #444444'}
# #                ),
# #                dbc.CardBody([
# #                    html.Div(id='mapa-data-table', style={'height': '520px', 'overflowY': 'auto'})
# #                ])
# #            ], className="shadow", 
# #               style={'backgroundColor': Config.COLORS['secondary'], 'border': 'none', 'height': '600px'})
# #        ], width=4)
# #    ])
# #
