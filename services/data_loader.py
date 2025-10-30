"""
Serviço de Carregamento de Dados
Implementa padrão Singleton para cache eficiente
"""
import pandas as pd
import geopandas as gpd
from config import Config

class DataLoader:
    _instance = None
    _data_cache = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
        return cls._instance
    
    def load_habitat_data(self):
        """Carrega e cacheia dados de habitat"""
        if 'habitat' not in self._data_cache:
            df = pd.read_csv(Config.HABITAT_CSV)
            df = df.drop(df.columns[0], axis=1)
            self._data_cache['habitat'] = df
        return self._data_cache['habitat']
    
    def load_meta_map_data(self):
        """Carrega dados meta do mapa"""
        if 'meta_map' not in self._data_cache:
            df = pd.read_csv(Config.META_MAP_CSV)
            self._data_cache['meta_map'] = df
        return self._data_cache['meta_map']
    
    def load_pr_geojson(self):
        """Carrega GeoJSON do Paraná"""
        if 'pr_geojson' not in self._data_cache:
            mapa = gpd.read_file(Config.PR_GEOJSON)
            mapa = mapa.to_crs(epsg=4326)
            mapa['id'] = mapa.index + 1
            mapa = mapa.reindex(
                columns=['id', 'code_muni', 'name_muni', 
                        'code_state', 'abbrev_state', 'geometry']
            )
            self._data_cache['pr_geojson'] = mapa
        return self._data_cache['pr_geojson']
    
    def load_vul_min_geojson(self):
        """Carrega GeoJSON de vulnerabilidade"""
        if 'vul_min' not in self._data_cache:
            mapa_meta = gpd.read_file(Config.VUL_MIN_GEOJSON)
            mapa_meta = mapa_meta.to_crs(epsg=4326)
            df_mapa = pd.DataFrame(mapa_meta)
            df_mapa = df_mapa.drop(
                columns=['geometry', 'code_muni', 'code_state']
            )
            df_mapa = df_mapa[['name_muni', 'quantile_class']]
            self._data_cache['vul_min'] = df_mapa
        return self._data_cache['vul_min']
    
    def get_habitat_list(self):
        """Retorna lista de habitats únicos"""
        df = self.load_habitat_data()
        return df['habitat'].unique()

