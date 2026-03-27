# Information Gathering Report

## 1. Knowledge Sources

In this phase, our goal is to gather high-quality, relevant information to support the construction of our Knowledge Graph, ensuring alignment with the purpose and scope defined earlier. This involves a meticulous selection of data sources and content that can accurately populate our KG with meaningful, structured information.

To address the project's knowledge resource needs, we used mainly **OpenStreetMap**, which provides a comprehensive set of predefined schemas for structured geospatial data. **Schema.org** was used as reference for standardized entity schemas (SkiResort, LodgingBusiness, FoodEstablishment). Together with OSM, these are collaborative, community-driven initiatives aimed at creating, maintaining, and promoting flexible schemas that can be applied across diverse domains.

All queries performed on OpenStreetMap data were run via **Overpass-Turbo** (overpass-turbo.eu). Overpass Turbo is a web-based tool designed to help users interactively query and visualize data from OSM, allowing custom location-based queries to extract specific types of geospatial data.

Due to the large amount of data gathered from OSM, we inserted the `osmId` in all entity types containing data gained from it, to enhance reusability.

### Knowledge Layer Sources

| Source | Type | Description | Classification |
|--------|------|-------------|----------------|
| Schema.org SkiResort | Schema reference | Formal schema for ski resort entities | Common |
| Schema.org LodgingBusiness | Schema reference | Formal schema for hotel/accommodation entities | Common |
| Schema.org FoodEstablishment | Schema reference | Formal schema for restaurant entities | Common |
| OpenStreetMap Piste Schema | Schema reference | OSM tags for piste:type, piste:difficulty | Contextual |
| OpenStreetMap Aerialway Schema | Schema reference | OSM tags for aerialway types | Contextual |
| Geospatial Ontology (Subhashis) | Reference ontology | Geographic coordinate and location modeling | Common |

### Data Layer Sources

| Source | URL | Description | Classification |
|--------|-----|-------------|----------------|
| OpenStreetMap (via Overpass API) | overpass-api.de | Primary source for all geospatial data | Core |
| Open Data Trentino | dati.trentino.it | Official provincial open data portal | Core |
| KGE Catalog | datascientiafoundation.github.io/LiveData-KGE/datasets/ | Reference datasets from prior KGE projects | Common |

## 2. Ski Slopes Resource

The **Ski Slopes Resource** is a **data value dataset** that provides information about ski slopes (downhill pistes) within the Trentino-Alto Adige/Sudtirol region.

The dataset is composed from the output of a query performed on OSM. The data follows the OSM piste schema which provides standardized tags for winter sports infrastructure.

**Overpass-Turbo query:**
```
[out:json][timeout:90];
area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
(
  way["piste:type"="downhill"](area.trentino);
  relation["piste:type"="downhill"](area.trentino);
);
out center tags;
```

**Records collected: 2,792**

Key attributes in the dataset are:
- **id** (integer): internal identifier
- **osmId** (string): original ID from OpenStreetMap for reusability
- **name** (string): name of the slope
- **difficulty** (string): can be *novice*, *easy*, *intermediate*, *advanced*, *expert*, *freeride*
- **resort** (string): associated ski resort name
- **ref** (string): slope reference number
- **lit** (string): whether the slope has night lighting
- **grooming** (string): grooming status
- **latitude** (float): center latitude
- **longitude** (float): center longitude

**Classification:** Contextual (ski-specific, directly tied to the project purpose)

## 3. Ski Lifts Resource

The **Ski Lifts Resource** is a **data value dataset** that provides information about aerial lift systems (chairlifts, gondolas, cable cars, drag lifts) within the Trentino region.

**Overpass-Turbo query:**
```
[out:json][timeout:90];
area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
(
  way["aerialway"](area.trentino);
  node["aerialway"](area.trentino);
);
out center tags;
```

**Records collected: 5,677** (after filtering out station nodes)

Key attributes:
- **id** (integer)
- **osmId** (string): OpenStreetMap ID
- **name** (string): name of the lift
- **type** (string): *chair_lift*, *gondola*, *cable_car*, *drag_lift*, *t-bar*, *platter*, *magic_carpet*
- **capacity** (string): persons per hour
- **occupancy** (string): persons per carrier
- **duration** (string): ride duration
- **resort** (string): associated resort
- **latitude**, **longitude** (float): center coordinates

**Classification:** Contextual

## 4. Ski Resorts Resource

The **Ski Resorts Resource** provides information about ski resort areas and winter sports facilities.

**Overpass-Turbo query:**
```
[out:json][timeout:90];
area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
(
  node["sport"="skiing"](area.trentino);
  way["sport"="skiing"](area.trentino);
  relation["sport"="skiing"](area.trentino);
  node["landuse"="winter_sports"](area.trentino);
  way["landuse"="winter_sports"](area.trentino);
  node["tourism"="winter_sports"](area.trentino);
  way["tourism"="winter_sports"](area.trentino);
);
out center tags;
```

**Records collected: 295**

