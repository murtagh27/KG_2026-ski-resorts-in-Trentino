"""Fetch remaining OSM data (resorts, restaurants, hotels, rental shops) with longer delays."""
import requests
import json
import csv
import os
import time

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def query_overpass(query, description=""):
    print(f"  Querying: {description}...")
    for attempt in range(3):
        try:
            response = requests.post(OVERPASS_URL, data={"data": query}, timeout=180)
            response.raise_for_status()
            data = response.json()
            elements = data.get("elements", [])
            print(f"  -> Got {len(elements)} elements")
            return elements
        except requests.exceptions.RequestException as e:
            print(f"  -> Attempt {attempt+1} error: {e}")
            if attempt < 2:
                wait = 30 * (attempt + 1)
                print(f"  -> Waiting {wait}s before retry...")
                time.sleep(wait)
    return []


def get_center_coords(element):
    if element["type"] == "node":
        return element.get("lat"), element.get("lon")
    elif "center" in element:
        return element["center"].get("lat"), element["center"].get("lon")
    elif "bounds" in element:
        b = element["bounds"]
        return (b["minlat"] + b["maxlat"]) / 2, (b["minlon"] + b["maxlon"]) / 2
    return None, None


def save_json(data, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {filepath} ({len(data)} records)")


def save_csv(data, filename, fieldnames):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)
    print(f"  Saved {filepath} ({len(data)} records)")


def fetch_ski_resorts():
    print("\n=== Fetching Ski Resorts ===")
    query = """
    [out:json][timeout:90];
    area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
    (
      node["sport"="skiing"](area.trentino);
      way["sport"="skiing"](area.trentino);
      relation["sport"="skiing"](area.trentino);
      node["landuse"="winter_sports"](area.trentino);
      way["landuse"="winter_sports"](area.trentino);
      relation["landuse"="winter_sports"](area.trentino);
      node["tourism"="winter_sports"](area.trentino);
      way["tourism"="winter_sports"](area.trentino);
    );
    out center tags;
    """
    elements = query_overpass(query, "ski resorts")
    resorts = []
    for el in elements:
        tags = el.get("tags", {})
        lat, lon = get_center_coords(el)
        resorts.append({
            "id": len(resorts) + 1,
            "osmId": el["id"],
            "osm_type": el["type"],
            "name": tags.get("name", ""),
            "website": tags.get("website", tags.get("contact:website", "")),
            "phone": tags.get("phone", tags.get("contact:phone", "")),
            "operator": tags.get("operator", ""),
            "municipality": tags.get("addr:city", ""),
            "latitude": lat,
            "longitude": lon,
        })
    save_json(resorts, "ski_resorts_raw.json")
    save_csv(resorts, "ski_resorts_raw.csv",
             ["id", "osmId", "osm_type", "name", "website", "phone", "operator", "municipality", "latitude", "longitude"])
    return resorts


def fetch_restaurants():
    print("\n=== Fetching Restaurants ===")
    query = """
    [out:json][timeout:120];
    area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
    (
      node["amenity"="restaurant"](area.trentino);
      way["amenity"="restaurant"](area.trentino);
    );
    out center tags;
    """
    elements = query_overpass(query, "restaurants")
    restaurants = []
    for el in elements:
        tags = el.get("tags", {})
        lat, lon = get_center_coords(el)
        if not tags.get("name"):
            continue
        restaurants.append({
            "id": len(restaurants) + 1,
            "osmId": el["id"],
            "osm_type": el["type"],
            "name": tags.get("name", ""),
            "cuisine": tags.get("cuisine", ""),
            "phone": tags.get("phone", tags.get("contact:phone", "")),
            "website": tags.get("website", tags.get("contact:website", "")),
            "addr_city": tags.get("addr:city", ""),
            "addr_street": tags.get("addr:street", ""),
            "addr_housenumber": tags.get("addr:housenumber", ""),
            "addr_postcode": tags.get("addr:postcode", ""),
            "latitude": lat,
            "longitude": lon,
        })
    save_json(restaurants, "restaurants_raw.json")
    save_csv(restaurants, "restaurants_raw.csv",
             ["id", "osmId", "osm_type", "name", "cuisine", "phone", "website",
              "addr_city", "addr_street", "addr_housenumber", "addr_postcode",
              "latitude", "longitude"])
    return restaurants


