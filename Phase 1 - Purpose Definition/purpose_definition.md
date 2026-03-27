# Phase 1 - Purpose Definition

## 1.1 Informal Purpose

The goal of this project is to build a Knowledge Graph (KG) that stores, organizes, and provides easy access to information about **ski resorts in the Trentino region**, with a specific focus on winter sports tourism. The KG will serve as a centralized knowledge hub, connecting tourists, travel planners, and local tourism boards to the wealth of skiing opportunities the region has to offer, such as ski slopes, ski lifts, ski passes, ski schools, nearby accommodation, restaurants, and equipment rental shops.

## 1.2 Domain of Interest (DoI)

The Domain of Interest (DoI) for this project is the **Trentino-Alto Adige/Sudtirol region** in the year **2026**, with a particular focus on **ski resorts and winter sports infrastructure**. The Trentino region is renowned for its world-class ski areas, ranging from the Dolomiti Superski circuit to smaller family-friendly resorts. The geographical scope spans the entire province, encompassing its alpine landscapes, valleys, and mountain passes.

Key features of the domain include:

- **Ski Resorts & Slopes**: Major ski areas such as Madonna di Campiglio, Val di Fassa, Val di Sole, Val Gardena, Plan de Corones, and many others, with slopes of varying difficulty levels.
- **Winter Sports Infrastructure**: Ski lifts (chairlifts, gondolas, cable cars), snow parks, cross-country trails, and ski schools.
- **Tourism Services**: Hotels, restaurants, equipment rental shops, and ski pass offices located near or within ski resort areas.
- **Geographic Context**: Municipalities, valleys, mountain peaks, and elevation data that contextualize the ski resort locations.

## 1.3 Scenarios Definition

In this section, a set of usage scenarios describing the multiple aspects considered by the project purpose are presented.

1. **Winter holiday planning** - **Marco Bianchi** and his girlfriend are planning a week-long ski vacation in Trentino during February. They want to compare different ski resorts based on the number and difficulty of slopes, available lifts, and proximity to hotels and restaurants. They are intermediate-level skiers looking for a resort with a good mix of blue and red slopes, and they want to dine at local restaurants after skiing. They also need to find a hotel within easy reach of the slopes.

2. **Family ski trip** - **Elena Fischer** and her family (husband and two children aged 6 and 10) are looking for a family-friendly ski resort in Trentino for the Christmas holidays. They need a resort with a ski school for beginners, easy (blue) slopes for the children, and kid-friendly facilities. They also want to find a nearby hotel with family rooms and restaurants that cater to children. Equipment rental is essential since the children are still growing.

3. **Expert/competitive skiing** - **Luca Martinelli** is an advanced skier and ski touring enthusiast who visits Trentino every winter. He specifically looks for resorts with challenging black slopes, modern high-capacity lift systems, and snow parks for freestyle. He wants to know which resorts have the highest altitude and the most vertical drop, and he prefers resorts with a large number of slopes to maximize variety during his stay.

4. **Budget student trip** - **Sofia Novak**, a 22-year-old Erasmus student in Trento, wants to organize a budget-friendly weekend ski trip with friends. She needs to find the most affordable ski pass options, cheap equipment rental shops, and budget accommodation near the slopes. She also wants to compare prices across different resorts to find the best value for money.

5. **Accessibility & logistics** - **Thomas Weber**, a 55-year-old tourist from Germany, is planning a ski trip but has mobility concerns due to a knee injury. He wants to find ski resorts that are easily accessible by public transport or have large parking facilities, resorts with gondola lifts (rather than drag lifts), and hotels at low altitude. He also wants to know which resorts have medical facilities nearby and restaurants that are accessible without climbing stairs.

## 1.4 Personas

In this section a set of real users acting within the scenarios defined above are defined.

1. **Marco Bianchi** is a 28-year-old software engineer from Milan. He has been skiing since childhood and considers himself an intermediate skier. He travels to Trentino 2-3 times per winter season with his girlfriend and values a balanced resort experience with good dining options. He prefers to plan everything in advance using online resources.

2. **Elena Fischer** is a 38-year-old schoolteacher from Innsbruck, Austria. She is an experienced skier but her priority is finding safe, child-appropriate ski environments. She values ski schools with qualified instructors and resorts that offer beginner terrain parks. She always rents equipment for the children and looks for all-inclusive family packages.

3. **Luca Martinelli** is a 32-year-old professional ski instructor from Trento. He knows the local ski scene well but uses the KG to discover less-known resorts with expert terrain. He is interested in slope statistics (difficulty distribution, altitude range, vertical drop) and cares about lift infrastructure quality. He frequently visits multiple resorts in a single season.

4. **Sofia Novak** is a 22-year-old university student from Bratislava, Slovakia, currently studying at the University of Trento on Erasmus. This is her first winter in the Alps and she has limited skiing experience. Budget is her primary constraint, so she compares ski pass prices and rental costs. She organizes group trips and needs information on affordable accommodation options.

