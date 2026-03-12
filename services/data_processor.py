"""
Serviço de Processamento de Dados
Responsável por transformações e agregações
"""
import pandas as pd
import geopandas as gpd
import numpy as np
from services.data_loader import DataLoader
from config import Config
import rasterio
from rasterio.features import geometry_mask

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
    
    #Adiciona novo processamento de dados
    def get_oco_data_for_ts(self):
        """Retorna dados processados para grafico de linhas"""
        oc = self.loader.load_oco_data()
        # Contar o número de linhas por categoria
        oc = oc.groupby('ano_final').size()
        oc = oc.rename('n_obs').reset_index()
        #n_ano = n_ano[n_ano['ano_final'] > 1950]
        oc['acc_'] = oc['n_obs'].cumsum()
        return oc
    
    #  Exemplo: função que retorna IDs direto da planilha original
    def get_ids(self):
        """Retorna lista do menu drop"""
        oc = self.loader.load_oco_data()
        ids = oc['ID'].unique()
        ids = [{'label': str(ID), 'value': ID} for ID in ids]
        # Retorne lista de dicionários para opções do dropdown
        return ids
    
    # Adiciona dados para mapas de distribuição e densidade
    def get_oco_data_for_map(self):
        """Prepara dados de ocorrência para visualização em mapas"""
        oc = self.loader.load_oco_data()
        # Unificar a geometria do gdf
        pr = self.loader.load_pr_geojson()
        #boundary = pr.geometry.unary_union # ETAPA QUE DEVE SER REMOVIDA APOS AJUSTE DA PLANILHA INICIAL
        # Remover localidades fora do gdf
        #points_inside = oc[oc.geometry.within(boundary)]      
        # Transformar points_inside em GeoDataFrame com geometria de ponto
        #gdf_points = gpd.GeoDataFrame(
        #    points_inside,
        #    geometry=gpd.points_from_xy(points_inside['long_dec'], points_inside['lat_dec']),
        #    crs='EPSG:4326'
        #)
        gdf_points = gpd.GeoDataFrame(
            oc,
            geometry=gpd.points_from_xy(oc['long_dec'], oc['lat_dec']),
            crs='EPSG:4326'
        )
        # Extrair coordenadas para o KDE
        coords = np.vstack([oc['lat_dec'], oc['long_dec']])
        #kde = gaussian_kde(coords)

        # Calcular valor do KDE para cada ponto individual
        #gdf_points['density_kde'] = np.round(kde(coords).flatten(), 6)  # KDE para cada ponto

        # Associar municipio (nome do polígono) para cada ponto
        points_with_poly = gpd.sjoin(gdf_points, pr[['geometry', 'name_muni']], how='left', predicate='within')

        # Contar pontos por polígono
        n_oc = points_with_poly.groupby('name_muni').size().reset_index(name='Ocorrencia')

        # Adicionar o valor da densidade a cada ponto associado ao polígono
        points_with_poly = points_with_poly.merge(
            n_oc, on='name_muni', how='left'
        )

        points_with_poly.rename(
            columns={
                'name_muni': 'Municipio', 
                'density_kde': 'Densidade', 
                'lat_dec':'Latitude',
                'long_dec':'Longitude'},
            inplace=True
        )
        return points_with_poly
    
    def get_pr_geometry(self):
        pr = self.loader.load_pr_geojson()
        return pr
    
    def get_raster_data(self):
        """Retorna um dicionário com grupos de dados de rasters"""
        gdf = self.loader.load_pr_geojson()
    
        # MAPEAMENTO PERSONALIZADO DAS CLASSES
        class_mapping = {
            0: "Atenção",
            1: "Preocupante", 
            2: "Vulnerável",
            3: "Muito Vulnerável"
        }

        # Configuração dos grupos de rasters
        raster_groups = {
            'Vert_ter': {
                'raster_a': Config.VERT_TER_CL,
                'raster_b': Config.VERT_TER_CP,
                'label_b': 'Pressão colonização (Vert)'
            },
            'Plant_ter': {
                'raster_a': Config.PLANT_TER_CL,  # Adicione o caminho correto no Config
                'raster_b': Config.PLANT_TER_CP,  # Adicione o caminho correto no Config
                'label_b': 'Pressão colonização (Plant)'
            }
        }

        # Dicionário para armazenar os DataFrames de cada grupo
        grouped_data = {}

        # Processar cada grupo de rasters
        for group_name, paths in raster_groups.items():
            data_list = []

            # Abrir os dois arquivos raster do grupo
            with rasterio.open(paths['raster_a']) as src_a, \
                 rasterio.open(paths['raster_b']) as src_b:

                # Ler as bandas dos rasters
                raster_a = src_a.read(1)
                raster_b = src_b.read(1)

                # Obter valores nodata
                nodata_a = src_a.nodata
                nodata_b = src_b.nodata

                # Verificar classes presentes no raster
                mask_valid = ~np.isnan(raster_a)
                if nodata_a is not None:
                    mask_valid = mask_valid & (raster_a != nodata_a)

                # Para cada polígono
                for idx, row in gdf.iterrows():
                    # Criar máscara para este polígono
                    geom = [row.geometry]
                    mask_array = geometry_mask(
                        geom, 
                        out_shape=raster_a.shape,
                        transform=src_a.transform,
                        invert=True
                    )

                    # Encontrar células dentro do polígono
                    rows, cols = np.where(mask_array)

                    # Extrair valores e coordenadas de ambos os rasters
                    for r, c in zip(rows, cols):
                        value_a = raster_a[r, c]
                        value_b = raster_b[r, c]

                        # Filtrar NaN e valores nodata
                        is_valid_a = not (np.isnan(value_a) or 
                                         (nodata_a is not None and value_a == nodata_a))
                        is_valid_b = not (np.isnan(value_b) or 
                                         (nodata_b is not None and value_b == nodata_b))

                        # Verificar se o valor_a está no mapeamento de classes
                        if is_valid_a and is_valid_b and int(value_a) in class_mapping:
                            x, y = rasterio.transform.xy(src_a.transform, r, c)

                            data_list.append({
                                'name_muni': row['name_muni'],
                                'polygon_id': idx,
                                'cell_row': r,
                                'cell_col': c,
                                'x_coord': x,
                                'y_coord': y,
                                'value_a_numeric': value_a,
                                'value_a_class': class_mapping[int(value_a)],
                                'value_b': value_b,
                                'label_b': paths['label_b']
                            })

            # Criar DataFrame para este grupo
            grouped_data[group_name] = pd.DataFrame(data_list)

        return grouped_data


