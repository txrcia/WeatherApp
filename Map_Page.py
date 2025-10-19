import streamlit as st
import pandas as pd
import random
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from streamlit.components.v1 import html

def map_page():
        
    dubai_coords = [
    ("Downtown Dubai", 25.2048, 55.2708),
    ("Jumeirah Beach", 25.2180, 55.2590),
    ("Dubai Marina", 25.0800, 55.1433),
    ("Deira", 25.2650, 55.3100),
    ("Al Barsha", 25.1180, 55.2000),
    ]

    data = []
    for name, lat, lon in dubai_coords:
        data.append({
            "location": name,
            "latitude": lat,
            "longitude": lon,
            "parameter": "pm25",
            "value": round(random.uniform(5, 60), 1)
        })
        data.append({
            "location": name,
            "latitude": lat,
            "longitude": lon,
            "parameter": "relativehumidity",
            "value": round(random.uniform(20, 70), 1)
        })
        data.append({
            "location": name,
            "latitude": lat,
            "longitude": lon,
            "parameter": "temperature",
            "value": round(random.uniform(25, 50), 1)
        })

    df = pd.DataFrame(data)

    # ------------------------
    # Add human-friendly labels
    # ------------------------
    def label_pm25(value):
        if value <= 12:
            return "Air quality is good"
        elif value <= 35.4:
            return "A mask would be nice"
        elif value <= 55.4:
            return "Avoid going out unless necessary"
        else:
            return "Dangerous to go out"

    def label_rh(value):
        if value < 30:
            return "It is dry outside"
        elif value <= 50:
            return "It is quite comfortable"
        else:
            return "Humidity level is very high"

    def label_temp(value):
        if 20 <= value <= 35:
            return "Pleasant"
        elif 35 < value <= 40:
            return "Good day to go to the beach"
        elif value <= 50:
            return "Moderate temp"
        else:
            return "Way too hot, good day to sleep in"

    def add_labels(row):
        if row['parameter'] == 'pm25':
            return label_pm25(row['value'])
        elif row['parameter'] == 'relativehumidity':
            return label_rh(row['value'])
        elif row['parameter'] == 'temperature':
            return label_temp(row['value'])
        else:
            return ""

    df['label'] = df.apply(add_labels, axis=1)

    # ------------------------
    # Streamlit App
    # ------------------------
    st.title("Dubai Air Quality & Weather Map")

    st.write("Interactive map showing PM2.5, Humidity, and Temperature levels in Dubai")



    # ------------------------
    # Filter PM2.5 data
    # ------------------------
    df_pm25 = df[df['parameter'] == 'pm25']



    dubai_map = folium.Map(location=[25.1950, 55.2784], zoom_start=12)
    heat_data = [[row['latitude'], row['longitude'], row['value']] for _, row in df_pm25.iterrows()]
    HeatMap(heat_data, radius=25, blur=15, min_opacity=0.5).add_to(dubai_map)

    # ------------------------
    # Add markers with location + all labels
    # ------------------------
    locations = df['location'].unique()
    for loc in locations:
        subset = df[df['location'] == loc]
        lat = subset['latitude'].iloc[0]
        lon = subset['longitude'].iloc[0]

        # Combine labels for popup
        popup_text = f"<b>{loc}</b><br>"
        for _, row in subset.iterrows():
            popup_text += f"{row['label']}<br>"

        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(color='blue')
        ).add_to(dubai_map)

    # ------------------------
    # Render stable map
    # ------------------------
    map_html = dubai_map._repr_html_()
    html(map_html, height=500, width=900)