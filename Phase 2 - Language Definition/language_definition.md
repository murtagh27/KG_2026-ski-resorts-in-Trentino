# Phase 2 - Language Definition

## 3.1 Concept Identification — Finalized Language Terms

### Entity Types (Etypes)

| # | Informal Label (Phase 1) | Finalized Language Term | UKC/WordNet Alignment | Focus |
|---|--------------------------|------------------------|-----------------------|-------|
| 1 | SkiResort | SkiResort | ski_resort#n#1 → resort#n#1 → facility#n#1 → artifact#n#1 → entity#n#1 | Common |
| 2 | SkiSlope | SkiSlope | slope#n#3 → piste#n#1 → path#n#1 → way#n#6 → artifact#n#1 | Contextual |
| 3 | SkiLift | SkiLift | ski_lift#n#1 → lift#n#3 → conveyance#n#3 → artifact#n#1 | Contextual |
| 4 | SkiPass | SkiPass | pass#n#14 → ticket#n#1 → credential#n#1 → document#n#1 | Contextual |
| 5 | SkiSchool | SkiSchool | school#n#1 → educational_institution#n#1 → institution#n#1 | Contextual |
| 6 | Hotel | Hotel | hotel#n#1 → building#n#1 → structure#n#1 → artifact#n#1 | Core |
| 7 | Restaurant | Restaurant | restaurant#n#1 → building#n#1 → structure#n#1 → artifact#n#1 | Core |
| 8 | RentalShop | RentalShop | shop#n#1 → mercantile_establishment#n#1 → place_of_business#n#1 | Core |
| 9 | Municipality | Municipality | municipality#n#1 → administrative_district#n#1 → district#n#1 → region#n#1 | Common |
| 10 | Coordinate | Coordinate | coordinate#n#1 → value#n#1 → quantity#n#1 → measure#n#2 | Common |

### Object Properties

| # | Informal Label | Finalized Term | LTLO Parent Concept | Domain → Range |
|---|----------------|----------------|---------------------|----------------|
| 1 | hasSlope | hasSlope | has_part#v#1 → possess#v#1 | SkiResort → SkiSlope |
| 2 | hasLift | hasLift | has_part#v#1 → possess#v#1 | SkiResort → SkiLift |
| 3 | hasSkiPass | hasSkiPass | offer#v#2 → provide#v#1 | SkiResort → SkiPass |
| 4 | hasSkiSchool | hasSkiSchool | has_part#v#1 → possess#v#1 | SkiResort → SkiSchool |
| 5 | locatedIn | locatedIn | located_in#prep → spatial_relation#n#1 | SkiResort/Hotel/Restaurant/RentalShop → Municipality |
| 6 | nearResort | nearResort | near#adj#1 → close#adj#1 → proximate#adj#1 | Hotel/Restaurant/RentalShop → SkiResort |
| 7 | hasCoordinates | hasCoordinates | has_attribute#v#1 → possess#v#1 | All → Coordinate |

### Data Properties

