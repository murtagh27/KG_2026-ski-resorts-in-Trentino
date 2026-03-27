# Phase 3 - Knowledge Definition

## 4.1 Teleology Definition

The Teleology defines the formal knowledge structure for our ski resorts KG. We compose the teleology from existing ontology fragments (Schema.org, OSM, Geospatial) and enrich with ski-specific fragments where needed.

### Ontology Fragments Used

| Fragment Source | Etypes Reused | Properties Reused | Notes |
|-----------------|---------------|-------------------|-------|
| Schema.org (SkiResort) | SkiResort | name, url, telephone, geo, address | Extended with altitude_min/max, total_slopes |
| Schema.org (LodgingBusiness) | Hotel | name, starRating, numberOfBeds, address, telephone, email | Used as-is with minor additions |
| Schema.org (FoodEstablishment) | Restaurant | name, servesCuisine, address, telephone | Used as-is |
| Schema.org (Store) | RentalShop | name, address, telephone | Extended for ski rental specifics |
| OSM Piste Schema | SkiSlope | piste:type, piste:difficulty, piste:name | Mapped to our language terms |
| OSM Aerialway Schema | SkiLift | aerialway, aerialway:capacity | Mapped to liftType, capacity |
| Geospatial Ontology | Coordinate, Municipality | latitude, longitude, name | Used as-is |
| **Custom (new)** | SkiPass | name, price, duration, type | Created from scratch — no existing fragment |
| **Custom (new)** | SkiSchool | name, phone, website, languages | Created from scratch — no existing fragment |

### Teleology Structure (OWL-compatible)

```
# Namespace: http://skiresorts-trentino.2026.kg/ontology#

@prefix ski: <http://skiresorts-trentino.2026.kg/ontology#> .
@prefix schema: <http://schema.org/> .
@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

### Classes (Etypes)

ski:SkiResort a owl:Class ;
    rdfs:subClassOf schema:SkiResort ;
    rdfs:label "Ski Resort" .

ski:SkiSlope a owl:Class ;
    rdfs:label "Ski Slope" ;
    rdfs:comment "A downhill ski slope/piste at a resort" .

ski:SkiLift a owl:Class ;
    rdfs:label "Ski Lift" ;
    rdfs:comment "An aerial lift system (chairlift, gondola, cable car, drag lift)" .

ski:SkiPass a owl:Class ;
    rdfs:label "Ski Pass" ;
    rdfs:comment "A ticket/pass for accessing ski facilities" .

ski:SkiSchool a owl:Class ;
    rdfs:subClassOf schema:EducationalOrganization ;
    rdfs:label "Ski School" .

ski:Hotel a owl:Class ;
    rdfs:subClassOf schema:LodgingBusiness ;
    rdfs:label "Hotel" .

ski:Restaurant a owl:Class ;
    rdfs:subClassOf schema:FoodEstablishment ;
    rdfs:label "Restaurant" .

ski:RentalShop a owl:Class ;
    rdfs:subClassOf schema:Store ;
    rdfs:label "Rental Shop" .

ski:Municipality a owl:Class ;
    rdfs:subClassOf schema:AdministrativeArea ;
    rdfs:label "Municipality" .

ski:Coordinate a owl:Class ;
    rdfs:label "Coordinate" ;
    rdfs:comment "WGS84 geographic coordinate pair" .

### Object Properties

ski:hasSlope a owl:ObjectProperty ;
    rdfs:domain ski:SkiResort ;
    rdfs:range ski:SkiSlope .

ski:hasLift a owl:ObjectProperty ;
    rdfs:domain ski:SkiResort ;
    rdfs:range ski:SkiLift .

ski:hasSkiPass a owl:ObjectProperty ;
    rdfs:domain ski:SkiResort ;
    rdfs:range ski:SkiPass .

ski:hasSkiSchool a owl:ObjectProperty ;
    rdfs:domain ski:SkiResort ;
    rdfs:range ski:SkiSchool .

ski:locatedIn a owl:ObjectProperty ;
    rdfs:range ski:Municipality .

ski:nearResort a owl:ObjectProperty ;
    rdfs:range ski:SkiResort .

ski:hasCoordinates a owl:ObjectProperty ;
    rdfs:range ski:Coordinate .

### Data Properties

ski:name a owl:DatatypeProperty ; rdfs:range xsd:string .
ski:osmId a owl:DatatypeProperty ; rdfs:range xsd:string .
ski:altitudeMin a owl:DatatypeProperty ; rdfs:domain ski:SkiResort ; rdfs:range xsd:integer .
ski:altitudeMax a owl:DatatypeProperty ; rdfs:domain ski:SkiResort ; rdfs:range xsd:integer .
ski:difficulty a owl:DatatypeProperty ; rdfs:domain ski:SkiSlope ; rdfs:range xsd:string .
ski:lengthKm a owl:DatatypeProperty ; rdfs:domain ski:SkiSlope ; rdfs:range xsd:float .
ski:liftType a owl:DatatypeProperty ; rdfs:domain ski:SkiLift ; rdfs:range xsd:string .
ski:capacity a owl:DatatypeProperty ; rdfs:domain ski:SkiLift ; rdfs:range xsd:integer .
ski:starRating a owl:DatatypeProperty ; rdfs:domain ski:Hotel ; rdfs:range xsd:string .
ski:numberOfBeds a owl:DatatypeProperty ; rdfs:domain ski:Hotel ; rdfs:range xsd:integer .
ski:price a owl:DatatypeProperty ; rdfs:range xsd:float .
ski:cuisine a owl:DatatypeProperty ; rdfs:domain ski:Restaurant ; rdfs:range xsd:string .
ski:phone a owl:DatatypeProperty ; rdfs:range xsd:string .
ski:email a owl:DatatypeProperty ; rdfs:domain ski:Hotel ; rdfs:range xsd:string .
ski:website a owl:DatatypeProperty ; rdfs:range xsd:anyURI .
ski:address a owl:DatatypeProperty ; rdfs:range xsd:string .
ski:postcode a owl:DatatypeProperty ; rdfs:range xsd:string .
ski:latitude a owl:DatatypeProperty ; rdfs:domain ski:Coordinate ; rdfs:range xsd:float .
ski:longitude a owl:DatatypeProperty ; rdfs:domain ski:Coordinate ; rdfs:range xsd:float .
ski:duration a owl:DatatypeProperty ; rdfs:domain ski:SkiPass ; rdfs:range xsd:string .
```

