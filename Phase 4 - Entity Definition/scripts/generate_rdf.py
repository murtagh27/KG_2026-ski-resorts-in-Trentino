"""
Generate RDF (Turtle) from cleaned datasets.
Maps each dataset to the ontology defined in Phase 3.
Produces individual .ttl files per dataset + a merged KG file.
"""

import json
import os
import re

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                        "Phase 2 - Language Definition", "data")
RDF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rdf")
os.makedirs(RDF_DIR, exist_ok=True)

BASE_URI = "http://skiresorts-trentino.2026.kg/resource/"
ONTOLOGY_URI = "http://skiresorts-trentino.2026.kg/ontology#"

PREFIXES = """@prefix ski: <http://skiresorts-trentino.2026.kg/ontology#> .
@prefix res: <http://skiresorts-trentino.2026.kg/resource/> .
@prefix schema: <http://schema.org/> .
@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

"""


def load_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_uri(name):
    """Convert a name to a safe URI fragment."""
    if not name:
        return "unknown"
    s = re.sub(r'[^a-zA-Z0-9_-]', '_', name.strip())
    s = re.sub(r'_+', '_', s).strip('_')
    return s[:80] if s else "unknown"


def escape_literal(val):
    """Escape a string for Turtle literal."""
    if val is None:
        return None
    s = str(val).replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
    return s


def triple_str(subject, predicate, obj_literal, datatype=None):
    """Create a Turtle triple with a literal object."""
    if obj_literal is None or str(obj_literal).strip() == "":
        return ""
    escaped = escape_literal(obj_literal)
    if datatype:
        return f'    {predicate} "{escaped}"^^{datatype} ;\n'
    return f'    {predicate} "{escaped}" ;\n'


def triple_uri(subject, predicate, obj_uri):
    """Create a Turtle triple with a URI object."""
    if not obj_uri:
        return ""
    return f'    {predicate} {obj_uri} ;\n'


# ============================================================
# Generate RDF for each dataset
# ============================================================

def gen_resorts():
    print("Generating RDF: Ski Resorts...")
    data = load_json("ski_resorts_cleaned.json")
    ttl = PREFIXES

    for r in data:
        uri = f'res:resort_{r["resortId"]}'
        ttl += f'{uri} a ski:SkiResort ;\n'
        ttl += triple_str(uri, 'ski:name', r.get("name"))
        ttl += triple_str(uri, 'ski:osmId', r.get("osmId"))
        ttl += triple_str(uri, 'ski:phone', r.get("phone"))
        if r.get("website"):
            ttl += f'    ski:website <{escape_literal(r["website"])}> ;\n'
        if r.get("municipality"):
            muni_uri = f'res:municipality_{safe_uri(r["municipality"])}'
            ttl += triple_uri(uri, 'ski:locatedIn', muni_uri)
        if r.get("latitude") is not None:
            coord_uri = f'res:coord_resort_{r["resortId"]}'
            ttl += triple_uri(uri, 'ski:hasCoordinates', coord_uri)
        # Close the resource
        ttl = ttl.rstrip(' ;\n') + ' .\n\n'

        # Coordinate entity
        if r.get("latitude") is not None:
            coord_uri = f'res:coord_resort_{r["resortId"]}'
            ttl += f'{coord_uri} a ski:Coordinate ;\n'
            ttl += f'    ski:latitude "{r["latitude"]}"^^xsd:float ;\n'
            ttl += f'    ski:longitude "{r["longitude"]}"^^xsd:float .\n\n'

    filepath = os.path.join(RDF_DIR, "ski_resorts.ttl")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(ttl)
    print(f"  -> {len(data)} resorts written to ski_resorts.ttl")
    return data


def gen_slopes(resorts):
    print("Generating RDF: Ski Slopes...")
    data = load_json("ski_slopes_cleaned.json")
    ttl = PREFIXES

    # Build resort name -> URI map
    resort_map = {}
    for r in resorts:
        if r.get("name"):
            resort_map[r["name"].lower()] = f'res:resort_{r["resortId"]}'

    for s in data:
        uri = f'res:slope_{s["slopeId"]}'
        ttl += f'{uri} a ski:SkiSlope ;\n'
        ttl += triple_str(uri, 'ski:name', s.get("name"))
        ttl += triple_str(uri, 'ski:osmId', str(s.get("osmId")))
        ttl += triple_str(uri, 'ski:difficulty', s.get("difficulty"))
        ttl += triple_str(uri, 'ski:ref', s.get("ref")) if s.get("ref") else ""

        # Link to resort
        resort_name = s.get("resort", "").lower()
        if resort_name and resort_name in resort_map:
            resort_uri = resort_map[resort_name]
            ttl += triple_uri(uri, 'ski:nearResort', resort_uri)

        if s.get("latitude") is not None:
            coord_uri = f'res:coord_slope_{s["slopeId"]}'
            ttl += triple_uri(uri, 'ski:hasCoordinates', coord_uri)

        ttl = ttl.rstrip(' ;\n') + ' .\n\n'

        if s.get("latitude") is not None:
            coord_uri = f'res:coord_slope_{s["slopeId"]}'
            ttl += f'{coord_uri} a ski:Coordinate ;\n'
            ttl += f'    ski:latitude "{s["latitude"]}"^^xsd:float ;\n'
            ttl += f'    ski:longitude "{s["longitude"]}"^^xsd:float .\n\n'

    filepath = os.path.join(RDF_DIR, "ski_slopes.ttl")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(ttl)
    print(f"  -> {len(data)} slopes written to ski_slopes.ttl")


