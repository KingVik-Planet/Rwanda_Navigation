import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import openrouteservice

# Function to perform the search
def search_location(query):
    geolocator = Nominatim(user_agent="my_search_app")
    location = geolocator.geocode(query)

    if location:
        return [location.latitude, location.longitude]
    else:
        return None

# Function to calculate ETA and draw route
def calculate_and_draw_route(start, end, map_object):
    # Set up OpenRouteService client
    client = openrouteservice.Client(key='5b3ce3597851110001cf6248f1bfcdf2da724bb8a95d2670504224d0')

    # Check if start and end coordinates are valid
    if not start or not end:
        st.warning("Invalid start or end location. Please enter valid locations.")
        return

    try:
        # Calculate route
        route = client.directions(coordinates=[start, end], profile='driving-car', format='geojson')

        # Draw the route on the map
        folium.PolyLine(locations=[list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']],
                        color='blue').add_to(map_object)

        # Calculate ETA
        duration = route['features'][0]['properties']['segments'][0]['duration']
        st.write(f"Estimated Time of Arrival (ETA): {duration} seconds")
    except openrouteservice.exceptions.ApiError as e:
        st.warning(f"Error calculating route: {e}")

# Streamlit app
st.title("Rwanda Navigation")

# User input for start and end locations
start_query = st.text_input("Enter Start Location:")
end_query = st.text_input("Enter End Location:")

# Check if both queries are not empty
if start_query and end_query:
    # Search for the start and end locations
    start_location = search_location(start_query)
    end_location = search_location(end_query)

    # Display the map centered at the start location
    if start_location:
        result_map = folium.Map(location=start_location, zoom_start=12)

        # Add a marker for the start location
        folium.Marker(
            location=start_location,
            popup="Start: " + start_query,
            icon=folium.Icon(color='green')
        ).add_to(result_map)

        # Add a marker for the end location
        if end_location:
            folium.Marker(
                location=end_location,
                popup="End: " + end_query,
                icon=folium.Icon(color='red')
            ).add_to(result_map)

            # Calculate and draw the route
            calculate_and_draw_route(start_location, end_location, result_map)

            # Display the result map using folium_static
            st.write("Route from", start_query, "to", end_query)
            folium_static(result_map)
        else:
            st.warning("End location not found. Please enter a valid location.")
    else:
        st.warning("Start location not found. Please enter a valid location.")