## 4.2 Knowledge Teleontology (KTLO) Alignment

### Etype Alignment to KTLO

| Etype | KTLO Parent | Alignment Method |
|-------|-------------|-----------------|
| SkiResort | schema:SkiResort → schema:SportsActivityLocation → schema:LocalBusiness → schema:Place → schema:Thing | Direct (schema.org) |
| SkiSlope | *Free etype* | No direct KTLO parent — enriched as subclass of schema:Place |
| SkiLift | *Free etype* | No direct KTLO parent — enriched as subclass of schema:CivicStructure |
| SkiPass | *Free etype* | No direct KTLO parent — enriched as subclass of schema:Offer |
| SkiSchool | schema:EducationalOrganization → schema:Organization → schema:Thing | Direct (schema.org) |
| Hotel | schema:LodgingBusiness → schema:LocalBusiness → schema:Place | Direct (schema.org) |
| Restaurant | schema:FoodEstablishment → schema:LocalBusiness → schema:Place | Direct (schema.org) |
| RentalShop | schema:Store → schema:LocalBusiness → schema:Place | Direct (schema.org) |
| Municipality | schema:AdministrativeArea → schema:Place → schema:Thing | Direct (schema.org) |
| Coordinate | geo:Point → geo:SpatialThing | Direct (W3C Geo) |

### Object Property Alignment

| Property | KTLO Parent |
|----------|-------------|
| hasSlope | schema:containsPlace |
| hasLift | schema:containsPlace |
| hasSkiPass | schema:makesOffer |
| hasSkiSchool | schema:containsPlace |
| locatedIn | schema:containedInPlace |
| nearResort | schema:geo / spatial proximity |
| hasCoordinates | schema:geo |

