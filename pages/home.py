"""
Página Home da Aplicação
"""
from dash import html
import dash_bootstrap_components as dbc
from components.cards import create_info_card, create_stat_card
from config import Config
from components.footer import create_footer

def get_home_layout():
    """Retorna layout da página inicial"""
    return html.Div(
        [
        dbc.Container(
            [
            # Hero Section
            _create_hero_section(),
            
            # Cards de Funcionalidades
            _create_feature_cards(),
            
            # Sobre o Observatório
            _create_about_section(),
            
            # Estatísticas
            _create_stats_section()            
            ], 
        fluid=True, 
        style={'maxWidth': '1200px'}
        ),
        create_footer()
    ], 
    style={'minHeight': '100vh', 'padding': '20px 0'})

def _create_hero_section():
    """
        Cria seção hero: Seção de primeiro contato com a plataforma
        importante para gerar primeira impressão com contéudo
    """
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.H1(
                    "Observatório Paranaense de Espécies Exóticas",
                    className="display-4 mb-4",
                    style={'color': Config.COLORS['text'], 'fontWeight': '300'}
                ),
                html.P(
                    "Uma plataforma integrada para monitoramento, análise e gestão de espécies exóticas no estado do Paraná",
                    className="lead mb-4",
                    style={'color': Config.COLORS['text_secondary'], 'fontSize': '25px'}
                ),
                html.Hr(style={'borderColor': Config.COLORS['primary'], 'width': '100px', 'margin': '30px 0'})
            ], className="text-center", style={'padding': '80px 0'})
        ])
    ])

def _create_feature_cards():
    """Cria cards de funcionalidades"""
    features = [
        {
            'title': 'Análises Gráficas',
            'description': 'Visualizações interativas e análises descritivas dos dados de espécies exóticas.',
            'button': 'Explorar Gráficos',
            'href': '/graficos',
            'icon': '📊'
        },
        {
            'title': 'Mapas Interativos',
            'description': 'Distribuição espacial e mapeamento territorial das espécies.',
            'button': 'Ver Mapas',
            'href': '/mapas',
            'icon': '🗺️'
        },
        {
            'title': 'Registro de Dados',
            'description': 'Formulários para cadastro e atualização de informações das espécies exóticas.',
            'button': 'Acessar Formulário',
            'href': '/formulario',
            'icon': '📝'
        },
        {
            'title': 'Espécies',
            'description': 'Banco de dados completo com informações detalhadas sobre cada espécie.',
            'button': 'Consultar Espécies',
            'href': '/especies',
            'icon': '🔍'
        }
    ]
    
    return dbc.Row([
        dbc.Col([
            create_info_card(
                f['title'], 
                f['description'], 
                f['button'], 
                f['href'], 
                f['icon']
            )
        ], md=3, className="mb-4")
        for f in features
    ])

def _create_about_section():
    """Cria seção sobre"""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2("Sobre o Observatório", className="mb-4"),
                    html.P("""
                        O Observatório Paranaense de Espécies Exóticas é uma iniciativa dedicada 
                        ao monitoramento e estudo de espécies exóticas no estado do Paraná.
                    """, style={'lineHeight': '1.6', 'fontSize': '16px'}),
                    dbc.Row([
                        dbc.Col([
                            html.H5("🎯 Missão"),
                            html.P("Promover o conhecimento e gestão adequada de espécies exóticas no Paraná.")
                        ], md=4),
                        dbc.Col([
                            html.H5("👁️ Visão"),
                            html.P("Ser referência em monitoramento e pesquisa de espécies exóticas no Brasil.")
                        ], md=4),
                        dbc.Col([
                            html.H5("🤝 Valores"),
                            html.P("Transparência, precisão científica e acessibilidade da informação.")
                        ], md=4)
                    ], className="mt-4")
                ])
            ], className="shadow mt-5", 
               style={'backgroundColor': Config.COLORS['secondary'], 'border': 'none'})
        ])
    ])

def _create_stats_section():
    """Cria seção de estatísticas"""
    stats = [
        {'value': '400+', 'label': 'Espécies Catalogadas'},
        {'value': '399', 'label': 'Municípios Monitorados'},
        {'value': '8K+', 'label': 'Ocorrências Mapeadas'},
        {'value': '2024', 'label': 'Dados Atualizados'}
    ]
    
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("Dados em Números", className="text-center mb-5"),
                dbc.Row([
                    dbc.Col([create_stat_card(s['value'], s['label'])], md=3)
                    for s in stats
                ])
            ], style={'padding': '60px 0'})
        ])
    ])

