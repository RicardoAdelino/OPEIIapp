"""
Aplicação Principal do Dashboard
Observatório Paranaense de Espécies Exóticas
"""
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from config import Config

# Importar componentes
from components.navbar import create_navbar

# Importar páginas
from pages.home import get_home_layout
#from pages.mapas import get_mapa_layout
from pages.chart_line import get_chart_layout
from pages.ocorrencia import get_ocorrencia_layout
from pages.modelos import get_modelo_layout
from pages.especie import get_especie_layout
from pages.indicador import get_indicator_layout

# Importar callbacks
#from callbacks.mapa_callbacks import register_mapa_callbacks
from callbacks.indicador_callbacks import register_mapa_callbacks
from callbacks.chart_callbacks import register_line_callbacks
from callbacks.ocorrencia_callbacks import register_ocorrencia_callbacks 
from callbacks.modelo_callbacks import register_modelos_callbacks

# Inicializar aplicação
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=Config.SUPPRESS_CALLBACK_EXCEPTIONS
)

# Criar navbar uma única vez
navegacao = create_navbar()

# Layout principal com roteamento
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navegacao,  # Navbar sempre presente
    html.Div(id='page-content'),
])

# Callback de roteamento
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """Gerencia roteamento entre páginas"""
    if pathname == '/ocorrencia':
        return get_ocorrencia_layout()
    #html.Div([
    #        dbc.Container([
    #            html.H2("Formulário de Registro", className="my-4"),
    #            html.P("Em desenvolvimento...")
    #        ])
    #    ])
    elif pathname == '/graficos':
        return get_chart_layout()
    #elif pathname == '/mapas':
    #    return get_mapa_layout()
    elif pathname =='/indicador':
        return get_indicator_layout()
    elif pathname == '/modelos':
       return get_modelo_layout()
    elif pathname == '/especies':
        return get_especie_layout()
    elif pathname == '/equipe':
        return html.Div(
            [
                dbc.Container(
                    [
                        html.H2(
                            "Equipe e Colaboradores", 
                            className="my-4", 
                            style={'textAlign': 'center'}
                        ),
                        # Layout com Row e Cols para dividir esquerda/direita
                        dbc.Row(
                            [
                                # Coluna da esquerda - Conteúdo texto
                                dbc.Col(
                                    dcc.Markdown(
                                        '''
                                            ### Desenvolvedores                    

                                            José Ricardo Pires Adelino • UFPR - UEL 

                                            André Andrian Padial • UFPR 

                                            Marcos Robalinho Lima • UEL   

                                            ### Pesquisadores colaboradores

                                            Aline Rosado • UEM 

                                            Éder André Gubiani • UNIOESTE 

                                            Fernando Jerep • UEL

                                            Kazue Kawakita • UEM 

                                            Pitágoras Augusto Piana • UNIOESTE 

                                            Roger Mormul • UEM 

                                            Sidinei Magela Thomaz • UEM 

                                            ### Laboratórios colaboradores

                                            [Laboratório de Ecologia e Conservação LEC](https://www.lecufpr.net) -  UFPR Litoral 

                                            [Laboratório de Análise e Síntese da Biodiversidade LASB](https://lasbufprbio.wixsite.com/home) - UFPR, Curitiba

                                            [Laboratório de Ecologia Evolução e Conservação - EECon](https://sites.google.com/view/eeconlab-uel/home?authuser=0) - UEL, Londrina                                                               
                                        '''
                                    ),
                                    width = 8,
                                    md = 4,  # 4 colunas em telas médias/grandes
                                    className="mb-4"
                                ),
                                # Coluna da direita - 4 imagens
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Img(
                                                    src="/assets/ufpr_logo.png",
                                                    style={
                                                        'width': '100%',
                                                        'maxWidth': '300px',  # Limita tamanho máximo
                                                        'marginBottom': '15px',
                                                        'borderRadius': '8px',
                                                        'border': 'transparent'
                                                    }
                                                ),
                                                html.Img(
                                                    src="/assets/uel_logo.png",
                                                    style={
                                                        'width': '100%',
                                                        'maxWidth': '300px',  # Limita tamanho máximo
                                                        'marginBottom': '15px',
                                                        'borderRadius': '8px',
                                                        'border': 'transparent'
                                                    }
                                                ),
                                                html.Img(
                                                    src="/assets/se_logo.png",
                                                    style={
                                                        'width': '100%',
                                                        'maxWidth': '300px',  # Limita tamanho máximo
                                                        'marginBottom': '15px',
                                                        'borderRadius': '8px',
                                                        'border': 'transparent'
                                                    }
                                                ),
                                                html.Img(
                                                    src="/assets/fa_logo.png",
                                                    style={
                                                        'width': '100%',
                                                        'maxWidth': '300px',  # Limita tamanho máximo
                                                        'borderRadius': '8px',
                                                        'border': 'transparent'
                                                    }
                                                ),
                                            ],
                                            style={
                                                'display': 'flex',
                                                'flexDirection': 'column',
                                                'position': 'sticky',
                                                'top': '20px'  # Fixo ao rolar
                                            }
                                        )
                                    ],
                                    width=10,
                                    md=2,  # 2 colunas em telas médias/grandes
                                ),
                            ],
                            className="g-4", 
                            justify="center"  # Centraliza as colunas
                        )
                    ],
                    fluid=True
                )
            ]
        )
    else:
        return get_home_layout()

# Registrar callbacks das páginas
register_mapa_callbacks(app)
register_line_callbacks(app)
register_ocorrencia_callbacks(app)
register_modelos_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, port=8050)