def gen_lifts(resorts):
    print("Generating RDF: Ski Lifts...")
    data = load_json("ski_lifts_cleaned.json")
    ttl = PREFIXES

    resort_map = {}
    for r in resorts:
        if r.get("name"):
            resort_map[r["name"].lower()] = f'res:resort_{r["resortId"]}'

    for l in data:
        uri = f'res:lift_{l["liftId"]}'
        ttl += f'{uri} a ski:SkiLift ;\n'
        ttl += triple_str(uri, 'ski:name', l.get("name"))
        ttl += triple_str(uri, 'ski:osmId', str(l.get("osmId")))
        ttl += triple_str(uri, 'ski:liftType', l.get("liftType"))
        if l.get("capacity"):
            ttl += triple_str(uri, 'ski:capacity', l.get("capacity"), "xsd:integer")

        resort_name = l.get("resort", "").lower()
        if resort_name and resort_name in resort_map:
            ttl += triple_uri(uri, 'ski:nearResort', resort_map[resort_name])

        if l.get("latitude") is not None:
            coord_uri = f'res:coord_lift_{l["liftId"]}'
            ttl += triple_uri(uri, 'ski:hasCoordinates', coord_uri)

        ttl = ttl.rstrip(' ;\n') + ' .\n\n'

        if l.get("latitude") is not None:
            coord_uri = f'res:coord_lift_{l["liftId"]}'
            ttl += f'{coord_uri} a ski:Coordinate ;\n'
            ttl += f'    ski:latitude "{l["latitude"]}"^^xsd:float ;\n'
            ttl += f'    ski:longitude "{l["longitude"]}"^^xsd:float .\n\n'

    filepath = os.path.join(RDF_DIR, "ski_lifts.ttl")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(ttl)
    print(f"  -> {len(data)} lifts written to ski_lifts.ttl")


def gen_hotels():
    print("Generating RDF: Hotels...")
    data = load_json("hotels_cleaned.json")
    ttl = PREFIXES

    for h in data:
        uri = f'res:hotel_{h["hotelId"]}'
        ttl += f'{uri} a ski:Hotel ;\n'
        ttl += triple_str(uri, 'ski:name', h.get("name"))
        ttl += triple_str(uri, 'ski:osmId', str(h.get("osmId")))
        ttl += triple_str(uri, 'ski:starRating', h.get("starRating"))
        if h.get("numberOfBeds"):
            ttl += triple_str(uri, 'ski:numberOfBeds', h.get("numberOfBeds"), "xsd:integer")
        ttl += triple_str(uri, 'ski:phone', h.get("phone"))
        ttl += triple_str(uri, 'ski:email', h.get("email"))
        if h.get("website"):
            ttl += f'    ski:website <{escape_literal(h["website"])}> ;\n'
        ttl += triple_str(uri, 'ski:address', h.get("address"))
        ttl += triple_str(uri, 'ski:postcode', h.get("postcode"))

        if h.get("municipality"):
            muni_uri = f'res:municipality_{safe_uri(h["municipality"])}'
            ttl += triple_uri(uri, 'ski:locatedIn', muni_uri)

        if h.get("nearResort"):
            resort_uri = f'res:resort_{safe_uri(h["nearResort"])}'
            ttl += triple_uri(uri, 'ski:nearResort', resort_uri)

        if h.get("latitude") is not None:
            coord_uri = f'res:coord_hotel_{h["hotelId"]}'
            ttl += triple_uri(uri, 'ski:hasCoordinates', coord_uri)

        ttl = ttl.rstrip(' ;\n') + ' .\n\n'

        if h.get("latitude") is not None:
            coord_uri = f'res:coord_hotel_{h["hotelId"]}'
            ttl += f'{coord_uri} a ski:Coordinate ;\n'
            ttl += f'    ski:latitude "{h["latitude"]}"^^xsd:float ;\n'
            ttl += f'    ski:longitude "{h["longitude"]}"^^xsd:float .\n\n'

    filepath = os.path.join(RDF_DIR, "hotels.ttl")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(ttl)
    print(f"  -> {len(data)} hotels written to hotels.ttl")


