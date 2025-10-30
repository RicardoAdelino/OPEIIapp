"""
Serviço de Processamento de Dados
Responsável por transformações e agregações
"""
import pandas as pd
from services.data_loader import DataLoader

class DataProcessor:
    def __init__(self):
        self.loader = DataLoader()
    
    def get_merged_meta_data(self):
        """Mescla dados meta com dados do mapa"""
        df_meta = self.loader.load_meta_map_data()
        df_mapa = self.loader.load_vul_min_geojson()
        meta_ = df_meta.merge(df_mapa, on='name_muni', how='left')
        return meta_
    
    def get_top_municipalities(self, habitat, top_n=20):
        """Retorna top N municípios por habitat"""
        meta_ = self.get_merged_meta_data()
        bar_data = meta_[['name_muni', habitat]]
        bar_ = bar_data[bar_data[habitat] > 0]
        bar_ = bar_.nlargest(top_n, habitat)
        bar_ = bar_.rename(
            columns={
                'name_muni': 'Município',
                str(habitat): 'Quantidade'
            }
        )
        return bar_
    
    def get_habitat_data_for_map(self, habitat):
        """Prepara dados de habitat para visualização no mapa"""
        df = self.loader.load_habitat_data()
        df_habitat = df[df['habitat'] == habitat]
        return df_habitat

