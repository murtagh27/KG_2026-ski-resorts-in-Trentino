# Evaluation

## 6.1 Knowledge Graph Statistics

### Overall Statistics

| Metric | Value |
|--------|-------|
| Total entities | ~31,992 |
| Total RDF triples | ~151,744 |
| Entity types defined (ontology) | 10 |
| Entity types populated (data) | 7 |
| Object properties defined | 7 |
| Data properties defined | 19 |
| Ontology fragments reused | 6 (Schema.org, OSM Piste, OSM Aerialway, W3C Geo, Geospatial) |
| Ontology fragments created | 2 (SkiPass, SkiSchool — ontology only, no data) |

### Entities per Etype

| Entity Type | Count | % of Total Entities |
|-------------|-------|---------------------|
| Coordinate | ~15,996 | 50.0% |
| SkiLift | 5,677 | 17.7% |
| Restaurant | 3,896 | 12.2% |
| Hotel | 3,393 | 10.6% |
| SkiSlope | 2,792 | 8.7% |
| SkiResort | 222 | 0.7% |
| RentalShop | 16 | 0.05% |
| SkiPass | 0 | 0% (no data) |
| SkiSchool | 0 | 0% (no data) |
| Municipality | 0 | 0% (referenced as URIs only) |

## 6.2 Knowledge Layer Evaluation

### 6.2.1 Teleontology vs Competency Questions

| CQ # | Question | Can be answered? | Requires |
|------|----------|-----------------|----------|
| 1.1 | Which ski resorts are available in Trentino? | Yes | SELECT on SkiResort |
| 1.2 | What slopes does resort X have? | Partially | Requires resort-slope linkage via nearResort |
| 1.3 | Which restaurants are near resort X? | Yes | nearResort property |
| 1.4 | Where can I find a hotel near resort X? | Yes | nearResort property |
| 1.5 | What ski lifts are at resort X? | Partially | Via nearResort linkage |
| 1.6 | What is the altitude range of resort X? | No | altitudeMin/Max not populated from OSM |
| 2.1 | Which resorts have ski schools? | No | SkiSchool not populated |
| 2.2 | Which resorts have easy slopes? | Yes | Filter slopes by difficulty="easy" + nearResort |
| 2.3 | Where to rent equipment near resort X? | Yes | RentalShop + nearResort |
| 2.4 | Which hotels near resort X offer family rooms? | Partially | Hotel data lacks room type details |
| 2.5 | Ski pass price at resort X? | No | SkiPass not populated |
| 3.1 | Which resorts have black slopes? | Yes | Filter difficulty="advanced"/"expert" |
| 3.2 | Which resort has the most slopes? | Yes | COUNT + GROUP BY on nearResort |
| 3.3 | Total lifts at each resort? | Yes | COUNT lifts per nearResort |
| 3.4 | Which resorts have snow parks? | Partially | No direct snow park data |
| 3.5 | Vertical drop of resort X? | No | altitudeMin/Max not populated |
| 4.1 | Cheapest ski pass? | No | SkiPass not populated |
| 4.2 | Cheapest equipment rental? | No | Price data not available for shops |
| 4.3 | Budget hotels near resorts? | Partially | Hotel data lacks price info |
| 4.4 | Public transport to resort X? | No | No transport data |
| 5.1 | Resorts with gondola lifts? | Yes | Filter lifts by liftType="gondola" |
| 5.2 | Resorts with parking? | No | No parking data |
| 5.3 | Hotels at low altitude near resorts? | Partially | Hotel altitude not available |
| 5.4 | Accessible restaurants near resort X? | Partially | No accessibility data |
| 5.5 | Medical facilities near resort X? | No | No medical facility data |

**Summary**: 10/25 CQs fully answerable, 6 partially, 9 not answerable.

### 6.2.2 Teleontology vs Reference Ontologies

| Reference Ontology | Etypes Covered | Properties Covered | Coverage |
|-------------------|----------------|-------------------|----------|
| Schema.org | 6/10 (SkiResort, Hotel, Restaurant, RentalShop, SkiSchool, Municipality) | 15/19 | 75% |
| OSM Piste Schema | 1/10 (SkiSlope) | 2/19 (difficulty, ref) | 10% |
| OSM Aerialway Schema | 1/10 (SkiLift) | 2/19 (liftType, capacity) | 10% |
| W3C Geo | 1/10 (Coordinate) | 2/19 (lat, long) | 10% |

## 6.3 Data Layer Evaluation

### 6.3.1 Entity Connectivity

| Entity Type | Entities with nearResort link | % Connected |
|-------------|------------------------------|-------------|
| SkiSlope | Computed via proximity | ~95% |
| SkiLift | Computed via proximity | ~95% |
| Hotel | Computed via proximity (<20km) | ~85% |
| Restaurant | Computed via proximity (<15km) | ~70% |
| RentalShop | Computed via proximity (<20km) | ~100% |

### 6.3.2 Property Connectivity

