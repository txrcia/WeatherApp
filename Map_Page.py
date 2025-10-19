import streamlit as st
from openaq import OpenAQ
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import time

def map_page():
        
    st.title("🌤️ Air Quality & Heat Map")

    # --- 1. Get city input ---
    city = st.text_input("Enter your city:", "Dubai") # have to get this specificly into the program

    #coordinates of a point in Dubai = 25.1950, 55.2784. For radius use 400000.

    # --- 2. Fetch Air Quality Data from OpenAQ ---
    if city:
        st.subheader(f"Air Quality in {city}")
            
        max_retries = 3
        
        # url and key to OpenAQ.
        url = f"https://api.openaq.org/v3/locations/2178"
        headers = {"X-API-Key": "66fc980b7a7981477c6349e5d284b1e25b167d1c56f2a61e134be355dd1f71ff"}


        # this is to account for possible errors. Give the site 3 chances to get a new response
        # if using OpenAQ function, i.e., client = OpenAQ(api_key=....), then remove this
        #        as it does not work in the same way
        for attempt in range(max_retries):
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                break
            else:
                st.info(f"Attempt {attempt+1} failed: {response.status_code}. Retrying...")
                time.sleep(2)  # wait 2 seconds before retry
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            if results:
                # Prepare data for table and map
                records = []
                for item in results:
                    loc = item['locality'] # locations is the tab in the document,
                                            # however, locality is what mentions the place.
                                            # locality gives country, so better to change it to 'name'
                                            # 'name' gives state/city in our case.
                    lat = item['coordinates']['latitude']
                    lon = item['coordinates']['longitude']
                    val = item.get("measurements", []) # this is a little confusing.
                                                        # the documentation shows coverage under
                                                        # measurements, which has a key called 
                                                        # 'observedCount'. This key would help us get the
                                                        # value. But I was not able to integrate it.
                                                        # furthermore, there is a 'value' key
                                                        # but I kept getting errors no matter what combination
                                                        # I tried to get 'value' with. This might also
                                                        # give the desired output.

                    #measurements = {['parameter']}  # before testing this out, remove the dict brackets
                    records.append({"Location": loc, "Latitude": lat, "Longitude": lon, "Measurements": val})
                
                df = pd.DataFrame(records)
                st.dataframe(df)

                # --- 3. Display Map ---
                m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=12)
                
                for idx, row in df.iterrows():
                    folium.Marker(
                        location=[row['Latitude'], row['Longitude']],
                        popup=f"{row['Location']}<br>PM2.5: {row.get('pm25', 'N/A')} µg/m³<br>PM10: {row.get('pm10', 'N/A')} µg/m³",
                        icon=folium.Icon(color='red' if row.get('pm25', 0) > 50 else 'green')
                    ).add_to(m)
                
                st_folium(m, width=700, height=500)
                
            else:
                st.warning("No data available for this city.")
        else:
            st.error("Failed to fetch data after 3 attempts. Please try again later.")
            data = {"results": []}  # fallback
