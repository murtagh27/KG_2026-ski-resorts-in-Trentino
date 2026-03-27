"""
Clean and format all raw datasets from Phase 1.
- Standardize column names to match finalized language terms
- Remove duplicates, entries without coordinates
- Standardize categorical values
- Associate slopes/lifts with resorts via proximity
"""

import json
import csv
import os
import math

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                       "Phase 1 - Purpose Definition", "data")
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(OUT_DIR, exist_ok=True)


def load_json(filename):
    filepath = os.path.join(RAW_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, filename):
    filepath = os.path.join(OUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {filename}: {len(data)} records")


def save_csv(data, filename, fieldnames):
    filepath = os.path.join(OUT_DIR, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)
    print(f"  Saved {filename}: {len(data)} records")


def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km."""
    if any(v is None for v in [lat1, lon1, lat2, lon2]):
        return float("inf")
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


# ============================================================
# Clean Ski Resorts
# ============================================================
def clean_resorts():
    print("\n=== Cleaning Ski Resorts ===")
    raw = load_json("ski_resorts_raw.json")

    # Filter: must have name and coordinates
    cleaned = []
    seen_names = set()
    for r in raw:
        name = r.get("name", "").strip()
        if not name or r.get("latitude") is None:
            continue
        # Deduplicate by name (keep first/most complete)
        name_lower = name.lower()
        if name_lower in seen_names:
            continue
        seen_names.add(name_lower)
        cleaned.append({
            "resortId": len(cleaned) + 1,
            "osmId": str(r["osmId"]),
            "name": name,
            "municipality": r.get("municipality", ""),
            "website": r.get("website", ""),
            "phone": r.get("phone", ""),
            "operator": r.get("operator", ""),
            "latitude": r["latitude"],
            "longitude": r["longitude"],
        })

    save_json(cleaned, "ski_resorts_cleaned.json")
    save_csv(cleaned, "ski_resorts_cleaned.csv",
             ["resortId", "osmId", "name", "municipality", "website", "phone", "operator", "latitude", "longitude"])
    return cleaned


# ============================================================
# Clean Ski Slopes
# ============================================================
def clean_slopes(resorts):
    print("\n=== Cleaning Ski Slopes ===")
    raw = load_json("ski_slopes_raw.json")

    DIFFICULTY_MAP = {
        "novice": "novice", "easy": "easy", "intermediate": "intermediate",
        "advanced": "advanced", "expert": "expert", "freeride": "freeride",
        "": ""
    }

    cleaned = []
    seen_osm = set()
    for s in raw:
        osm_id = s.get("osmId")
        if osm_id in seen_osm:
            continue
        seen_osm.add(osm_id)

        if s.get("latitude") is None:
            continue

        diff = s.get("difficulty", "").lower().strip()
        difficulty = DIFFICULTY_MAP.get(diff, diff)

        # Find nearest resort
        nearest_resort = ""
        min_dist = float("inf")
        for r in resorts:
            d = haversine_km(s["latitude"], s["longitude"], r["latitude"], r["longitude"])
            if d < min_dist:
                min_dist = d
                nearest_resort = r["name"]

        cleaned.append({
            "slopeId": len(cleaned) + 1,
            "osmId": str(osm_id),
            "name": s.get("name", ""),
            "difficulty": difficulty,
            "resort": s.get("resort", "") or (nearest_resort if min_dist < 15 else ""),
            "ref": s.get("ref", ""),
            "latitude": s["latitude"],
            "longitude": s["longitude"],
        })

    save_json(cleaned, "ski_slopes_cleaned.json")
    save_csv(cleaned, "ski_slopes_cleaned.csv",
             ["slopeId", "osmId", "name", "difficulty", "resort", "ref", "latitude", "longitude"])
    return cleaned


# ============================================================
# Clean Ski Lifts
# ============================================================
def clean_lifts(resorts):
    print("\n=== Cleaning Ski Lifts ===")
    raw = load_json("ski_lifts_raw.json")

    LIFT_TYPES = {"chair_lift", "gondola", "cable_car", "drag_lift", "t-bar",
                  "platter", "magic_carpet", "mixed_lift", "j-bar", "rope_tow", "zip_line"}

    cleaned = []
    seen_osm = set()
    for l in raw:
        osm_id = l.get("osmId")
        if osm_id in seen_osm:
            continue
        seen_osm.add(osm_id)

        if l.get("latitude") is None:
            continue

        lift_type = l.get("type", "").lower().strip()
        if lift_type not in LIFT_TYPES and lift_type:
            lift_type = lift_type  # keep as-is if not in standard set

        # Find nearest resort
        nearest_resort = ""
        min_dist = float("inf")
        for r in resorts:
            d = haversine_km(l["latitude"], l["longitude"], r["latitude"], r["longitude"])
            if d < min_dist:
                min_dist = d
                nearest_resort = r["name"]

        cleaned.append({
            "liftId": len(cleaned) + 1,
            "osmId": str(osm_id),
            "name": l.get("name", ""),
            "liftType": lift_type,
            "capacity": l.get("capacity", ""),
            "resort": l.get("resort", "") or (nearest_resort if min_dist < 15 else ""),
            "latitude": l["latitude"],
            "longitude": l["longitude"],
        })

    save_json(cleaned, "ski_lifts_cleaned.json")
    save_csv(cleaned, "ski_lifts_cleaned.csv",
             ["liftId", "osmId", "name", "liftType", "capacity", "resort", "latitude", "longitude"])
    return cleaned


# ============================================================
# Clean Hotels
# ============================================================
def clean_hotels(resorts):
    print("\n=== Cleaning Hotels ===")
    raw = load_json("hotels_raw.json")

    cleaned = []
    seen_osm = set()
    for h in raw:
        osm_id = h.get("osmId")
        if osm_id in seen_osm:
            continue
        seen_osm.add(osm_id)

        if h.get("latitude") is None:
            continue

        # Find nearest resort
        nearest_resort = ""
        min_dist = float("inf")
        for r in resorts:
            d = haversine_km(h["latitude"], h["longitude"], r["latitude"], r["longitude"])
            if d < min_dist:
                min_dist = d
                nearest_resort = r["name"]

        cleaned.append({
            "hotelId": len(cleaned) + 1,
            "osmId": str(osm_id),
            "name": h.get("name", ""),
            "starRating": h.get("stars", ""),
            "numberOfBeds": h.get("beds", ""),
            "phone": h.get("phone", ""),
            "email": h.get("email", ""),
            "website": h.get("website", ""),
            "municipality": h.get("addr_city", ""),
            "address": f'{h.get("addr_street", "")} {h.get("addr_housenumber", "")}'.strip(),
            "postcode": h.get("addr_postcode", ""),
            "nearResort": nearest_resort if min_dist < 20 else "",
            "distanceToResort_km": round(min_dist, 1) if min_dist < 20 else None,
            "latitude": h["latitude"],
            "longitude": h["longitude"],
        })

    save_json(cleaned, "hotels_cleaned.json")
    save_csv(cleaned, "hotels_cleaned.csv",
             ["hotelId", "osmId", "name", "starRating", "numberOfBeds",
              "phone", "email", "website", "municipality", "address", "postcode",
              "nearResort", "distanceToResort_km", "latitude", "longitude"])
    return cleaned


# ============================================================
# Clean Restaurants
# ============================================================
def clean_restaurants(resorts):
    print("\n=== Cleaning Restaurants ===")
    raw = load_json("restaurants_raw.json")

    cleaned = []
    seen_osm = set()
    for r_data in raw:
        osm_id = r_data.get("osmId")
        if osm_id in seen_osm:
            continue
        seen_osm.add(osm_id)

        if r_data.get("latitude") is None:
            continue

        # Find nearest resort
        nearest_resort = ""
        min_dist = float("inf")
        for r in resorts:
            d = haversine_km(r_data["latitude"], r_data["longitude"], r["latitude"], r["longitude"])
            if d < min_dist:
                min_dist = d
                nearest_resort = r["name"]

        cleaned.append({
            "restaurantId": len(cleaned) + 1,
            "osmId": str(osm_id),
            "name": r_data.get("name", ""),
            "cuisine": r_data.get("cuisine", ""),
            "phone": r_data.get("phone", ""),
            "website": r_data.get("website", ""),
            "municipality": r_data.get("addr_city", ""),
            "address": f'{r_data.get("addr_street", "")} {r_data.get("addr_housenumber", "")}'.strip(),
            "postcode": r_data.get("addr_postcode", ""),
            "nearResort": nearest_resort if min_dist < 15 else "",
            "distanceToResort_km": round(min_dist, 1) if min_dist < 15 else None,
            "latitude": r_data["latitude"],
            "longitude": r_data["longitude"],
        })

    save_json(cleaned, "restaurants_cleaned.json")
    save_csv(cleaned, "restaurants_cleaned.csv",
             ["restaurantId", "osmId", "name", "cuisine", "phone", "website",
              "municipality", "address", "postcode",
              "nearResort", "distanceToResort_km", "latitude", "longitude"])
    return cleaned


# ============================================================
# Clean Rental Shops
# ============================================================
def clean_rental_shops(resorts):
    print("\n=== Cleaning Rental Shops ===")
    raw = load_json("rental_shops_raw.json")

    cleaned = []
    for s in raw:
        if s.get("latitude") is None:
            continue

        nearest_resort = ""
        min_dist = float("inf")
        for r in resorts:
            d = haversine_km(s["latitude"], s["longitude"], r["latitude"], r["longitude"])
            if d < min_dist:
                min_dist = d
                nearest_resort = r["name"]

        cleaned.append({
            "rentalId": len(cleaned) + 1,
            "osmId": str(s["osmId"]),
            "name": s.get("name", ""),
            "shopType": s.get("shop_type", ""),
            "phone": s.get("phone", ""),
            "website": s.get("website", ""),
            "municipality": s.get("addr_city", ""),
            "address": s.get("addr_street", ""),
            "postcode": s.get("addr_postcode", ""),
            "nearResort": nearest_resort if min_dist < 20 else "",
            "latitude": s["latitude"],
            "longitude": s["longitude"],
        })

    save_json(cleaned, "rental_shops_cleaned.json")
    save_csv(cleaned, "rental_shops_cleaned.csv",
             ["rentalId", "osmId", "name", "shopType", "phone", "website",
              "municipality", "address", "postcode", "nearResort",
              "latitude", "longitude"])
    return cleaned


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("Dataset Cleaning — Phase 2 Language Definition")
    print("=" * 60)

    resorts = clean_resorts()
    slopes = clean_slopes(resorts)
    lifts = clean_lifts(resorts)
    hotels = clean_hotels(resorts)
    restaurants = clean_restaurants(resorts)
    rental_shops = clean_rental_shops(resorts)

    print("\n" + "=" * 60)
    print("CLEANING SUMMARY")
    print("=" * 60)
    print(f"  Resorts:      {len(resorts)}")
    print(f"  Slopes:       {len(slopes)}")
    print(f"  Lifts:        {len(lifts)}")
    print(f"  Hotels:       {len(hotels)}")
    print(f"  Restaurants:  {len(restaurants)}")
    print(f"  Rental Shops: {len(rental_shops)}")
    print(f"\nAll cleaned data saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
