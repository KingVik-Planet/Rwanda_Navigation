import streamlit as st
import folium
from streamlit_folium import folium_static
import geocoder

# Function to perform the search
def search_location(query):
    location = geocoder.osm(query)
    if location.ok:
        m = folium.Map(location=[location.latlng[0], location.latlng[1]], zoom_start=14)
        folium.Marker(
            location=[location.latlng[0], location.latlng[1]],
            popup=query,
            icon=folium.Icon(color='blue')
        ).add_to(m)
        return m
    else:
        return None

# Create a Streamlit app
st.title("Interactive Map with Streamlit")

# Create a map centered at Kigali, Rwanda
kigali_location = [-1.9536, 30.0606]
m = folium.Map(location=kigali_location, zoom_start=12)

# Display the map using folium_static
st.write("Interactive Map:")
folium_static(m)

# User input for location
query = st.text_input("Enter Location of Interest:")

# Check if the query is not empty
if query:
    # Search for the location
    result_map = search_location(query)

    # Display the result map using folium_static
    if result_map:
        st.write("Map for:", query)
        folium_static(result_map)
    else:
        st.warning("Location not found. Please enter a valid location.")
