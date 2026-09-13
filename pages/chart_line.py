"""
Página de Mapas Interativos
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
from services.data_loader import DataLoader
from services.data_processor import DataProcessor
from config import Config

# Versao original
#def get_chart_layout():
#    """Retorna layout da página de mapas"""
#    loader = DataLoader()
#    
#    return html.Div([
#        dbc.Container([
#            # Header
#            _create_chart_header(), 
#            # grafico 
#            line_chart()         
#            
#        ], fluid=True)
#    ], style={'padding': '20px', 'minHeight': '100vh'})

#Versao drop
def get_chart_layout():
    loader = DataLoader()
    # NOVO: Adiciona opções de ID para dropdown usando função já existente do DataProcessor
    
    id_options = DataProcessor().get_ids()
    return html.Div([
        dbc.Container([
            _create_chart_header(),
            #Slider
            html.Div([
                html.H5(
                    "Selecione o ano inicial", 
                    className = "mb-2", 
                    style={'textAlign': 'center'}
                ),
                dcc.Slider(
                    id='ano-slider',
                    min=1950,
                    max=2025,
                    step=1,
                    value=1950,
                    marks={ano: str(ano) for ano in range(1950,2026,4)},
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode='mouseup',
                    included=True
                ),
            ], 
            style={'marginBottom': '32px'}),

            # NOVO: Dropdown para seleção de ID
            html.Div([    
                html.H5(
                    "Selecione a categoria",
                    className="mb-2",
                    style={
                        'color': 'white', 
                        'textAlign': 'center'
                    }
                ),            
                dcc.Dropdown(
                    id='id-dropdown',
                    options=id_options,
                    placeholder = "Selecione a categoria de interesse",
                    className='custom-dropdown',   # chave para CSS consistente
                    style={'width': '100%', 'maxWidth': '350px', 'margin': '0 auto','textAlign': 'center'}
                    ),
                ], 
                style={'marginBottom': '20px'}),
            html.Br(),
            html.Br(),
            line_chart(), 
            html.Div(id="tabela-dados-container") # Insere tabela de dados
        ], fluid=True)
    ], style={'padding': '20px', 'minHeight': '100vh'})


def _create_chart_header():
    """Cria cabeçalho da página"""
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.H3(
                    "Acompanhe a dinâmica das espécies exóticas no Paraná ao longo do tempo",
                    className="text-center mb-4",
                    style={
                        'color': Config.COLORS['text'], 
                        'fontWeight': '300'}
                ),
                html.H4(
                    "Visualize de forma interativa os registros das espécies exóticas do Paraná.",
                    className="text-center mb-4",
                    style={
                        'color': Config.COLORS['text'], 
                        'fontWeight': '180'}
                ),
                dcc.Markdown([
                    """
                   Compreender a introdução e o estabelecimento de organismos fora de sua área nativa exige uma análise profunda de padrões espaciais e temporais. A partir desta plataforma, visualize de forma interativa os registros das espécies exóticas do Paraná para examinar o crescimento histórico dessas ocorrências. O sistema permite entender como essas espécies se comportam ao ocupar diferentes habitats e ao se diversificar em múltiplos grupos taxonômicos dentro do estado.O grande diferencial desta análise é a integração de marcadores históricos fundamentais, que fornecem o pano de fundo necessário para uma interpretação rica e contextualizada da biologia da invasão na região.Explore as ferramentas interativas logo abaixo. Manipule o controle deslizante para visualizar as grandes transformações ao longo das décadas e utilize o sistema de filtragem para isolar as variáveis e investigar detalhadamente as categorias de seu interesse científico.

                    """
                    ],
                className="mb-4",
                style={
                    'color': Config.COLORS['text_secondary'],
                    'fontSize': '18px',
                    'textAlign': 'justify'
                })

            ], className="page-header")
        ])
    ])


def line_chart():
    return html.Div([
    dcc.Graph(id='time-series-graph')
])