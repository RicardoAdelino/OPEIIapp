import pandas as pd
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from services.data_loader import DataLoader

class_mapping = {
    0: "Atenção",
    1: "Preocupante",
    2: "Vulnerável",
    3: "Muito Vulnerável"
}

class_colors = {
    "Muito Vulnerável": "#e41a1c",
    "Vulnerável": "#ff7f00",
    "Preocupante": "#4daf4a",
    "Atenção": "#377eb8"
}

class RasterService:
    def __init__(self):
        self.data_loader = DataLoader()

    def process_raster_group(self, raster_a_path, raster_b_path):
        gdf = self.data_loader.load_pr_geojson()
        data_list = []
        with rasterio.open(raster_a_path) as src_a, rasterio.open(raster_b_path) as src_b:
            raster_a = src_a.read(1)
            raster_b = src_b.read(1)
            nodata_a = src_a.nodata
            nodata_b = src_b.nodata
            for idx, row in gdf.iterrows():
                geom = [row.geometry]
                mask_array = geometry_mask(
                    geom,
                    out_shape=raster_a.shape,
                    transform=src_a.transform,
                    invert=True
                )
                rows, cols = np.where(mask_array)
                for r, c in zip(rows, cols):
                    value_a = raster_a[r, c]
                    value_b = raster_b[r, c]
                    is_valid_a = not (np.isnan(value_a) or (nodata_a is not None and value_a == nodata_a))
                    is_valid_b = not (np.isnan(value_b) or (nodata_b is not None and value_b == nodata_b))
                    if is_valid_a and is_valid_b and int(value_a) in class_mapping:
                        x, y = rasterio.transform.xy(src_a.transform, r, c)
                        data_list.append({
                            'name_muni': row['name_muni'],
                            'x_coord': x,
                            'y_coord': y,
                            'value_a_class': class_mapping[int(value_a)],
                            'value_b': value_b
                        })
        return pd.DataFrame(data_list)
