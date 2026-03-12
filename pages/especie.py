from dash import html
import dash_bootstrap_components as dbc
from config import Config

def get_especie_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2(
                    "Espécies por Ecossistemas", 
                    className="text-center mb-4", 
                    style={"fontWeight": "300"})
            ], width=12)
        ]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/terrestre_sp.jpeg",
                            alt="Ecossistema Terrestre",
                            style={
                                "width": "300px",
                                "height": "300px",
                                "objectFit": "cover",
                                "borderRadius": "12px",
                                "boxShadow": "0 2px 8px #222",
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto"
                            }
                        ),
                        html.H5("Ecossistema Terrestre", className="text-center mt-3")
                    ],
                    md=4, xs=12
                ),
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/aquatico_sp.jpeg",
                            alt="Ecossistema Aquático",
                            style={
                                "width": "300px",
                                "height": "300px",
                                "objectFit": "cover",
                                "borderRadius": "12px",
                                "boxShadow": "0 2px 8px #222",
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto"
                            }
                        ),
                        html.H5("Ecossistema Aquático", className="text-center mt-3")
                    ],
                    md=4, xs=12
                ),
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/marinho_sp.jpeg",
                            alt="Ecossistema Marinho",
                            style={
                                "width": "300px",
                                "height": "300px",
                                "objectFit": "cover",
                                "borderRadius": "12px",
                                "boxShadow": "0 2px 8px #222",
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto"
                            }
                        ),
                        html.H5("Ecossistema Marinho", className="text-center mt-3")
                    ],
                    md=4, xs=12
                ),
            ],
            className="justify-content-center g-5",
            style={"marginTop": "32px", "textAlign": "center"}
        ),
    ], fluid=True, style={"padding": "32px", "maxWidth": "1200px", "margin": "0 auto"})