# Prepara dados para o raster
# def get_raster_data(self):
#     gdf = self.loader.load_pr_geojson()
#     
#     # MAPEAMENTO PERSONALIZADO DAS CLASSES
#     class_mapping = {
#         0: "Atenção",
#         1: "Preocupante", 
#         2: "Vulnerável",
#         3: "Muito Vulnerável"
#     }
#     
#     # Definir cores para cada classe
#     class_colors = {
#         "Muito Vulnerável": "#e41a1c",
#         "Vulnerável": "#ff7f00",
#         "Preocupante": "#4daf4a",
#         "Atenção": "#377eb8"    
#     }
#   
#     # Lista para armazenar os dados
#     data_list = []
#     
#     # Carrega raster
#     # Abrir os dois arquivos raster
#     with rasterio.open(Config.VERT_TER_CL) as src_a, rasterio.open(Config.VERT_TER_CP) as src_b:
#         # Ler as bandas dos rasters
#         raster_a = src_a.read(1)
#         raster_b = src_b.read(1)
#     # Obter valores nodata (se existirem)
#         nodata_a = src_a.nodata
#         nodata_b = src_b.nodata
#         # Verificar classes presentes no raster
#         mask_valid = ~np.isnan(raster_a)
#         if nodata_a is not None:
#             mask_valid = mask_valid & (raster_a != nodata_a)
#             unique_classes = np.unique(raster_a[mask_valid])
#         # Para cada polígono
#         for idx, row in gdf.iterrows():
#             # Criar máscara para este polígono
#             geom = [row.geometry]
#             mask_array = geometry_mask(geom, 
#                                        out_shape=raster_a.shape,
#                                        transform=src_a.transform,
#                                        invert=True)
#             # Encontrar células dentro do polígono
#             rows, cols = np.where(mask_array)
#             # Extrair valores e coordenadas de ambos os rasters
#             for r, c in zip(rows, cols):
#                 value_a = raster_a[r, c]
#                 value_b = raster_b[r, c]
#                 # Filtrar NaN e valores nodata
#                 is_valid_a = not (np.isnan(value_a) or (nodata_a is not None and value_a == nodata_a))
#                 is_valid_b = not (np.isnan(value_b) or (nodata_b is not None and value_b == nodata_b))
#                 # Verificar se o valor_a está no mapeamento de classes
#                 if is_valid_a and is_valid_b and int(value_a) in class_mapping:
#                     x, y = rasterio.transform.xy(src_a.transform, r, c)
#                     data_list.append({
#                         'name_muni': row['name_muni'],
#                         'polygon_id': idx,
#                         'cell_row': r,
#                         'cell_col': c,
#                         'x_coord': x,
#                         'y_coord': y,
#                         'value_a_numeric': value_a,
#                         'value_a_class': class_mapping[int(value_a)],
#                         'value_b': value_b
#                     })
#     # Criar DataFrame
#     df_combined = pd.DataFrame(data_list)
#     return df_combined

   