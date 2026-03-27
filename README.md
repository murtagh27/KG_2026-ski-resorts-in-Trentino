# KG 2026 - Ski Resorts in Trentino

A Knowledge Graph about **ski resorts and winter sports infrastructure** in the Trentino-Alto Adige/Sudtirol region of Italy, built following the **iTelos methodology** as part of the Knowledge Graphs course (2025/2026) at the University of Trento.

## Overview

This project models ski resorts, slopes, lifts, hotels, restaurants, and equipment rental shops across Trentino, connecting them through geographic and semantic relationships. The KG is built from OpenStreetMap data and aligned to Schema.org, W3C Geo, and OSM ontology fragments.

### Key Numbers

| Metric | Value |
|--------|-------|
| Total entities | ~31,992 |
| Total RDF triples | ~151,744 |
| Entity types (ontology) | 10 |
| Entity types (populated) | 7 |
| Object properties | 7 |
| Data properties | 19 |
| Data source | OpenStreetMap (Overpass API) |

## Repository Structure

```
.
├── Phase 1 - Purpose Definition/
│   ├── purpose_definition.md        # Scenarios, personas, 25 CQs, ER model
│   ├── information_gathering.md     # Data source descriptions
│   ├── data/                        # Raw datasets (JSON + CSV)
│   └── scripts/                     # OSM data collection scripts
│
├── Phase 2 - Language Definition/
│   ├── language_definition.md       # Finalized terms, LTLO alignment, cleaning docs
│   ├── data/                        # Cleaned datasets (JSON + CSV)
│   └── scripts/                     # Dataset cleaning script
│
├── Phase 3 - Knowledge Definition/
│   ├── knowledge_definition.md      # Teleology definition, KTLO alignment
│   └── ontology/
│       └── ski_resorts_trentino.ttl # OWL ontology (Turtle)
│
├── Phase 4 - Entity Definition/
│   ├── entity_definition.md         # Entity mapping documentation
│   ├── rdf/                         # Generated RDF files
│   │   ├── ski_resorts.ttl
│   │   ├── ski_slopes.ttl
│   │   ├── ski_lifts.ttl
│   │   ├── hotels.ttl
│   │   ├── restaurants.ttl
│   │   ├── rental_shops.ttl
│   │   └── ski_resorts_trentino_kg.ttl  # Merged KG
│   └── scripts/                     # RDF generation script
│
├── Evaluation/
│   └── evaluation.md                # KG statistics, SPARQL queries, CQ answerability
│
├── Metadata/
│   └── metadata_definition.md       # DCAT-compatible metadata
│
├── ProjectReport/
│   ├── knowdive-files/              # LaTeX class, main.tex, logos
│   └── section/                     # Report sections (0-11)
│
└── Documentation/                   # Template PDF and ZIP
```

## Entity Types

| Entity | Count | Classification | Description |
|--------|-------|----------------|-------------|
| SkiResort | 222 | Common | Ski areas and winter sports facilities |
| SkiSlope | 2,792 | Contextual | Downhill pistes with difficulty levels |
| SkiLift | 5,677 | Contextual | Chairlifts, gondolas, cable cars, drag lifts |
| Hotel | 3,393 | Core | Accommodation near ski areas |
| Restaurant | 3,896 | Core | Dining establishments near ski areas |
| RentalShop | 16 | Core | Ski equipment rental shops |
| Coordinate | ~15,996 | Common | WGS84 geographic coordinates |

## Ontology

- **Namespace**: `http://skiresorts-trentino.2026.kg/ontology#`
- **Format**: OWL in Turtle (.ttl)
- **Aligned to**: Schema.org, W3C Geo, OSM Piste/Aerialway schemas
- **File**: [`Phase 3 - Knowledge Definition/ontology/ski_resorts_trentino.ttl`](Phase%203%20-%20Knowledge%20Definition/ontology/ski_resorts_trentino.ttl)

## Competency Questions

25 competency questions were defined across 5 personas representing different user needs:

- **Marco Bianchi** (intermediate skier) - Resort comparison, slopes, dining
- **Elena Fischer** (family traveler) - Child-friendly resorts, ski schools, rentals
- **Luca Martinelli** (expert skier) - Black slopes, lift infrastructure, statistics
- **Sofia Novak** (budget student) - Affordable passes, cheap rentals, budget hotels
- **Thomas Weber** (accessibility needs) - Gondola lifts, low-altitude hotels, logistics

**Answerability**: 9/25 fully answerable, 7/25 partially, 9/25 not answerable (due to missing ski pass, ski school, transport, and accessibility data from OSM).

## How to Use

### Query the KG

Load `Phase 4 - Entity Definition/rdf/ski_resorts_trentino_kg.ttl` into any SPARQL endpoint (e.g., Apache Jena Fuseki, GraphDB, Blazegraph) and run queries:

```sparql
PREFIX ski: <http://skiresorts-trentino.2026.kg/ontology#>

# List all ski resorts
SELECT ?resort ?name WHERE {
  ?resort a ski:SkiResort ; ski:name ?name .
} ORDER BY ?name

# Find restaurants near a specific resort
SELECT ?name ?cuisine WHERE {
  ?r a ski:Restaurant ; ski:name ?name ;
     ski:nearResort ?resort .
  ?resort ski:name "Madonna di Campiglio" .
  OPTIONAL { ?r ski:cuisine ?cuisine . }
}

# Resorts with gondola lifts
SELECT DISTINCT ?resortName WHERE {
  ?lift a ski:SkiLift ; ski:liftType "gondola" ;
        ski:nearResort ?resort .
  ?resort ski:name ?resortName .
}
```

### Compile the Report

Open `ProjectReport/knowdive-files/main.tex` in [Overleaf](https://www.overleaf.com/) or compile locally:

```bash
cd ProjectReport/knowdive-files
pdflatex main.tex
```

### Reproduce the Data Pipeline

```bash
# 1. Fetch raw data from OSM
python "Phase 1 - Purpose Definition/scripts/fetch_osm_data.py"

# 2. Clean datasets
python "Phase 2 - Language Definition/scripts/clean_datasets.py"

# 3. Generate RDF
python "Phase 4 - Entity Definition/scripts/generate_rdf.py"
```

**Requirements**: Python 3.8+ with `requests` library.

## Methodology

This project follows the **iTelos** methodology developed by the KnowDive Research Group at the University of Trento:

1. **Purpose Definition** - Domain of Interest, scenarios, personas, competency questions, ER model
2. **Language Definition** - Fixing language terms, LTLO alignment, dataset cleaning
3. **Knowledge Definition** - Teleology (ontology) definition, KTLO alignment
4. **Entity Definition** - Entity identification, data mapping, RDF generation

## License

- **Code & Documentation**: See [LICENSE](LICENSE)
- **Data**: OpenStreetMap data is used under the [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/)

## Credits

- **Course**: Knowledge Graphs (KG 2025/2026), University of Trento
- **Supervisor**: Prof. Fausto Giunchiglia
- **Teaching Assistant**: Mayukh Bagchi
- **Research Group**: [KnowDive Group](https://knowdive.disi.unitn.it/), DISI, University of Trento