5. **Thomas Weber** is a 55-year-old retired engineer from Munich, Germany. He is a lifelong skier but recent knee surgery limits him to gentle slopes. He values accessibility information, prefers gondola lifts over drag lifts, and needs to stay at hotels with easy access to the slopes. He travels by car and appreciates detailed parking information.

## 1.5 Competency Questions (CQs)

| Person | No. | Question |
|--------|-----|----------|
| Marco Bianchi | 1.1 | Which ski resorts are available in the Trentino region? |
| Marco Bianchi | 1.2 | What slopes (and their difficulty levels) does ski resort X have? |
| Marco Bianchi | 1.3 | Which restaurants are located near ski resort X? |
| Marco Bianchi | 1.4 | Where can I find a hotel near ski resort X? |
| Marco Bianchi | 1.5 | What ski lifts are available at ski resort X and what type are they? |
| Marco Bianchi | 1.6 | What is the altitude range (min/max elevation) of ski resort X? |
| Elena Fischer | 2.1 | Which ski resorts have a ski school for beginners? |
| Elena Fischer | 2.2 | Which ski resorts have easy (blue) slopes suitable for children? |
| Elena Fischer | 2.3 | Where can I rent ski equipment near ski resort X? |
| Elena Fischer | 2.4 | Which hotels near ski resort X offer family rooms? |
| Elena Fischer | 2.5 | What is the price of a ski pass at ski resort X? |
| Luca Martinelli | 3.1 | Which ski resorts have black (expert) slopes? |
| Luca Martinelli | 3.2 | Which ski resort has the most slopes? |
| Luca Martinelli | 3.3 | What is the total number of ski lifts at each resort? |
| Luca Martinelli | 3.4 | Which resorts have snow parks for freestyle skiing? |
| Luca Martinelli | 3.5 | What is the vertical drop (altitude difference) of ski resort X? |
| Sofia Novak | 4.1 | Which ski resort has the cheapest ski pass? |
| Sofia Novak | 4.2 | Where can I rent ski equipment at the lowest price? |
| Sofia Novak | 4.3 | Which budget hotels or hostels are near ski resorts? |
| Sofia Novak | 4.4 | Can I reach ski resort X by public transport from Trento? |
| Thomas Weber | 5.1 | Which ski resorts have gondola or cable car lifts? |
| Thomas Weber | 5.2 | Which ski resorts have parking facilities? |
| Thomas Weber | 5.3 | Which hotels are at low altitude near ski resorts? |
| Thomas Weber | 5.4 | Are there restaurants near ski resort X that are easily accessible? |
| Thomas Weber | 5.5 | What medical facilities or pharmacies are near ski resort X? |

## 1.6 Concepts Identification

In this section, the key concepts representing entities and their associated properties within the Knowledge Graph are outlined.

### Entity Types (Etypes)

| Etype | Description | Properties | Focus |
|-------|-------------|------------|-------|
| SkiResort | A ski resort/area in Trentino | resortId, name, municipality, altitude_min, altitude_max, total_slopes, website, coordinates | **Common** |
| SkiSlope | An individual ski slope/piste | slopeId, osmId, name, difficulty, length_km, resort, coordinates | **Contextual** |
| SkiLift | A lift system at a ski resort | liftId, osmId, name, type, capacity, resort, coordinates | **Contextual** |
| SkiPass | Ski pass/ticket pricing info | passId, name, type, price, duration, resort | **Contextual** |
| SkiSchool | A ski school operating at a resort | schoolId, name, resort, phone, website, languages | **Contextual** |
| Hotel | Accommodation near ski areas | hotelId, name, municipality, address, star_rating, altitude, nBeds, price, phone, email, website, coordinates | **Core** |
| Restaurant | Dining establishment near ski areas | restaurantId, osmId, name, cuisine, municipality, address, phone, coordinates | **Core** |
| RentalShop | Equipment rental shop | rentalId, osmId, name, type, municipality, address, phone, coordinates | **Core** |
| Municipality | A municipality/town in Trentino | municipalityId, name, province, population, altitude, coordinates | **Common** |
| Coordinate | Geographic coordinates | latitude, longitude | **Common** |

### Object Properties

| Property | Domain | Range | Description | Focus |
|----------|--------|-------|-------------|-------|
| hasSlope | SkiResort | SkiSlope | Resort contains this slope | Contextual |
| hasLift | SkiResort | SkiLift | Resort has this lift | Contextual |
| hasSkiPass | SkiResort | SkiPass | Resort offers this pass | Contextual |
| hasSkiSchool | SkiResort | SkiSchool | Resort has this school | Contextual |
| locatedIn | SkiResort / Hotel / Restaurant / RentalShop | Municipality | Entity is in this municipality | Common |
| nearResort | Hotel / Restaurant / RentalShop | SkiResort | Entity is near this resort | Core |
| hasCoordinates | SkiResort / Hotel / Restaurant / etc. | Coordinate | Entity has these geo coordinates | Common |