Key attributes:
- **id** (integer)
- **osmId** (string)
- **name** (string): resort name
- **website** (string): official website
- **phone** (string): contact phone
- **operator** (string): operating company
- **municipality** (string): municipality name
- **latitude**, **longitude** (float)

**Classification:** Common (central entity connecting all other resources)

## 5. Restaurants Resource

The **Restaurant Resource** is a **data value dataset** providing information on restaurants within Trentino.

The final dataset is the output of a query on OSM, filtered to include only restaurants with a name attribute.

**Overpass-Turbo query:**
```
[out:json][timeout:120];
area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
(
  node["amenity"="restaurant"](area.trentino);
  way["amenity"="restaurant"](area.trentino);
);
out center tags;
```

**Records collected: 3,896** (filtered from 4,009 to exclude unnamed entries)

Key attributes:
- **id** (integer)
- **osmId** (string)
- **name** (string)
- **cuisine** (string): type of cuisine (italian, regional, pizza, etc.)
- **phone** (string)
- **website** (string)
- **addr_city** (string): municipality
- **addr_street** (string)
- **addr_housenumber** (string)
- **addr_postcode** (string)
- **latitude**, **longitude** (float)

**Classification:** Core (satisfies tourist dining needs, connected to resorts via proximity)

## 6. Hotels Resource

The **Hotel Resource** is a **data value dataset** providing information on hotels within Trentino.

**Overpass-Turbo query:**
```
[out:json][timeout:120];
area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
(
  node["tourism"="hotel"](area.trentino);
  way["tourism"="hotel"](area.trentino);
);
out center tags;
```

**Records collected: 3,393** (filtered from 3,459 to exclude unnamed entries)

Key attributes:
- **id** (integer)
- **osmId** (string)
- **name** (string)
- **stars** (string): star rating (1-5)
- **rooms** (integer): number of rooms
- **beds** (integer): number of beds
- **phone** (string)
- **email** (string)
- **website** (string)
- **addr_city** (string)
- **addr_street**, **addr_housenumber**, **addr_postcode** (string)
- **latitude**, **longitude** (float)

**Classification:** Core

## 7. Ski Rental Shops Resource

The **Ski Rental Shops Resource** provides information about ski equipment rental shops.

**Overpass-Turbo query:**
```
[out:json][timeout:90];
area["name"="Trentino-Alto Adige/Südtirol"]->.trentino;
(
  node["shop"="ski_rental"](area.trentino);
  way["shop"="ski_rental"](area.trentino);
  node["shop"="ski"](area.trentino);
  way["shop"="ski"](area.trentino);
);
out center tags;
```

**Records collected: 16**

Note: Similar to the L12-2 project experience, we faced limited data availability for ski rental shops on OSM. Only 16 shops were found. This may need to be supplemented with manual data collection from Google Maps or resort websites in later phases.

Key attributes:
- **id** (integer)
- **osmId** (string)
- **name** (string)
- **shop_type** (string): "ski_rental" or "ski"
- **phone** (string)
- **website** (string)
- **addr_city**, **addr_street**, **addr_postcode** (string)
- **latitude**, **longitude** (float)

**Classification:** Core

## 8. Data Collection Summary

| Dataset | Source | Records | Classification | Schema Reference |
|---------|--------|---------|----------------|-----------------|
| Ski Slopes | OSM (Overpass) | 2,792 | Contextual | OSM Piste Schema |
| Ski Lifts | OSM (Overpass) | 5,677 | Contextual | OSM Aerialway Schema |
| Ski Resorts | OSM (Overpass) | 295 | Common | Schema.org SkiResort |
| Restaurants | OSM (Overpass) | 3,896 | Core | Schema.org FoodEstablishment |
| Hotels | OSM (Overpass) | 3,393 | Core | Schema.org LodgingBusiness |
| Rental Shops | OSM (Overpass) | 16 | Core | OSM Shop Schema |
| **Total** | | **16,069** | | |

## 9. Report

In this phase of data gathering, we collected a substantial amount of geospatial data from OpenStreetMap, totaling over 16,000 records across 6 entity types. The primary source (OSM via Overpass API) provided rich, structured data with geographic coordinates for all entities.

**Strengths:**
- Large, comprehensive datasets for slopes (2,792), lifts (5,677), restaurants (3,896), and hotels (3,393)
- All records include geographic coordinates, enabling spatial queries and proximity calculations
- OSM IDs preserved for reusability and cross-referencing
- Standardized schemas (OSM piste, aerialway) provide consistency

**Challenges:**
- Ski rental shop data is very limited (only 16 records) — will need supplementation
- Some datasets have sparse attribute coverage (e.g., many hotels lack star ratings)
- The `resort` field in slopes/lifts is often empty, requiring spatial association in later phases
- Data quality varies — some entries lack names or have incomplete addresses
- SkiPass and SkiSchool data is not available on OSM and will need to be sourced from resort websites or official tourism portals

**Next steps:**
- Clean and format datasets (Phase 2)
- Associate slopes and lifts with resorts via spatial proximity
- Supplement rental shop data with manual collection
- Source ski pass pricing and ski school data from official resort websites
