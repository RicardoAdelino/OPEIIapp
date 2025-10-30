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
from pages.mapas import get_mapa_layout

# Importar callbacks
from callbacks.mapa_callbacks import register_mapa_callbacks

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
    html.Div(id='page-content')
])

# Callback de roteamento
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    """Gerencia roteamento entre páginas"""
    if pathname == '/formulario':
        return html.Div([
            dbc.Container([
                html.H2("Formulário de Registro", className="my-4"),
                html.P("Em desenvolvimento...")
            ])
        ])
    elif pathname == '/graficos':
        return html.Div([
            dbc.Container([
                html.H2("Análises Gráficas", className="my-4"),
                html.P("Em desenvolvimento...")
            ])
        ])
    elif pathname == '/mapas':
        return get_mapa_layout()
    elif pathname == '/especies':
        return html.Div([
            dbc.Container([
                html.H2("Catálogo de Espécies", className="my-4"),
                html.P("Em desenvolvimento...")
            ])
        ])
    elif pathname == '/equipe':
        return html.Div([
            dbc.Container([
                html.H2("Equipe de Colaboradores", className="my-4"),
                html.P("Em desenvolvimento...")
            ])
        ])
    else:
        return get_home_layout()

# Registrar callbacks das páginas
register_mapa_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, port=8050)
