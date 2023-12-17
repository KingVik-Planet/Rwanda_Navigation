import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim

# Function to perform the search
def search_location(query):
    geolocator = Nominatim(user_agent="my_search_app")
    location = geolocator.geocode(query)

    if location:
        # Create a map centered at the search result
        m = folium.Map(location=[location.latitude, location.longitude], zoom_start=14)

        # Add a marker for the search result
        folium.Marker(
            location=[location.latitude, location.longitude],
            popup=query,
            icon=folium.Icon(color='blue')
        ).add_to(m)

        return m
    else:
        return None

# Streamlit app
st.title("Location Search and Display")

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
