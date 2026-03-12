"""
Componente de Barra de Navegação
"""
import dash_bootstrap_components as dbc
from dash import html

def create_navbar():
    """Cria a barra de navegação principal - Idêntica ao original"""
    return dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand(
                html.Div([
                    html.Span("Observatório de", style={'fontWeight': '300'}),
                    html.Span(" Espécies Exóticas", style={'fontWeight': '600', 'color': '#bddd3d'})#375a7f
                ]),
                href="/",
                className="me-4"
            ),
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Início", href="/", active="exact")),
                dbc.NavItem(dbc.NavLink("Gráficos", href="/graficos")),
                dbc.NavItem(dbc.NavLink("Ocorrencia", href="/ocorrencia")),
                dbc.NavItem(dbc.NavLink("Indicador", href="/indicador")),
                #dbc.NavItem(dbc.NavLink("Mapas", href="/mapas")),
                dbc.NavItem(dbc.NavLink("Modelos", href="/modelos")),
                dbc.NavItem(dbc.NavLink("Espécies", href="/especies")), 
                dbc.NavItem(dbc.NavLink("Equipe", href="/equipe"))
            ], navbar=True)
        ]),
        color="dark",
        dark=True,
        sticky="top",
        className="shadow"
    )
