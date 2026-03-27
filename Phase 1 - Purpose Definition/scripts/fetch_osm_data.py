"""
Fetch ski resort related data from OpenStreetMap via Overpass API.
Queries for: ski resorts, ski slopes, ski lifts, restaurants, hotels, rental shops
All within the Trentino-Alto Adige/Sudtirol region.
"""

import requests
import json
import csv
import os
import time
import sys

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def query_overpass(query, description=""):
    """Execute an Overpass API query and return JSON results."""
    print(f"  Querying: {description}...")
    try:
        response = requests.post(OVERPASS_URL, data={"data": query}, timeout=120)
        response.raise_for_status()
        data = response.json()
        elements = data.get("elements", [])
        print(f"  -> Got {len(elements)} elements")
        return elements
    except requests.exceptions.RequestException as e:
        print(f"  -> Error: {e}")
        return []


def get_center_coords(element):
    """Extract center coordinates from an OSM element (node, way, or relation)."""
    if element["type"] == "node":
        return element.get("lat"), element.get("lon")
    elif "center" in element:
        return element["center"].get("lat"), element["center"].get("lon")
    elif "bounds" in element:
        b = element["bounds"]
        return (b["minlat"] + b["maxlat"]) / 2, (b["minlon"] + b["maxlon"]) / 2
    return None, None


def get_way_coordinates(element):
    """Extract list of coordinates from a way element with geometry."""
    coords = []
    if "geometry" in element:
        for point in element["geometry"]:
            coords.append((point["lat"], point["lon"]))
    return coords


def save_json(data, filename):
    """Save data as JSON file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {filepath} ({len(data)} records)")


def save_csv(data, filename, fieldnames):
    """Save data as CSV file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)
    print(f"  Saved {filepath} ({len(data)} records)")


# ============================================================
# 1. SKI SLOPES (piste:type=downhill)
# ============================================================
def fetch_ski_slopes():
    print("\n=== Fetching Ski Slopes ===")
    query = """
    [out:json][timeout:90];
    area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
    (
      way["piste:type"="downhill"](area.trentino);
      relation["piste:type"="downhill"](area.trentino);
    );
    out center tags;
    """
    elements = query_overpass(query, "ski slopes (downhill pistes)")

    slopes = []
    for el in elements:
        tags = el.get("tags", {})
        lat, lon = get_center_coords(el)
        slopes.append({
            "id": len(slopes) + 1,
            "osmId": el["id"],
            "osm_type": el["type"],
            "name": tags.get("name", ""),
            "difficulty": tags.get("piste:difficulty", ""),
            "resort": tags.get("piste:name", tags.get("name:resort", "")),
            "ref": tags.get("ref", ""),
            "lit": tags.get("piste:lit", tags.get("lit", "")),
            "grooming": tags.get("piste:grooming", ""),
            "latitude": lat,
            "longitude": lon,
        })

    save_json(slopes, "ski_slopes_raw.json")
    save_csv(slopes, "ski_slopes_raw.csv",
             ["id", "osmId", "osm_type", "name", "difficulty", "resort", "ref", "lit", "grooming", "latitude", "longitude"])
    return slopes


# ============================================================
# 2. SKI LIFTS (aerialway=*)
# ============================================================
def fetch_ski_lifts():
    print("\n=== Fetching Ski Lifts ===")
    query = """
    [out:json][timeout:90];
    area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
    (
      way["aerialway"](area.trentino);
      node["aerialway"](area.trentino);
    );
    out center tags;
    """
    elements = query_overpass(query, "ski lifts (aerialways)")

    lifts = []
    for el in elements:
        tags = el.get("tags", {})
        lat, lon = get_center_coords(el)
        lift_type = tags.get("aerialway", "")
        # Filter to actual ski lifts (not stations)
        if lift_type in ("station",):
            continue
        lifts.append({
            "id": len(lifts) + 1,
            "osmId": el["id"],
            "osm_type": el["type"],
            "name": tags.get("name", ""),
            "type": lift_type,
            "capacity": tags.get("aerialway:capacity", ""),
            "occupancy": tags.get("aerialway:occupancy", ""),
            "duration": tags.get("aerialway:duration", ""),
            "resort": tags.get("name:resort", ""),
            "latitude": lat,
            "longitude": lon,
        })

    save_json(lifts, "ski_lifts_raw.json")
    save_csv(lifts, "ski_lifts_raw.csv",
             ["id", "osmId", "osm_type", "name", "type", "capacity", "occupancy", "duration", "resort", "latitude", "longitude"])
    return lifts


