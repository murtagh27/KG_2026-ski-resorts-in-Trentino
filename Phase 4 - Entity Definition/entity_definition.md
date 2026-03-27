# Phase 4 - Entity Definition

## 5.1 Overview and Objectives

In this phase, we merge the knowledge layer (ontology/teleology from Phase 3) with the data layer (cleaned datasets from Phase 2) to produce a structured Knowledge Graph. The process involves:

1. **Producer process**: Mapping each individual dataset to the ontology structure
2. **Consumer process**: Merging all dataset mappings into a single unified KG

## 5.2 Entity Identification

For each dataset, entities were identified using unique identifiers:

| Dataset | Entity Type | ID Field | Total Entities |
|---------|-------------|----------|----------------|
| Ski Resorts | ski:SkiResort | resortId (1-222) | 222 |
| Ski Slopes | ski:SkiSlope | slopeId (1-2792) | 2,792 |
| Ski Lifts | ski:SkiLift | liftId (1-5677) | 5,677 |
| Hotels | ski:Hotel | hotelId (1-3393) | 3,393 |
| Restaurants | ski:Restaurant | restaurantId (1-3896) | 3,896 |
| Rental Shops | ski:RentalShop | rentalId (1-16) | 16 |
| Coordinates | ski:Coordinate | per-entity coord | ~15,996 |
| **Total unique entities** | | | **~31,992** |

## 5.3 Data Mapping

Each dataset was mapped to the teleology using a Python script (`generate_rdf.py`) that acts as our Karma-equivalent mapping tool. The mapping process:

1. **Individual dataset mapping**: Each cleaned CSV/JSON dataset is read and mapped to the corresponding OWL class and properties
2. **URI generation**: Entities are assigned URIs following the pattern `res:{type}_{id}` (e.g., `res:resort_1`, `res:slope_42`)
3. **Coordinate entities**: Created as separate entities (`res:coord_{type}_{id}`) linked via `ski:hasCoordinates`
4. **Cross-dataset linking**:
   - Slopes and lifts linked to nearest resort via `ski:nearResort` (within 15km threshold)
   - Hotels and restaurants linked to nearest resort via `ski:nearResort` (within 20km and 15km respectively)
   - All location entities linked to municipalities via `ski:locatedIn`

## 5.4 Entity Mapping — Cross-Dataset Composition

The consumer process merges all individual RDF files into a unified Knowledge Graph (`ski_resorts_trentino_kg.ttl`).

### Cross-dataset entity matching:
- **Resort ↔ Slopes**: Slopes associated to resorts via spatial proximity (haversine distance < 15km) and/or OSM `piste:name` attribute
- **Resort ↔ Lifts**: Lifts associated to resorts via spatial proximity (< 15km) and/or OSM `name:resort` attribute
- **Resort ↔ Hotels/Restaurants/Shops**: Facilities linked via `ski:nearResort` when within proximity threshold
- **Municipality matching**: All entities with `addr:city` mapped to `ski:Municipality` entities

## 5.5 Phase Outcomes

| Metric | Value |
|--------|-------|
| Total entities | ~31,992 |
| Total RDF triples | ~151,744 |
| Individual TTL files | 6 |
| Merged KG file | ski_resorts_trentino_kg.ttl |
| Ontology file | ski_resorts_trentino.ttl |
| Etypes populated | 7 (SkiResort, SkiSlope, SkiLift, Hotel, Restaurant, RentalShop, Coordinate) |
| Etypes not populated | 3 (SkiPass, SkiSchool, Municipality — data not available from OSM) |

## 5.6 Decisions and Reflections

### Strengths
- Successful mapping of 6 datasets to the teleology, producing over 151K triples
- Cross-dataset linking via spatial proximity worked well for associating facilities with resorts
- URI naming convention is systematic and supports entity resolution

### Challenges
- **SkiPass and SkiSchool**: No structured data available from OSM. These entities exist in the ontology but are not populated in the KG. Future work could scrape resort websites for this data.
- **Municipality**: While municipality names appear as data properties on other entities, dedicated Municipality entities with population/altitude were not created from external sources. This could be enriched from ISTAT data.
- **Entity matching across datasets**: Spatial proximity is an approximation — some slopes/lifts may be incorrectly associated with resorts, especially in areas where multiple resorts are close together.
- **Rental shops**: Only 16 records from OSM — significantly less data than other entity types.

### Evaluation

| Metric | Initially Considered | Finally Produced |
|--------|---------------------|-----------------|
| Entity types | 10 | 7 populated + 3 in ontology only |
| Ski resorts | 295 (raw) | 222 (cleaned, deduplicated) |
| Ski slopes | 2,792 | 2,792 |
| Ski lifts | 5,677 | 5,677 |
| Hotels | 3,393 | 3,393 |
| Restaurants | 3,896 | 3,896 |
| Rental shops | 16 | 16 |
| Cross-dataset links | N/A | Computed via proximity |

### Changes from Previous Phases
No changes were required to the Purpose, Language, or Knowledge Definition phases during entity mapping. The teleology structure was sufficient to model all available data.
