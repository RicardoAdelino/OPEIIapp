"""
Layout da Página de Formulários
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
from config import Config
from services.data_loader import DataLoader
from services.data_processor import DataProcessor

def get_ocorrencia_layout():
    id_options = DataProcessor().get_ids()
    """Retorna o layout da página de formulários com dois mapas"""
    return dbc.Container([
        # Título da página
        dbc.Row([
            dbc.Col([
                html.H3(
                    "Acompanhe a dinâmica das espécies exóticas no Paraná no espaço geográfico",
                    className="text-center mb-4",
                    style={'color': Config.COLORS['text'], 'fontWeight': '300'}
                ),
                dcc.Markdown(
                    """
                    Analise a distribuição dos registros das espécies exóticas diretamente no mapa e descubra as regiões com maior incidência de registros, 
                    por ano e formas de vida. Identifique a identidade das espécies,
                    padrões de dispersão, e, áreas estratégicas para pesquisa ou gestão ambiental. 
                    Por meio dos mapas de densidade e da distribuição dos registros em nossa base de dados 
                    você pode explorar quais onde as espécies introduzidas foram observadas e em quais regiões apresentam maior concentração de casos.
                    
                    """,
                    className="mb-4",
                    style={
                        'color': Config.COLORS['text_secondary'],
                        'fontSize': '20px',
                        'textAlign': 'justify'
                    }
                ), 
                # Adiciona espaço extra
                html.Div(style={'height': '40px'}),
            ])
        ]),

        # Adiciona SLIDER e MENU #bddd3d
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Selecione o ano inicial", className="mb-2", style={'textAlign': 'center'}),
                    dcc.Slider(
                        id = 'slider-ano',
                        min = 1950,
                        max = 2025,
                        step = 1,
                        value = 1900,
                        marks = {ano: str(ano) for ano in range(1950, 2026, 2)},
                        tooltip = {"placement": "bottom", "always_visible": True},
                        included = True,
                        updatemode = 'mouseup'
                    ),
                ], style={'marginBottom': '32px'}),
                html.Div([
                    html.H5("Selecione uma categoria", className="mb-2", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id='dropdown-id',
                        options=id_options,   # será preenchido dinamicamente ou pelo seu processor
                        placeholder="Selecione a categoria de interesse",
                        className='custom-dropdown',   # chave para CSS consistente
                        style={'width': '100%', 'maxWidth': '350px', 'margin': '0 auto','textAlign': 'center'}
                    ),
                ], style={'marginBottom': '24px'})
            ], width=12)
        ]),

        # Linha com os dois mapas lado a lado
        dbc.Row([
            # Mapa 1 - Lado esquerdo
            dbc.Col([
                html.H4('Estimador de densidade de registros', style={'color': 'white'}),
                dcc.Graph(
                    id='mapa-densidade',
                    style={'height': '600px'}
                )
            ], md=6, lg=6),  # Ocupa metade da tela
            
            # Mapa 2 - Lado direito
            dbc.Col([
                html.H4('Distribuição dos registros de ocorrência', style={'color': 'white'}),
                dcc.Graph(
                    id='mapa-distribuicao',
                    style={'height': '600px'}
                )
            ], md=6, lg=6)  # Ocupa metade da tela
        ], className='mb-4'),
        # Texto ilustrativo abaixo dos mapas
        #dbc.Row([
        #    dbc.Col([
        #        html.Div([
        #            html.P([
        #                "",
        #                html.Strong("Diagnóstico espacial estratégico: "),
        #                "os mapas permitem identificar rapidamente áreas críticas de ocorrência de espécies exóticas, otimizando o planejamento de ações preventivas e corretivas."
        #            ], 
        #            style={
        #                'fontSize': '18px', 
        #                'color': Config.COLORS['text'], 'textAlign': 'center', 'marginBottom': '12px'}),
        #            html.P([
        #                "",
        #                html.Strong("Foco em pontos quentes: "),
        #                "o mapa de densidade realça regiões com alta concentração de registros, facilitando o direcionamento de esforços de monitoramento e controle."
        #            ], style={'fontSize': '18px', 'color': Config.COLORS['text'], 'textAlign': 'center', 'marginBottom': '12px'}),
        #            html.P([
        #                "",
        #                html.Strong("Monitoramento detalhado: "),
        #                "a distribuição pontual permite acompanhar o avanço das espécies exóticas ao longo do tempo e do espaço, promovendo intervenções baseadas em evidências."
        #            ], style={'fontSize': '18px', 'color': Config.COLORS['text'], 'textAlign': 'center', 'marginBottom': '12px'}),
        #            html.P([
        #                "",
        #                html.Strong("Valor para pesquisa e gestão: "),
        #                "a plataforma oferece informações integradas para subsidiar estudos científicos, elaboração de políticas públicas e ações de educação ambiental."
        #            ], 
        #            style={
        #                'fontSize': '18px', 
        #                'color': Config.COLORS['text'], 'textAlign': 'center', 'marginBottom': '0'}),
        #        ],
        #            style={
        #                'backgroundColor': 'rgba(40, 44, 52, 0.86)',
        #                'borderRadius': '10px',
        #                'border': '1px solid #375a7f',
        #                'padding': '25px 20px',
        #                'marginTop': '24px',
        #                'boxShadow': '0 2px 8px rgba(0,0,0,0.12)'
        #            }
        #        )
        #    ], width=12)
        #]),
    ##        dbc.Row([
    ##    dbc.Col([
    ##        html.Div([
    ##           html.P([
    ##                "Os mapas acima representam visualmente a concentração e a distribuição de registros de espécies exóticas no estado do Paraná.",
    #                html.Br(),
    #                "O painel de densidade destaca áreas com maior incidência de ocorrências, enquanto o painel de distribuição mostra cada local registrado em nossa base de dados.",
    #                " Em conjunto, essa ferramenta é importante para o auxilio em identificar possíveis focos de introdução, áreas vulneráveis e tendências de expansão ao longo do território."
    #            ],
    #                style={
    #                    'color': Config.COLORS['text'],
    #                    'fontSize': '18px',
    #                    'textAlign': 'justify',
    #                    'marginBottom': '0'
    #                }
    #            )
    #        ],
    #            style={
    #                'backgroundColor': 'rgba(40, 44, 52, 0.86)',  # Cor de fundo levemente destacada
    #                'borderRadius': '10px',
    #                'border': '1px solid #375a7f',
    #                'padding': '25px 20px',
    #                'marginTop': '24px',
    #                'boxShadow': '0px 2px 8px rgba(0,0,0,0.12)'
    #            }
    #        )
    #    ], width=12)
    #]),
        
    # Linha adicional para controles (opcional)
    #dbc.Row([
    #    dbc.Col([
    #        html.H4('Filtros', style={'color': 'white'}),
    #        dcc.Dropdown(
    #            id='filtro-especies',
    #            placeholder='Selecione uma espécie...',
    #            style={'marginBottom': '20px'}
    #        )
    #    ], md=4),
    #    
    #    dbc.Col([
    #        html.H4('Período', style={'color': 'white'}),
    #        dcc.RangeSlider(
    #            id='slider-ano',
    #            min=1950,
    #            max=2025,
    #            step=1,
    #            value=[2000, 2025],
    #            marks={i: str(i) for i in range(1950, 2026, 10)}
    #        )
    #    ], md=8)
    #])
    #
    ], 
    fluid=True, 
    style={'padding': '20px'}
    )
