import json
import os
from functools import lru_cache


@lru_cache(maxsize=1)
def get_algerian_wilayas():
    wilayas = []
    file_path = os.path.join(os.path.dirname(__file__), 'algeria_cities.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for entry in data:
            wilaya_name = entry.get('wilaya_name')
            wilaya_code = entry.get('wilaya_code')
            if wilaya_name and wilaya_code and (wilaya_code, wilaya_name) not in wilayas:
                wilayas.append((wilaya_code, wilaya_name))
    return tuple(wilayas)