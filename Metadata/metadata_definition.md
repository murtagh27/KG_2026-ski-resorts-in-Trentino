# Metadata Definition

## 7.1 Project Metadata Description

| Field | Value |
|-------|-------|
| **Title** | Ski Resorts in Trentino Knowledge Graph |
| **Description** | A Knowledge Graph modeling ski resorts, slopes, lifts, and associated tourism facilities (hotels, restaurants, rental shops) in the Trentino-Alto Adige/Sudtirol region of Italy. |
| **Creator** | KG 2026 Project Team — University of Trento |
| **Date** | March 2026 |
| **Language** | English |
| **Subject** | Ski tourism, Knowledge Graphs, Trentino, Winter sports |
| **Coverage** | Trentino-Alto Adige/Sudtirol, Italy (2026) |
| **License** | Open Data (datasets from OpenStreetMap under ODbL) |
| **Format** | RDF/Turtle (.ttl) |
| **Methodology** | iTelos (KnowDive Group, University of Trento) |
| **Repository** | github.com/murtagh27/KG_2026-ski-resorts-in-Trentino |

## 7.2 People Metadata Description

| Field | Value |
|-------|-------|
| **Supervisor** | Prof. Fausto Giunchiglia |
| **Teaching Assistant** | Mayukh Bagchi |
| **Course** | Knowledge Graphs (KG 2025/2026) |
| **University** | University of Trento, DISI |
| **Research Group** | KnowDive Group |

## 7.3 Language Resources Metadata

| Resource | Description | Format | Location |
|----------|-------------|--------|----------|
| Language Terms Table | Finalized etype, object property, and data property language terms | Markdown | Phase 2/language_definition.md |
| LTLO Alignment | Mapping of terms to UKC/WordNet hierarchy | Markdown table | Phase 2/language_definition.md |
| LTLO Enrichment | New terms added to the Language Teleontology | Markdown table | Phase 2/language_definition.md |

## 7.4 Knowledge Resources Metadata

| Resource | Description | Format | Location |
|----------|-------------|--------|----------|
| Teleology (Ontology) | OWL ontology defining classes, object properties, and data properties | Turtle (.ttl) | Phase 3/ontology/ski_resorts_trentino.ttl |
| KTLO Alignment | Mapping of ontology elements to Schema.org / W3C Geo parents | Markdown table | Phase 3/knowledge_definition.md |
| ER Model | Entity-Relationship model diagram | Text/Markdown | Phase 1/purpose_definition.md |

### Ontology Metadata (DCAT-compatible)

```turtle
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix dct: <http://purl.org/dc/terms/> .

<http://skiresorts-trentino.2026.kg/ontology> a dcat:Dataset ;
    dc:title "Ski Resorts in Trentino Ontology" ;
    dc:description "OWL ontology for modeling ski resorts and tourism facilities in Trentino" ;
    dct:creator "KG 2026 Project Team, University of Trento" ;
    dct:issued "2026-03-26" ;
    dct:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcat:distribution [
        a dcat:Distribution ;
        dcat:mediaType "text/turtle" ;
        dcat:downloadURL <http://skiresorts-trentino.2026.kg/ontology/ski_resorts_trentino.ttl>
    ] .
```

## 7.5 Data Resources Metadata

| Resource | Source | Records | Format | Classification | Location |
|----------|--------|---------|--------|----------------|----------|
| Ski Resorts (raw) | OpenStreetMap | 295 | JSON/CSV | Common | Phase 1/data/ |
| Ski Resorts (cleaned) | Cleaned OSM | 222 | JSON/CSV | Common | Phase 2/data/ |
| Ski Slopes (raw) | OpenStreetMap | 2,792 | JSON/CSV | Contextual | Phase 1/data/ |
| Ski Slopes (cleaned) | Cleaned OSM | 2,792 | JSON/CSV | Contextual | Phase 2/data/ |
| Ski Lifts (raw) | OpenStreetMap | 5,677 | JSON/CSV | Contextual | Phase 1/data/ |
| Ski Lifts (cleaned) | Cleaned OSM | 5,677 | JSON/CSV | Contextual | Phase 2/data/ |
| Hotels (raw) | OpenStreetMap | 3,393 | JSON/CSV | Core | Phase 1/data/ |
| Hotels (cleaned) | Cleaned OSM | 3,393 | JSON/CSV | Core | Phase 2/data/ |
| Restaurants (raw) | OpenStreetMap | 3,896 | JSON/CSV | Core | Phase 1/data/ |
| Restaurants (cleaned) | Cleaned OSM | 3,896 | JSON/CSV | Core | Phase 2/data/ |
| Rental Shops (raw) | OpenStreetMap | 16 | JSON/CSV | Core | Phase 1/data/ |
| Rental Shops (cleaned) | Cleaned OSM | 16 | JSON/CSV | Core | Phase 2/data/ |

## 7.6 KG Metadata Description

| Field | Value |
|-------|-------|
| **Title** | Ski Resorts in Trentino Knowledge Graph |
| **Format** | RDF/Turtle (.ttl) |
| **Size** | ~151,744 triples |
| **Entity types** | 10 defined (7 populated) |
| **Total entities** | ~31,992 |
| **Namespace** | http://skiresorts-trentino.2026.kg/ |
| **Ontology namespace** | http://skiresorts-trentino.2026.kg/ontology# |
| **Resource namespace** | http://skiresorts-trentino.2026.kg/resource/ |
| **Primary data source** | OpenStreetMap (ODbL license) |
| **Schema references** | Schema.org, W3C Geo, OSM Piste/Aerialway schemas |
| **Location** | Phase 4/rdf/ski_resorts_trentino_kg.ttl |

### Distribution

The KG and all associated resources are published via:
- **GitHub repository**: Source code, scripts, documentation, and data files
- **RDF files**: Individual per-entity-type TTL files + merged KG file in Phase 4/rdf/
- **Ontology**: Standalone TTL file in Phase 3/ontology/
