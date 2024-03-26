from typing import Any

import shapefile  # type: ignore


def convert_shapefile_to_geojson_objects(filepath: str) -> list[dict[str, Any]]:
    # read the shapefile
    reader = shapefile.Reader(filepath)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))

    return buffer
