#"""
#Componente de Rodapé - Versão Simples
#"""
#from dash import html
#import dash_bootstrap_components as dbc
#from datetime import datetime
#
#def create_footer():
#    """Cria rodapé simples com direitos autorais"""
#    current_year = datetime.now().year
#    
#    return html.Footer([
#        dbc.Container([
#            html.Hr(style={'borderColor': 'rgba(255, 255, 255, 0.1)', 'margin': '60px 0 30px 0'}),
#            
#            dbc.Row([
#                dbc.Col([
#                    html.P([
#                        html.Strong("Desenvolvido por: "),
#                        "Dr. Nome Autor 1, Dr. Nome Autor 2, Dr. Nome Autor 3"
#                    ], className="text-center", style={'marginBottom': '10px'})
#                ], width=12)
#            ]),
#            
#            dbc.Row([
#                dbc.Col([
#                    html.P(
#                        f"© {current_year} Observatório Paranaense de Espécies Exóticas. Todos os direitos reservados.",
#                        className="text-center mb-0",
#                        style={'color': '#CCCCCC', 'fontSize': '14px'}
#                    )
#                ], width=12)
#            ])
#            
#        ], fluid=True, style={'maxWidth': '1200px'})
#    ], style={
#        'backgroundColor': '#2C3E50',
#        'color': '#FFFFFF',
#        'padding': '30px 0',
#        'marginTop': '40px'
#    })

"""
Componente de Rodapé
"""
from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime

def create_footer():
    """Cria rodapé com direitos autorais e autores"""
    current_year = datetime.now().year
    
    return html.Footer([
        dbc.Container([
            html.Hr(style={'borderColor': 'rgba(255, 255, 255, 0.1)', 'margin': '40px 0 30px 0'}),
            
            # Informações dos Autores
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H5("Desenvolvido por:", className="mb-3", style={'fontWeight': '600'}),
                        html.P(
                            [
                                html.Strong("Dr.José Ricardo Pires Adelino"),
                                html.Br(),
                                "Universidade Federal do Paraná - UFPR",
                                html.Br(),
                                html.A("ricaro.pires@ufpr.br", href="mailto:ricardo.pires@ufpr.br", 
                                style={'color': '#bddd3d', 'textDecoration': 'none'})
                            ], 
                                style={'marginBottom': '15px'}
                            ),
                        html.P(
                            [
                                html.Strong("Dr. Marcos Robalinho Lima"),
                                html.Br(),
                                "Universidade Estadual de Londrina",
                                html.Br(),
                                html.A("robalinho@uel.br", href="mailto:robalinho@uel.br", 
                                style={'color': "#bddd3d", 'textDecoration': 'none'})
                            ]
                            ),
                        html.P(
                            [
                                html.Strong("Dr. André Andrian Padial"),
                                    html.Br(),
                                    "Universidade Estadual de Londrina",
                                    html.Br(),
                                    html.A("aapadial@gmail.br", href="mailto:aapadial@gmail.br", 
                                    style={'color': '#bddd3d', 'textDecoration': 'none'})
                            ]
                            )
                    ])
                ], md=4),
                
                # Informações do Projeto
                dbc.Col([
                    html.Div([
                        html.H5("Sobre o Projeto:", className="mb-3", style={'fontWeight': '600'}),
                        html.P([
                            "Observatório Paranaense de Espécies Exóticas",
                            html.Br(),
                            "Uma iniciativa para monitoramento e gestão de espécies exóticas no Paraná"
                        ], style={'lineHeight': '1.6'}),
                        html.Div([
                            html.A([html.I(className="fab fa-github"), " GitHub"], 
                                  href="https://github.com/seu-projeto", 
                                  target="_blank",
                                  className="me-3",
                                  style={'color': '#bddd3d', 'textDecoration': 'none'}),
                            html.A([html.I(className="fas fa-envelope"), " Contato"], 
                                  href="mailto:contato@projeto.br",
                                  style={'color': '#bddd3d', 'textDecoration': 'none'})
                        ])
                    ])
                ], md=4),
                
                # Licença e Copyright
                dbc.Col([
                    html.Div([
                        html.H5("Licença:", className="mb-3", style={'fontWeight': '600'}),
                        html.P([
                            "© ", str(current_year), " Observatório Paranaense",
                            html.Br(),
                            "Todos os direitos reservados"
                        ], style={'marginBottom': '15px'}),
                        html.P([
                            html.Small([
                                "Licenciado sob ",
                                html.A("MIT License", 
                                      href="https://opensource.org/licenses/MIT",
                                      target="_blank",
                                      style={'color': '#bddd3d'})
                            ])
                        ])
                    ])
                ], md=4)
            ], className="mb-4"),
            
            # Copyright centralizado
            html.Div([
                html.Hr(style={'borderColor': 'rgba(255, 255, 255, 0.1)', 'margin': '20px 0'}),
                html.P(
                    f"© {current_year} Observatório Paranaense de Espécies Exóticas. Desenvolvido com Python & Dash.",
                    className="text-center mb-0",
                    style={'color': '#CCCCCC', 'fontSize': '14px'}
                )
            ])
            
        ], fluid=True, style={'maxWidth': '1200px'})
    ], style={
        'backgroundColor': '#2C3E50',
        'color': '#FFFFFF',
        'padding': '20px 0 30px 0',
        'marginTop': '60px'
    })
