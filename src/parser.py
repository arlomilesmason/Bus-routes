import os
import xml.etree.ElementTree as ET
import pandas as pd


def extract_service_number(filename):
    service = filename.split("-")[0]
    return service.lstrip("0") or service


def parse_single_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        if "}" in root.tag:
            ns_uri = root.tag.split("}")[0].strip("{")
            ns = {"ns": ns_uri}
        else:
            ns = {}

    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return [], []

    journeys = []
    routes = []

    try:
        route_name = extract_service_number(os.path.basename(file_path))

        # ✅ Extract route geometry
        for link in root.findall('.//ns:RouteLink', ns):
            coords = []

            for loc in link.findall('.//ns:Location', ns):
                lat = loc.findtext('ns:Latitude', namespaces=ns)
                lon = loc.findtext('ns:Longitude', namespaces=ns)

                if lat and lon:
                    coords.append((float(lat), float(lon)))

            if len(coords) > 1:
                routes.append({
                    "route": route_name,
                    "coords": coords
                })

        for journey in root.findall('.//ns:VehicleJourney', ns):
            journeys.append({
                "route": route_name,
                "departure_time": journey.findtext(
                    './/ns:DepartureTime', default="", namespaces=ns)
            })

    except Exception as e:
        print(f"[WARN] {file_path}: {e}")

    return journeys, routes


def parse_folder(folder_path):
    all_journeys = []
    all_routes = []

    xml_files = [f for f in os.listdir(folder_path) if f.endswith(".xml")]

    for file in xml_files:
        print(f"Processing {file}...")

        journeys, routes = parse_single_file(os.path.join(folder_path, file))

        all_journeys.extend(journeys)
        all_routes.extend(routes)

    return pd.DataFrame(all_journeys), all_routes