### Data Properties

| Property | Domain | Datatype | Description | Focus |
|----------|--------|----------|-------------|-------|
| name | All etypes | string | Name of the entity | Common |
| altitude | Hotel / Municipality | integer | Altitude in meters | Common |
| altitude_min | SkiResort | integer | Minimum altitude of resort | Contextual |
| altitude_max | SkiResort | integer | Maximum altitude of resort | Contextual |
| difficulty | SkiSlope | string | blue/red/black | Contextual |
| length_km | SkiSlope | float | Length of slope in km | Contextual |
| type | SkiLift | string | chairlift/gondola/cable_car/drag | Contextual |
| capacity | SkiLift | integer | Persons per hour | Contextual |
| star_rating | Hotel | string | 1-5 stars | Core |
| price | SkiPass / Hotel | float | Price in EUR | Core |
| cuisine | Restaurant | string | Type of cuisine | Core |
| phone | Hotel / Restaurant / RentalShop / SkiSchool | string | Phone number | Common |
| website | SkiResort / Hotel / SkiSchool | string | Website URL | Common |
| osmId | SkiSlope / SkiLift / Restaurant / RentalShop | string | OpenStreetMap ID | Common |
| latitude | Coordinate | float | Geographic latitude | Common |
| longitude | Coordinate | float | Geographic longitude | Common |

## 1.7 ER Model Definition

The ER model is designed to provide tourists easy access to information about ski resorts and their associated facilities. The model centers on two main entities:

- **SkiResort** — the primary entity representing a ski area, serving as the hub connecting slopes, lifts, passes, and schools.
- **Municipality** — the geographic entity linking resorts to their location context.

These two entities are classified as **common** because they store the main connective information for all other entities.

Connected to **SkiResort**, there is a set of **contextual** entities containing ski-specific information:
- **SkiSlope** — individual slopes with difficulty and length
- **SkiLift** — lift infrastructure with type and capacity
- **SkiPass** — pricing and ticket options
- **SkiSchool** — ski instruction facilities

Connected to **Municipality** (and indirectly to SkiResort via `nearResort`), there are **core** entities satisfying tourist service needs:
- **Hotel** — accommodation with star rating, beds, and pricing
- **Restaurant** — dining options with cuisine type
- **RentalShop** — equipment rental facilities

The common entity **Coordinate** stores latitude/longitude and is referenced by most entities for geographic positioning.

### ER Diagram (textual description)

```
                    ┌──────────────┐
                    │  SkiSchool   │ Contextual
                    └──────┬───────┘
                           │ hasSkiSchool
┌──────────┐        ┌──────┴───────┐        ┌──────────────┐
│ SkiSlope │◄───────│  SkiResort   │───────►│   SkiLift    │
│Contextual│hasSlope│   Common     │hasLift │ Contextual   │
└──────────┘        └──────┬───────┘        └──────────────┘
                           │ hasSkiPass / locatedIn
                    ┌──────┴───────┐
                    │   SkiPass    │ Contextual
                    └──────────────┘

┌──────────┐  locatedIn  ┌──────────────┐  nearResort  ┌──────────────┐
│  Hotel   │────────────►│ Municipality │◄─────────────│  Restaurant  │
│  Core    │             │   Common     │              │    Core      │
└──────────┘             └──────────────┘              └──────────────┘
                                ▲
                                │ locatedIn
                         ┌──────┴───────┐
                         │  RentalShop  │ Core
                         └──────────────┘

All entities ──hasCoordinates──► Coordinate (Common)
```

## 1.8 Report

In this chapter, we set up a solid base by defining our main purpose, creating realistic scenarios, and developing specific competency questions. This helps make sure the Knowledge Graph meets the needs of Trentino's ski tourism, with a focus on ski resorts and winter sports.

The five user personas add helpful context, guiding us to design the graph around practical needs — from an intermediate skier comparing resorts, to a family looking for child-friendly facilities, to a budget student, to someone with accessibility concerns. Each persona represents a distinct use case that the KG must support.

**Strengths of our approach:**
- The scenarios cover diverse user needs (experience level, budget, family, accessibility), ensuring broad coverage of the project purpose.
- The CQs are directly derived from personas, making them concrete and testable.
- The ER model follows the L12-2 example pattern with common/core/contextual classification.

**Potential challenges:**
- Data availability for some attributes (ski pass prices, ski school details) may be limited in open data sources. We plan to address this during information gathering.
- The `nearResort` relationship requires spatial computation (distance thresholds), which adds complexity to the data processing pipeline.
- Some ski resorts span multiple municipalities, which may complicate the `locatedIn` relationship.

We plan to revisit and refine the ER model after the data-gathering phase, making adjustments based on actual data availability — following the iterative approach recommended by the iTelos methodology.