def fetch_hotels():
    print("\n=== Fetching Hotels ===")
    query = """
    [out:json][timeout:120];
    area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
    (
      node["tourism"="hotel"](area.trentino);
      way["tourism"="hotel"](area.trentino);
    );
    out center tags;
    """
    elements = query_overpass(query, "hotels")
    hotels = []
    for el in elements:
        tags = el.get("tags", {})
        lat, lon = get_center_coords(el)
        if not tags.get("name"):
            continue
        hotels.append({
            "id": len(hotels) + 1,
            "osmId": el["id"],
            "osm_type": el["type"],
            "name": tags.get("name", ""),
            "stars": tags.get("stars", ""),
            "rooms": tags.get("rooms", ""),
            "beds": tags.get("beds", ""),
            "phone": tags.get("phone", tags.get("contact:phone", "")),
            "email": tags.get("email", tags.get("contact:email", "")),
            "website": tags.get("website", tags.get("contact:website", "")),
            "addr_city": tags.get("addr:city", ""),
            "addr_street": tags.get("addr:street", ""),
            "addr_housenumber": tags.get("addr:housenumber", ""),
            "addr_postcode": tags.get("addr:postcode", ""),
            "latitude": lat,
            "longitude": lon,
        })
    save_json(hotels, "hotels_raw.json")
    save_csv(hotels, "hotels_raw.csv",
             ["id", "osmId", "osm_type", "name", "stars", "rooms", "beds",
              "phone", "email", "website",
              "addr_city", "addr_street", "addr_housenumber", "addr_postcode",
              "latitude", "longitude"])
    return hotels


def fetch_rental_shops():
    print("\n=== Fetching Ski Rental Shops ===")
    query = """
    [out:json][timeout:90];
    area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
    (
      node["shop"="ski_rental"](area.trentino);
      way["shop"="ski_rental"](area.trentino);
      node["shop"="ski"](area.trentino);
      way["shop"="ski"](area.trentino);
    );
    out center tags;
    """
    elements = query_overpass(query, "ski rental shops")
    shops = []
    seen_ids = set()
    for el in elements:
        if el["id"] in seen_ids:
            continue
        seen_ids.add(el["id"])
        tags = el.get("tags", {})
        lat, lon = get_center_coords(el)
        shops.append({
            "id": len(shops) + 1,
            "osmId": el["id"],
            "osm_type": el["type"],
            "name": tags.get("name", ""),
            "shop_type": tags.get("shop", ""),
            "phone": tags.get("phone", tags.get("contact:phone", "")),
            "website": tags.get("website", tags.get("contact:website", "")),
            "addr_city": tags.get("addr:city", ""),
            "addr_street": tags.get("addr:street", ""),
            "addr_postcode": tags.get("addr:postcode", ""),
            "latitude": lat,
            "longitude": lon,
        })
    save_json(shops, "rental_shops_raw.json")
    save_csv(shops, "rental_shops_raw.csv",
             ["id", "osmId", "osm_type", "name", "shop_type", "phone", "website",
              "addr_city", "addr_street", "addr_postcode",
              "latitude", "longitude"])
    return shops


if __name__ == "__main__":
    print("Fetching remaining OSM data (with retry logic)...")
    print("Waiting 15s for rate limit to cool down...\n")
    time.sleep(15)

    r1 = fetch_ski_resorts()
    time.sleep(10)
    r2 = fetch_restaurants()
    time.sleep(10)
    r3 = fetch_hotels()
    time.sleep(10)
    r4 = fetch_rental_shops()

    print("\n=== SUMMARY ===")
    print(f"  Ski resorts: {len(r1)}")
    print(f"  Restaurants: {len(r2)}")
    print(f"  Hotels: {len(r3)}")
    print(f"  Rental shops: {len(r4)}")