### Data Property Alignment

| Property | KTLO Parent |
|----------|-------------|
| name | schema:name |
| altitudeMin | schema:elevation |
| altitudeMax | schema:elevation |
| difficulty | *Free property* (enriched) |
| lengthKm | schema:distance |
| liftType | schema:additionalType |
| capacity | schema:maximumAttendeeCapacity |
| starRating | schema:starRating |
| numberOfBeds | schema:numberOfBedrooms |
| price | schema:price |
| cuisine | schema:servesCuisine |
| phone | schema:telephone |
| email | schema:email |
| website | schema:url |
| address | schema:address |
| postcode | schema:postalCode |
| latitude | geo:lat |
| longitude | geo:long |
| osmId | schema:identifier |
| duration | schema:validThrough |

### KTLO Enrichment Summary

| Free Etype/Property | Parent Created Under | Justification |
|---------------------|---------------------|---------------|
| SkiSlope | schema:Place | Ski-specific subtype of geographic feature |
| SkiLift | schema:CivicStructure | Transportation infrastructure for ski areas |
| SkiPass | schema:Offer | Ticketing/pricing offer for resort access |
| difficulty | schema:additionalProperty | Piste difficulty classification (ski-specific) |

## 4.3 Dataset Reshaping

The cleaned datasets from Phase 2 are already aligned with the knowledge structure:
- Column names match finalized data property terms
- Entity IDs follow the naming convention (resortId, slopeId, liftId, etc.)
- Object properties (locatedIn, nearResort) are computed via spatial proximity
- Datatypes are consistent with the teleology specification

No additional reshaping was needed beyond the Phase 2 cleaning.

## 4.4 Evaluation — Knowledge Definition

### Etypes Evaluation

| Etype | Initial | Final | From Reference Ontology | Aligned to KTLO | Method |
|-------|---------|-------|------------------------|-----------------|--------|
| SkiResort | Yes | Yes | Schema.org SkiResort | Yes | Direct |
| SkiSlope | Yes | Yes | No (custom fragment) | Yes (enriched) | Free etype |
| SkiLift | Yes | Yes | No (custom fragment) | Yes (enriched) | Free etype |
| SkiPass | Yes | Yes | No (custom fragment) | Yes (enriched) | Free etype |
| SkiSchool | Yes | Yes | Schema.org EducationalOrg | Yes | Direct |
| Hotel | Yes | Yes | Schema.org LodgingBusiness | Yes | Direct |
| Restaurant | Yes | Yes | Schema.org FoodEstablishment | Yes | Direct |
| RentalShop | Yes | Yes | Schema.org Store | Yes | Direct |
| Municipality | Yes | Yes | Schema.org AdministrativeArea | Yes | Direct |
| Coordinate | Yes | Yes | W3C Geo Point | Yes | Direct |
| **Total** | **10** | **10** | **6 reused, 4 custom** | **10** | |

### Object Properties Evaluation

| Property | Initial | Final | Aligned to KTLO |
|----------|---------|-------|-----------------|
| hasSlope | Yes | Yes | Yes (containsPlace) |
| hasLift | Yes | Yes | Yes (containsPlace) |
| hasSkiPass | Yes | Yes | Yes (makesOffer) |
| hasSkiSchool | Yes | Yes | Yes (containsPlace) |
| locatedIn | Yes | Yes | Yes (containedInPlace) |
| nearResort | Yes | Yes | Yes (geo proximity) |
| hasCoordinates | Yes | Yes | Yes (geo) |
| **Total** | **7** | **7** | **7** |

### Data Properties Evaluation

| # Properties Initially | # Finally | # Aligned to KTLO | # Enriched |
|------------------------|-----------|-------------------|------------|
| 19 | 19 | 18 | 1 (difficulty) |

### Changes from Previous Phases

No changes were required to the Purpose Definition or Language Definition phases. The teleology structure successfully captures all concepts identified in Phase 1 and aligned in Phase 2.