def gen_restaurants():
    print("Generating RDF: Restaurants...")
    data = load_json("restaurants_cleaned.json")
    ttl = PREFIXES

    for r in data:
        uri = f'res:restaurant_{r["restaurantId"]}'
        ttl += f'{uri} a ski:Restaurant ;\n'
        ttl += triple_str(uri, 'ski:name', r.get("name"))
        ttl += triple_str(uri, 'ski:osmId', str(r.get("osmId")))
        ttl += triple_str(uri, 'ski:cuisine', r.get("cuisine"))
        ttl += triple_str(uri, 'ski:phone', r.get("phone"))
        if r.get("website"):
            ttl += f'    ski:website <{escape_literal(r["website"])}> ;\n'
        ttl += triple_str(uri, 'ski:address', r.get("address"))
        ttl += triple_str(uri, 'ski:postcode', r.get("postcode"))

        if r.get("municipality"):
            muni_uri = f'res:municipality_{safe_uri(r["municipality"])}'
            ttl += triple_uri(uri, 'ski:locatedIn', muni_uri)

        if r.get("nearResort"):
            resort_uri = f'res:resort_{safe_uri(r["nearResort"])}'
            ttl += triple_uri(uri, 'ski:nearResort', resort_uri)

        if r.get("latitude") is not None:
            coord_uri = f'res:coord_restaurant_{r["restaurantId"]}'
            ttl += triple_uri(uri, 'ski:hasCoordinates', coord_uri)

        ttl = ttl.rstrip(' ;\n') + ' .\n\n'

        if r.get("latitude") is not None:
            coord_uri = f'res:coord_restaurant_{r["restaurantId"]}'
            ttl += f'{coord_uri} a ski:Coordinate ;\n'
            ttl += f'    ski:latitude "{r["latitude"]}"^^xsd:float ;\n'
            ttl += f'    ski:longitude "{r["longitude"]}"^^xsd:float .\n\n'

    filepath = os.path.join(RDF_DIR, "restaurants.ttl")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(ttl)
    print(f"  -> {len(data)} restaurants written to restaurants.ttl")


def gen_rental_shops():
    print("Generating RDF: Rental Shops...")
    data = load_json("rental_shops_cleaned.json")
    ttl = PREFIXES

    for s in data:
        uri = f'res:rental_{s["rentalId"]}'
        ttl += f'{uri} a ski:RentalShop ;\n'
        ttl += triple_str(uri, 'ski:name', s.get("name"))
        ttl += triple_str(uri, 'ski:osmId', str(s.get("osmId")))
        ttl += triple_str(uri, 'ski:phone', s.get("phone"))
        if s.get("website"):
            ttl += f'    ski:website <{escape_literal(s["website"])}> ;\n'

        if s.get("municipality"):
            muni_uri = f'res:municipality_{safe_uri(s["municipality"])}'
            ttl += triple_uri(uri, 'ski:locatedIn', muni_uri)

        if s.get("nearResort"):
            resort_uri = f'res:resort_{safe_uri(s["nearResort"])}'
            ttl += triple_uri(uri, 'ski:nearResort', resort_uri)

        if s.get("latitude") is not None:
            coord_uri = f'res:coord_rental_{s["rentalId"]}'
            ttl += triple_uri(uri, 'ski:hasCoordinates', coord_uri)

        ttl = ttl.rstrip(' ;\n') + ' .\n\n'

        if s.get("latitude") is not None:
            coord_uri = f'res:coord_rental_{s["rentalId"]}'
            ttl += f'{coord_uri} a ski:Coordinate ;\n'
            ttl += f'    ski:latitude "{s["latitude"]}"^^xsd:float ;\n'
            ttl += f'    ski:longitude "{s["longitude"]}"^^xsd:float .\n\n'

    filepath = os.path.join(RDF_DIR, "rental_shops.ttl")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(ttl)
    print(f"  -> {len(data)} rental shops written to rental_shops.ttl")


def merge_all():
    """Merge all individual TTL files into one KG file."""
    print("\nMerging all RDF files into unified KG...")
    merged = PREFIXES
    merged += "# ============================================================\n"
    merged += "# Unified Knowledge Graph: Ski Resorts in Trentino\n"
    merged += "# ============================================================\n\n"

    files = ["ski_resorts.ttl", "ski_slopes.ttl", "ski_lifts.ttl",
             "hotels.ttl", "restaurants.ttl", "rental_shops.ttl"]

    for fname in files:
        filepath = os.path.join(RDF_DIR, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # Remove duplicate prefix declarations
        lines = content.split('\n')
        body_lines = [l for l in lines if not l.startswith('@prefix')]
        merged += f"# --- {fname} ---\n"
        merged += '\n'.join(body_lines) + '\n\n'

    filepath = os.path.join(RDF_DIR, "ski_resorts_trentino_kg.ttl")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(merged)

    # Count triples (approximate)
    triple_count = merged.count(' .\n') + merged.count(' ;\n')
    print(f"  -> Merged KG saved to ski_resorts_trentino_kg.ttl")
    print(f"  -> Approximate triple count: {triple_count}")


def main():
    print("=" * 60)
    print("RDF Generation — Phase 4 Entity Definition")
    print("=" * 60)

    resorts = gen_resorts()
    gen_slopes(resorts)
    gen_lifts(resorts)
    gen_hotels()
    gen_restaurants()
    gen_rental_shops()
    merge_all()


if __name__ == "__main__":
    main()
