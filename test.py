import requests
import json
from itertools import islice

def chunked_iterable(iterable, size):
    """Yield successive n-sized chunks from an iterable."""
    it = iter(iterable)
    while chunk := list(islice(it, size)):
        yield chunk

def fetch_map_ids():
    """Fetches the list of map IDs from the API."""
    response = requests.get("https://api.guildwars2.com/v2/maps")
    response.raise_for_status()
    return response.json()

def fetch_map_details(map_ids):
    """Fetches detailed information for given map IDs."""
    ids_param = ",".join(map(str, map_ids))
    url = f"https://api.guildwars2.com/v2/maps?ids={ids_param}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def main():
    map_ids = fetch_map_ids()
    map_details = {}
    
    for chunk in chunked_iterable(map_ids, 50):
        details = fetch_map_details(chunk)
        for detail in details:
            map_details[detail['id']] = detail['name']
    
    with open("map_details.json", "w", encoding="utf-8") as f:
        json.dump(map_details, f, indent=4)

if __name__ == "__main__":
    main()