import streamlit as st
from streamlit_folium import folium_static
import folium
from folium import plugins

# Create a Streamlit app
st.title("Interactive Map with Streamlit")

# Create a map centered at Kigali, Rwanda
kigali_location = [-1.9536, 30.0606]
m = folium.Map(location=kigali_location, zoom_start=12)

# Add OpenStreetMap tiles as the background
folium.TileLayer('openstreetmap').add_to(m)

# Add Stamen Terrain tiles as a satellite view
folium.TileLayer('Stamen Terrain').add_to(m)

# Add Stamen Toner tiles
folium.TileLayer('Stamen Toner').add_to(m)

# Add Stamen Water Color tiles
folium.TileLayer('Stamen Water Color').add_to(m)

# Add CartoDB Positron tiles
folium.TileLayer('CartoDB Positron').add_to(m)

# Create a FeatureGroup to hold base maps
base_maps = folium.FeatureGroup(name='Base Maps').add_to(m)

# Add the base maps to the FeatureGroup
folium.TileLayer('openstreetmap').add_to(base_maps)
folium.TileLayer('Stamen Terrain', attr='Stamen').add_to(base_maps)
folium.TileLayer('Stamen Satellite', attr='Stamen').add_to(base_maps)
folium.TileLayer('Stamen Toner').add_to(base_maps)
folium.TileLayer('Stamen Water Color').add_to(base_maps)
folium.TileLayer('CartoDB Positron').add_to(base_maps)

# Add layer control for switching between base maps
folium.LayerControl().add_to(m)

# Add a search box
search = plugins.Search(layer=base_maps, geom_type='Point')  # Pass the FeatureGroup to the layer parameter
search.add_to(m)

# Display the map using folium_static
st.write("Interactive Map:")
folium_static(m)
