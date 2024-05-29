import pandas as pd
import numpy as np
from glob import glob
import folium
from datetime import datetime
from geopy.geocoders import Nominatim
import traceback


def get_lat_lon(location_name):
    geolocator = Nominatim(user_agent="location_finder")
    location = geolocator.geocode(location_name)
    if location:
        latitude, longitude = location.latitude, location.longitude
        return latitude, longitude
    else:
        return None


def generate_map(coordinates, location_name):
    if coordinates:
        lat = coordinates[0]
        long = coordinates[1]
        map = folium.Map(location=[lat, long], zoom_start=150)

        # create an iframe pop-up for the marker
        popup_html = f"<b>Date:</b> 10th October, 2023<br/>"
        popup_html += f"<b>Location:</b> Department of Maths <br/>"
        popup_html += f"<b>Time:</b> {datetime.now()}<br/>"
        popup_html += '<b><a href="{}" target="_blank">Event Page</a></b>'.format(
            "Testing Map"
        )
        popup_iframe = folium.IFrame(width=200, height=110, html=popup_html)

        folium.Marker(
            location=[lat, long],
            popup=folium.Popup(popup_iframe),
            icon=folium.Icon(color="red"),
        ).add_to(map)
        points = [(24.94411, 67.08085), (24.9443, 67.0793), (24.94351, 67.08298)]
        folium.PolyLine(points, color="red", weight=5, opacity=0.85).add_to(map)

        map.save("map.html")
    else:
        print(
            f"Location not found for {location_name}. Please check the spelling or provide more details."
        )


def fetch_tracking_records(df, start_location, end_location):
    start_location_df = df[df["desc"] == start_location]
    end_location_df = df[df["desc"] == end_location]
    if start_location_df.empty or end_location_df.empty:
        print(f"One or both of the specified locations not found.")
        return pd.DataFrame()
    start_index = start_location_df.index[0]
    end_index = end_location_df.index[0]
    tracking_records = df.loc[start_index:end_index, ["latitude", "longitude"]]
    return tracking_records


def gather_data(path_to_files_folder):
    """This function gathers all files and generate a single file"""
    files = glob(path_to_files_folder)
    final = pd.DataFrame()
    for file in files:
        file_data = pd.read_csv(files[0])
        final = pd.concat([final, file_data])
    data = final.copy(deep=True)
    data = data.drop_duplicates()
    data = data[["type", "latitude", "longitude", "desc"]]
    return data


def generate_tracking_memory(reference, tracking):
    tracking_memory = {}
    all_locations = list(reference["desc"])
    for i, fromm in enumerate(all_locations):
        for j, tto in enumerate(all_locations):
            if i != j:  # Ensure different locations
                key = f"{fromm}-{tto}"
                reverse_key = f"{tto}-{fromm}"
                value = fetch_tracking_records(tracking, fromm, tto)
                if not value.empty:
                    tracking_memory[key] = value
                    tracking_memory[reverse_key] = value
    return tracking_memory


def label_data(reference, tracking):
    for lat, long, label in zip(
        reference.latitude, reference.longitude, reference.desc
    ):
        condition = (tracking["latitude"] == lat) & (tracking["longitude"] == long)
        print("Marking", label)
        tracking.loc[condition, "desc"] = label
    return tracking


def get_locations(files_folder):
    data = gather_data(files_folder)
    reference = data[data["type"] == "W"]
    return data, reference


def generate_map_string(current, destination):
    data, reference = get_locations("csv_data/*.csv")
    reference = data[data["type"] == "W"]
    tracking = data[data["type"] == "T"]
    tracking = label_data(reference, tracking)
    tracking_memory = generate_tracking_memory(reference, tracking)
    lat, long = get_lat_lon("Sindh Madressa-tul-Islam University")
    smiu_map = folium.Map(location=[lat, long], zoom_start=150)
    for lat, lng, label in zip(reference.latitude, reference.longitude, reference.desc):
        folium.Marker(
            [lat, lng],
            popup=label,
        ).add_to(smiu_map)

    track = tracking_memory[f"{current}-{destination}"]
    points = [(x, y) for x, y in zip(track.latitude, track.longitude)]
    folium.PolyLine(points, color="yellow", weight=5, opacity=0.85).add_to(smiu_map)
    filename = f"./maps/{current}-{destination}.html"
    smiu_map.save(filename)
    with open(filename, 'r') as file:
        html_content = file.read()
        return html_content
