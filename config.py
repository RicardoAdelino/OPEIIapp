"""
Configurações Globais da Aplicação
"""
import os

class Config:
    # Configurações do Dash
    SUPPRESS_CALLBACK_EXCEPTIONS = True
    
    # Caminhos de dados
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'raw')
    
    # Arquivos de dados
    HABITAT_CSV = os.path.join(DATA_DIR, 'habitat_long_meta.csv')
    META_MAP_CSV = os.path.join(DATA_DIR, 'meta_map.csv')
    PR_GEOJSON = os.path.join(DATA_DIR, 'pr.geojson')
    VUL_MIN_GEOJSON = os.path.join(DATA_DIR, 'vul_min.geojson')
    
    # Configurações do Mapa
    MAP_CENTER = {'lat': -24.845946, 'lon': -51.557551}
    MAP_ZOOM = 5.4
    
    # Tema e estilos
    THEME = 'DARKLY'
    MAPBOX_STYLE = 'carto-darkmatter'
    
    # Cores
    COLORS = {
        'primary': '#375a7f',
        'secondary': '#2C3E50', ##2C3E50
        'background': 'rgba(0,0,0,0)',
        'text': '#FFFFFF',
        'text_secondary': '#CCCCCC'
    }