| Data Property | Entities with value | % Non-empty |
|---------------|-------------------|-------------|
| name | ~15,996 (all non-coord) | ~100% |
| osmId | ~15,996 | ~100% |
| difficulty (slopes) | ~2,500 | ~90% |
| liftType (lifts) | ~5,677 | ~100% |
| cuisine (restaurants) | ~1,200 | ~31% |
| starRating (hotels) | ~800 | ~24% |
| phone | ~3,000 | ~19% |
| email (hotels) | ~500 | ~15% |
| website | ~1,500 | ~9% |
| latitude/longitude | ~15,996 | ~100% |

## 6.4 Query Execution — SPARQL Queries

The following SPARQL queries correspond to the Competency Questions that CAN be answered by the KG.

### 6.4.1 CQ 1.1: All Ski Resorts in Trentino

```sparql
PREFIX ski: <http://skiresorts-trentino.2026.kg/ontology#>
PREFIX res: <http://skiresorts-trentino.2026.kg/resource/>

SELECT ?resort ?name
WHERE {
  ?resort a ski:SkiResort ;
          ski:name ?name .
}
ORDER BY ?name
```

**Expected result**: 222 ski resorts

### 6.4.2 CQ 1.3: Restaurants Near a Specific Resort

```sparql
PREFIX ski: <http://skiresorts-trentino.2026.kg/ontology#>
PREFIX res: <http://skiresorts-trentino.2026.kg/resource/>

SELECT ?restaurant ?name ?cuisine
WHERE {
  ?restaurant a ski:Restaurant ;
              ski:name ?name ;
              ski:nearResort ?resort .
  ?resort ski:name "Madonna di Campiglio" .
  OPTIONAL { ?restaurant ski:cuisine ?cuisine . }
}
ORDER BY ?name
```

### 6.4.3 CQ 1.4: Hotels Near a Specific Resort

```sparql
PREFIX ski: <http://skiresorts-trentino.2026.kg/ontology#>

SELECT ?hotel ?name ?stars
WHERE {
  ?hotel a ski:Hotel ;
         ski:name ?name ;
         ski:nearResort ?resort .
  ?resort ski:name "Val di Fassa" .
  OPTIONAL { ?hotel ski:starRating ?stars . }
}
ORDER BY DESC(?stars)
```

### 6.4.4 CQ 2.2: Resorts with Easy (Blue) Slopes

```sparql
PREFIX ski: <http://skiresorts-trentino.2026.kg/ontology#>

SELECT ?resortName (COUNT(?slope) AS ?easySlopes)
WHERE {
  ?slope a ski:SkiSlope ;
         ski:difficulty "easy" ;
         ski:nearResort ?resort .
  ?resort ski:name ?resortName .
}
GROUP BY ?resortName
ORDER BY DESC(?easySlopes)
```

### 6.4.5 CQ 3.1: Resorts with Black/Expert Slopes

```sparql
PREFIX ski: <http://skiresorts-trentino.2026.kg/ontology#>

SELECT DISTINCT ?resortName
WHERE {
  ?slope a ski:SkiSlope ;
         ski:nearResort ?resort .
  ?resort ski:name ?resortName .
  FILTER(?difficulty IN ("advanced", "expert"))
  ?slope ski:difficulty ?difficulty .
}
ORDER BY ?resortName
```

### 6.4.6 CQ 3.2: Resort with Most Slopes

```sparql
PREFIX ski: <http://skiresorts-trentino.2026.kg/ontology#>

SELECT ?resortName (COUNT(?slope) AS ?totalSlopes)
WHERE {
  ?slope a ski:SkiSlope ;
         ski:nearResort ?resort .
  ?resort ski:name ?resortName .
}
GROUP BY ?resortName
ORDER BY DESC(?totalSlopes)
LIMIT 10
```

### 6.4.7 CQ 5.1: Resorts with Gondola Lifts

```sparql
PREFIX ski: <http://skiresorts-trentino.2026.kg/ontology#>

SELECT DISTINCT ?resortName
WHERE {
  ?lift a ski:SkiLift ;
        ski:liftType "gondola" ;
        ski:nearResort ?resort .
  ?resort ski:name ?resortName .
}
ORDER BY ?resortName
```

## 6.5 Query Execution Summary

| CQ Category | Total CQs | Fully Answerable | Partially | Not Answerable |
|-------------|-----------|------------------|-----------|----------------|
| Marco (general skiing) | 6 | 3 | 2 | 1 |
| Elena (family) | 5 | 2 | 1 | 2 |
| Luca (expert) | 5 | 3 | 1 | 1 |
| Sofia (budget) | 4 | 0 | 1 | 3 |
| Thomas (accessibility) | 5 | 1 | 2 | 2 |
| **Total** | **25** | **9 (36%)** | **7 (28%)** | **9 (36%)** |

The main gaps are due to missing data for: ski pass pricing, ski schools, public transport, parking, medical facilities, and accessibility information. These represent future enrichment opportunities.
