"""
Componentes de Card Reutilizáveis
"""
import dash_bootstrap_components as dbc
from dash import html
from config import Config

def create_info_card(title, description, button_text, href, icon="📊"):
    """Cria um card informativo padrão"""
    return dbc.Card([
        dbc.CardBody([
            html.H4(f"{icon} {title}", className="card-title mb-3"),
            html.P(description),
            dbc.Button(
                button_text, 
                href=href, 
                color="info", #"success" "info", "warning" "primary"
                outline=True
            )
        ], 
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'height': '100%',
            'justifyContent': 'space-between', 
            'alignItems': 'center',
            'textAlign': 'center'
            }
        )
    ], className="h-100 shadow", 
       style={'backgroundColor': Config.COLORS['secondary'], 'border': 'none'})

def create_stat_card(value, label):
    """Cria um card de estatística"""
    return html.Div([
        html.H2(value, style={'color': Config.COLORS['primary'], 'fontWeight': 'bold'}),
        html.P(label)
    ], className="text-center")

