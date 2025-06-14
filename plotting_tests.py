#%%
import os
import exifread
import pandas as pd

import plotly.express as px

def plot_gps_heatmap(df):
    fig = px.density_mapbox(df, lat='lat', lon='lon', radius=10,
                            center=dict(lat=df.lat.mean(), lon=df.lon.mean()),
                            zoom=5, mapbox_style="open-street-map")
    fig.show()

def dms_to_dd(dms, ref):
    degrees, minutes, seconds = [float(x.num) / float(x.den) for x in dms]
    dd = degrees + minutes / 60 + seconds / 3600
    return -dd if ref in ['S', 'W'] else dd

def get_image_gps(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, stop_tag="GPS GPSLongitude")
        try:
            lat = dms_to_dd(tags["GPS GPSLatitude"].values, tags["GPS GPSLatitudeRef"].values)
            lon = dms_to_dd(tags["GPS GPSLongitude"].values, tags["GPS GPSLongitudeRef"].values)
            return lat, lon
        except KeyError:
            return None

def collect_gps_from_folder(folder):
    data = []
    for file in os.listdir(folder):
        if file.lower().endswith((".jpg", ".jpeg")):
            coords = get_image_gps(os.path.join(folder, file))
            if coords:
                data.append({"filename": file, "lat": coords[0], "lon": coords[1]})
    return pd.DataFrame(data)

#%%

coords = collect_gps_from_folder(r"D:/Coding/photo-location-visualization/")
#%%

plot_gps_heatmap(coords)
