from datetime import datetime, timezone


def convertFromFormat1(jsonObject):
    """Convert Format 1 telemetry data to the unified format.

    Format 1 has 'location' as a slash-separated string:
    "country/city/area/factory/section"
    """
    parts = jsonObject["location"].split("/")
    if len(parts) != 5:
        raise ValueError(
            f"Expected location string with 5 components separated by '/', "
            f"got {len(parts)}: {jsonObject['location']!r}"
        )
    result = dict(jsonObject)
    result["location"] = {
        "country": parts[0],
        "city": parts[1],
        "area": parts[2],
        "factory": parts[3],
        "section": parts[4],
    }
    return result


def convertFromFormat2(jsonObject):
    """Convert Format 2 telemetry data to the unified format.

    Format 2 has 'timestamp' as an ISO 8601 string.
    Converts it to milliseconds since the Unix epoch.
    """
    result = dict(jsonObject)
    dt = datetime.fromisoformat(
        jsonObject["timestamp"].replace("Z", "+00:00")
    )
    result["timestamp"] = int(dt.timestamp() * 1000)
    return result