| # | Informal Label | Finalized Term | Datatype | LTLO Parent | Domain |
|---|----------------|----------------|----------|-------------|--------|
| 1 | name | name | xsd:string | name#n#1 → label#n#1 → communication#n#1 | All |
| 2 | altitude | altitude | xsd:integer | altitude#n#1 → elevation#n#1 → height#n#1 | Hotel, Municipality |
| 3 | altitude_min | altitudeMin | xsd:integer | altitude#n#1 → elevation#n#1 | SkiResort |
| 4 | altitude_max | altitudeMax | xsd:integer | altitude#n#1 → elevation#n#1 | SkiResort |
| 5 | difficulty | difficulty | xsd:string | difficulty#n#3 → attribute#n#2 | SkiSlope |
| 6 | length_km | lengthKm | xsd:float | length#n#1 → measure#n#2 | SkiSlope |
| 7 | type | liftType | xsd:string | type#n#1 → kind#n#1 → category#n#1 | SkiLift |
| 8 | capacity | capacity | xsd:integer | capacity#n#1 → capability#n#1 | SkiLift |
| 9 | star_rating | starRating | xsd:string | rating#n#1 → evaluation#n#1 | Hotel |
| 10 | price | price | xsd:float | price#n#1 → cost#n#1 → value#n#1 | SkiPass, Hotel |
| 11 | cuisine | cuisine | xsd:string | cuisine#n#1 → cooking#n#1 | Restaurant |
| 12 | phone | phone | xsd:string | telephone_number#n#1 → number#n#1 | Hotel, Restaurant, RentalShop, SkiSchool |
| 13 | website | website | xsd:anyURI | website#n#1 → site#n#1 | SkiResort, Hotel, SkiSchool |
| 14 | email | email | xsd:string | email#n#1 → message#n#2 | Hotel |
| 15 | osmId | osmId | xsd:string | identifier#n#1 → symbol#n#1 | SkiSlope, SkiLift, Restaurant, Hotel, RentalShop |
| 16 | latitude | latitude | xsd:float | latitude#n#1 → angular_position#n#1 | Coordinate |
| 17 | longitude | longitude | xsd:float | longitude#n#1 → angular_position#n#1 | Coordinate |
| 18 | address | address | xsd:string | address#n#1 → direction#n#2 | Hotel, Restaurant, RentalShop |
| 19 | postcode | postcode | xsd:string | zip_code#n#1 → code#n#2 | Hotel, Restaurant, RentalShop |
| 20 | nBeds | numberOfBeds | xsd:integer | count#n#2 → number#n#2 | Hotel |
| 21 | duration | duration | xsd:string | duration#n#1 → time_period#n#1 | SkiPass |

## 3.2 LTLO Alignment

### Alignment Strategy

The Language Teleontology (LTLO) is based on the Universal Knowledge Core (UKC), which provides a multilingual, lexical-semantic hierarchy. Our alignment strategy:

1. **Direct alignment**: Terms that have a direct parent in the LTLO/WordNet hierarchy (e.g., hotel, restaurant, municipality)
2. **Indirect alignment via hypernym chain**: Terms requiring multiple hops up the hierarchy (e.g., SkiSlope → slope → piste → path → way → artifact)
3. **LTLO enrichment**: Domain-specific terms not found in UKC that require new entries (e.g., SkiPass, SkiSchool)

### LTLO Enrichment

The following terms required enrichment of the Language Teleontology, as no direct parent existed:

| Term | Enrichment Type | New Entry | Aligned To |
|------|----------------|-----------|------------|
| SkiResort | Composition | ski_resort#n#1 | resort#n#1 (existing) |
| SkiSlope | Composition | ski_slope#n#1 | slope#n#3 (existing) |
| SkiLift | Already exists | ski_lift#n#1 | lift#n#3 (existing) |
| SkiPass | New entry | ski_pass#n#1 | pass#n#14 / ticket#n#1 (existing) |
| SkiSchool | Composition | ski_school#n#1 | school#n#1 (existing) |
| RentalShop | Composition | rental_shop#n#1 | shop#n#1 (existing) |
| altitudeMin | New entry | minimum_altitude#n#1 | altitude#n#1 (existing) |
| altitudeMax | New entry | maximum_altitude#n#1 | altitude#n#1 (existing) |
| starRating | Composition | star_rating#n#1 | rating#n#1 (existing) |
| osmId | New entry | osm_identifier#n#1 | identifier#n#1 (existing) |

## 3.3 Dataset Filtering and Cleaning

### Cleaning Operations Applied

For each dataset, the following cleaning and formatting operations were performed:

1. **Ski Slopes**: Removed entries without names AND without coordinates. Standardized difficulty values to {novice, easy, intermediate, advanced, expert, freeride}. Removed duplicate osmIds.

2. **Ski Lifts**: Filtered out "station" type entries. Standardized lift type values to {chair_lift, gondola, cable_car, drag_lift, t-bar, platter, magic_carpet, mixed_lift}. Removed entries without coordinates.

