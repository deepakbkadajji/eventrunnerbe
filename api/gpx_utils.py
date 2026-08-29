import xml.etree.ElementTree as ET

GPX_NS = {"gpx": "http://www.topografix.com/GPX/1/1"}


def _encode_polyline_value(value):
    value = int(round(value * 1e5))
    value = ~(value << 1) if value < 0 else (value << 1)
    chunks = []
    while value >= 0x20:
        chunks.append(chr((0x20 | (value & 0x1F)) + 63))
        value >>= 5
    chunks.append(chr(value + 63))
    return "".join(chunks)


def encode_polyline(coordinates):
    encoded = []
    previous_lat = 0
    previous_lng = 0
    for lat, lng in coordinates:
        encoded.append(_encode_polyline_value(lat - previous_lat))
        encoded.append(_encode_polyline_value(lng - previous_lng))
        previous_lat = lat
        previous_lng = lng
    return "".join(encoded)


def _parse_lat_lon(trkpt):
    lat = trkpt.get("lat")
    lon = trkpt.get("lon")
    if lat is None or lon is None:
        return None
    return float(lat), float(lon)


def extract_track_points_from_gpx(gpx_content):
    if isinstance(gpx_content, bytes):
        gpx_content = gpx_content.decode("utf-8")

    root = ET.fromstring(gpx_content)
    points = []

    for trkpt in root.findall(".//gpx:trkpt", GPX_NS):
        point = _parse_lat_lon(trkpt)
        if point:
            points.append(point)

    if not points:
        for trkpt in root.findall(".//trkpt"):
            point = _parse_lat_lon(trkpt)
            if point:
                points.append(point)

    if not points:
        for rtept in root.findall(".//gpx:rtept", GPX_NS):
            point = _parse_lat_lon(rtept)
            if point:
                points.append(point)

    if not points:
        for rtept in root.findall(".//rtept"):
            point = _parse_lat_lon(rtept)
            if point:
                points.append(point)

    if len(points) < 2:
        raise ValueError("GPX file must contain at least two track or route points.")

    return points


def gpx_to_encoded_polyline(gpx_content):
    coordinates = extract_track_points_from_gpx(gpx_content)
    return encode_polyline(coordinates)
