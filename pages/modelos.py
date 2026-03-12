from dash import html,dcc
import dash_bootstrap_components as dbc
from config import Config

#def get_modelo_layout():
#    return dbc.Container([
#        dbc.Row([
#            dbc.Col([
#                html.H2(
#                    "Espécies por Ecossistemas", 
#                    className="text-center mb-4", 
#                    style={"fontWeight": "300"})
#            ], width=12)
#        ]),
#        dbc.Row(
#            [
#                dbc.Col(
#                    [
#                        html.Img(
#                            src="/assets/terrestre_sp.jpeg",
#                            alt="Ecossistema Terrestre",
#                            style={
#                                "width": "300px",
#                                "height": "300px",
#                                "objectFit": "cover",
#                                "borderRadius": "12px",
#                                "boxShadow": "0 2px 8px #222",
#                                "display": "block",
#                                "marginLeft": "auto",
#                                "marginRight": "auto"
#                            }
#                        ),
#                        html.H5("Ecossistema Terrestre", className="text-center mt-3")
#                    ],
#                    md=4, xs=12
#                ),
#                dbc.Col(
#                    [
#                        html.Img(
#                            src="/assets/aquatico_sp.jpeg",
#                            alt="Ecossistema Aquático",
#                            style={
#                                "width": "300px",
#                                "height": "300px",
#                                "objectFit": "cover",
#                                "borderRadius": "12px",
#                                "boxShadow": "0 2px 8px #222",
#                                "display": "block",
#                                "marginLeft": "auto",
#                                "marginRight": "auto"
#                            }
#                        ),
#                        html.H5("Ecossistema Aquático", className="text-center mt-3")
#                    ],
#                    md=4, xs=12
#                ),
#                dbc.Col(
#                    [
#                        html.Img(
#                            src="/assets/marinho_sp.jpeg",
#                            alt="Ecossistema Marinho",
#                            style={
#                                "width": "300px",
#                                "height": "300px",
#                                "objectFit": "cover",
#                                "borderRadius": "12px",
#                                "boxShadow": "0 2px 8px #222",
#                                "display": "block",
#                                "marginLeft": "auto",
#                                "marginRight": "auto"
#                            }
#                        ),
#                        html.H5("Ecossistema Marinho", className="text-center mt-3")
#                    ],
#                    md=4, xs=12
#                ),
#            ],
#            className="justify-content-center g-5",
#            style={"marginTop": "32px", "textAlign": "center"}
#        ),
#    ], fluid=True, style={"padding": "32px", "maxWidth": "1200px", "margin": "0 auto"})

def get_modelo_layout():
    return html.Div(
        [
            dbc.Container(
                [
                    _create_modelo_header(),
                    html.Div(
                        [
                            html.H5(
                                "Selecione um grupo", 
                                className="mb-2",
                                style={
                                    'color': 'white', 
                                    'textAlign': 'center'
                                    }
                                ),       
                    dcc.Dropdown(
                        id = 'raster-group-dropdown',
                        options = [
                            {'label': 'Vertebrados Terrestres', 'value': 'Vert_ter'},
                            {'label': 'Plantas Terrestres', 'value': 'Plant_ter'}
                        ],
                        value='Vert_ter',  # Valor padrão
                        placeholder = "Selecione a categoria de interesse",
                        className='custom-dropdown',   # chave para CSS consistente
                        style={'width': '100%', 'maxWidth': '350px', 'margin': '0 auto','textAlign': 'center'}
                        #value=[],
                            ),
                        ], 
                    style={'marginBottom': '20px'}
                ),
                # ADICIONE ESTE COMPONENTE:
            dcc.Graph(
                id='modelos-map',
                style={'height': '700px'}
            )
            ]
        )
    ]
)

def _create_modelo_header():
    """Cria cabeçalho da página"""
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.H3(
                    "Acompanhe as previsões de modelos estatísticas para o acúmulo de espécies",
                    className="text-center mb-4",
                    style={
                        'color': Config.COLORS['text'], 
                        'fontWeight': '300'}
                ),
                #html.H4(
                #    "Nossos modelos foram calibrados para identificar regiões favoráveis a persistência de populações ecologicamente viáveis de espécies não nativas. Ao combinar informações relevantes de condições ambientais, nossa previsões ajudam a inferir padrões espacias de dispersão das espécies e auxiliam gestores a priorizar áreas de monitoramento intensivo",
                #    className="text-center mb-4",
                #    style={
                #        'color': Config.COLORS['text'], 
                #        'fontWeight': '180'}
                #),
                dcc.Markdown([
                    """
                        Nossos modelos foram calibrados para identificar regiões favoráveis a 
                        persistência de populações ecologicamente viáveis de espécies não nativas. 
                        Ao combinar informações relevantes de condições ambientais, nossa previsões 
                        ajudam a inferir padrões espacias de dispersão das espécies e auxiliam gestores 
                        a priorizar áreas de monitoramento intensivo
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