3. **Ski Resorts**: Removed entries without names. Deduplicated by name (keeping the entry with most attributes filled).

4. **Restaurants**: Already filtered during collection (name required). Standardized cuisine values. Removed entries without coordinates.

5. **Hotels**: Already filtered during collection (name required). Standardized star ratings to 1-5 scale. Removed entries without coordinates.

6. **Rental Shops**: Small dataset (16 records) — manual review for completeness. All entries retained.

### Column Renaming (OSM → Finalized Terms)

| Dataset | OSM Column | Finalized Column |
|---------|------------|-----------------|
| All | lat/latitude | latitude |
| All | lon/longitude | longitude |
| Slopes | piste:difficulty | difficulty |
| Lifts | aerialway | liftType |
| Lifts | aerialway:capacity | capacity |
| Hotels | stars | starRating |
| Hotels | beds | numberOfBeds |
| Restaurants | addr:city | municipality |
| Hotels | addr:city | municipality |

## 3.4 Evaluation — Language Definition

### Etype Terms Evaluation

| Etype | Initially Considered | Finally Considered | Aligned to LTLO | Notes |
|-------|---------------------|-------------------|-----------------|-------|
| SkiResort | Yes | Yes | Yes (enriched) | Composed from resort#n#1 |
| SkiSlope | Yes | Yes | Yes (enriched) | Composed from slope#n#3 |
| SkiLift | Yes | Yes | Yes (existing) | Direct alignment |
| SkiPass | Yes | Yes | Yes (enriched) | New entry under ticket#n#1 |
| SkiSchool | Yes | Yes | Yes (enriched) | Composed from school#n#1 |
| Hotel | Yes | Yes | Yes (existing) | Direct alignment |
| Restaurant | Yes | Yes | Yes (existing) | Direct alignment |
| RentalShop | Yes | Yes | Yes (enriched) | Composed from shop#n#1 |
| Municipality | Yes | Yes | Yes (existing) | Direct alignment |
| Coordinate | Yes | Yes | Yes (existing) | Direct alignment |
| **Total** | **10** | **10** | **10 (6 enriched, 4 existing)** | |

### Object Property Terms Evaluation

| Property | Initially | Finally | Aligned to LTLO |
|----------|-----------|---------|-----------------|
| hasSlope | Yes | Yes | Yes (has_part) |
| hasLift | Yes | Yes | Yes (has_part) |
| hasSkiPass | Yes | Yes | Yes (offer) |
| hasSkiSchool | Yes | Yes | Yes (has_part) |
| locatedIn | Yes | Yes | Yes (located_in) |
| nearResort | Yes | Yes | Yes (near) |
| hasCoordinates | Yes | Yes | Yes (has_attribute) |
| **Total** | **7** | **7** | **7** |

### Data Property Terms Evaluation

| Property | Initially | Finally | Aligned to LTLO |
|----------|-----------|---------|-----------------|
| name | Yes | Yes | Yes |
| altitude/altitudeMin/altitudeMax | Yes | Yes | Yes (enriched) |
| difficulty | Yes | Yes | Yes |
| lengthKm | Yes | Yes | Yes |
| liftType | Yes | Yes | Yes |
| capacity | Yes | Yes | Yes |
| starRating | Yes | Yes | Yes (enriched) |
| price | Yes | Yes | Yes |
| cuisine | Yes | Yes | Yes |
| phone | Yes | Yes | Yes |
| website | Yes | Yes | Yes |
| email | Yes | Yes | Yes |
| osmId | Yes | Yes | Yes (enriched) |
| latitude | Yes | Yes | Yes |
| longitude | Yes | Yes | Yes |
| address | Yes | Yes | Yes |
| postcode | Yes | Yes | Yes |
| numberOfBeds | Yes | Yes | Yes |
| duration | Yes | Yes | Yes |
| **Total** | **19** | **19** | **19** |

### Changes from Purpose Definition

No changes were required to the Purpose Definition phase at this stage. All 10 etypes and their properties were confirmed as viable during language finalization.