# ============================================================
# 3. SKI RESORTS (landuse=winter_sports / sport=skiing)
# ============================================================
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
      relation["piste:type"="downhill"]["name"](area.trentino);
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


# ============================================================
# 4. RESTAURANTS
# ============================================================
def fetch_restaurants():
    print("\n=== Fetching Restaurants ===")
    query = """
    [out:json][timeout:120];
    area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
    (
      node["amenity"="restaurant"](area.trentino);
      way["amenity"="restaurant"](area.trentino);
      relation["amenity"="restaurant"](area.trentino);
    );
    out center tags;
    """
    elements = query_overpass(query, "restaurants")

    restaurants = []
    for el in elements:
        tags = el.get("tags", {})
        lat, lon = get_center_coords(el)
        # Filter: must have at least a name
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
            "opening_hours": tags.get("opening_hours", ""),
            "latitude": lat,
            "longitude": lon,
        })

    save_json(restaurants, "restaurants_raw.json")
    save_csv(restaurants, "restaurants_raw.csv",
             ["id", "osmId", "osm_type", "name", "cuisine", "phone", "website",
              "addr_city", "addr_street", "addr_housenumber", "addr_postcode",
              "opening_hours", "latitude", "longitude"])
    return restaurants


# ============================================================
# 5. HOTELS
# ============================================================
def fetch_hotels():
    print("\n=== Fetching Hotels ===")
    query = """
    [out:json][timeout:120];
    area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
    (
      node["tourism"="hotel"](area.trentino);
      way["tourism"="hotel"](area.trentino);
      relation["tourism"="hotel"](area.trentino);
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


# ============================================================
# 6. SKI RENTAL SHOPS
# ============================================================
def fetch_rental_shops():
    print("\n=== Fetching Ski Rental Shops ===")
    query = """
    [out:json][timeout:90];
    area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
    (
      node["shop"="ski_rental"](area.trentino);
      way["shop"="ski_rental"](area.trentino);
      node["shop"="sports"]["sport"~"skiing"](area.trentino);
      node["rental"="ski"](area.trentino);
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
            "opening_hours": tags.get("opening_hours", ""),
            "latitude": lat,
            "longitude": lon,
        })

    save_json(shops, "rental_shops_raw.json")
    save_csv(shops, "rental_shops_raw.csv",
             ["id", "osmId", "osm_type", "name", "shop_type", "phone", "website",
              "addr_city", "addr_street", "addr_postcode", "opening_hours",
              "latitude", "longitude"])
    return shops


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("OSM Data Collection for Ski Resorts in Trentino KG Project")
    print("=" * 60)

    results = {}

    # Fetch all datasets with delays between requests
    results["slopes"] = fetch_ski_slopes()
    time.sleep(3)

    results["lifts"] = fetch_ski_lifts()
    time.sleep(3)

    results["resorts"] = fetch_ski_resorts()
    time.sleep(3)

    results["restaurants"] = fetch_restaurants()
    time.sleep(3)

    results["hotels"] = fetch_hotels()
    time.sleep(3)

    results["rental_shops"] = fetch_rental_shops()

    # Summary
    print("\n" + "=" * 60)
    print("COLLECTION SUMMARY")
    print("=" * 60)
    for key, data in results.items():
        print(f"  {key}: {len(data)} records")
    print(f"\nAll data saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
