# TRACE EMISSION CONTRACT

## ARCSI UNIVERSE

### Event Emission & Trace Governance Specification

*Dátum: 2026-11-11*

*Kontextus:*

> Audi Universe
>
> Vállalati AI tervezés

*Fókusz:*

> • Event Emission
>
> • Trace Governance
>
> • Event Integrity
>
> • System Interoperability

---

## Cél

> A Trace Responsibility Model meghatározza,
> hogy ki miért felelős.
>
> A Trace Emission Contract meghatározza,
> hogy milyen eseményeket,
> milyen formában,
> milyen minimális tartalommal
> kell kibocsátani.

A dokumentum célja a komponensek közötti
egységes trace-kommunikáció biztosítása.

---

## Alapelv

> Minden üzletileg vagy technikailag
> jelentős eseménynek visszakövethető,
> egységes formátumú trace-eseménnyé
> kell válnia.

---

## Egységes Esemény-Boríték (Event Envelope)

> Az Event Envelope a rendszertechnikai
> interoperabilitást biztosítja,
> míg a Payload az adott komponens
> üzleti jelentését hordozza.

Minden kibocsátott esemény két részből áll:

```text
Event
 ├─ Event Envelope
 └─ Payload
```

---

### Event Envelope

Az Event Envelope minden komponens számára kötelező.

Az Envelope biztosítja, hogy:

- az esemény azonosítható legyen
- a trace-lánc összekapcsolható legyen
- a Governance szabályokat tudjon alkalmazni
- az esemény auditálható legyen

### Kötelező mezők

| Mező | Leírás |
|--------|--------|
| timestamp | Az esemény időpontja |
| correlation_id | Üzleti kapcsoló azonosító |
| trace_id | W3C Trace Context azonosító |
| component | Az esemény kibocsátója |
| event_type | Eseménytípus |
| source_of_truth | Szemantikai gazda |
| schema_version | Eseményséma verziója |

---

### Domain Payload

A Payload tartalmáért a szemantikai gazda felel.

A Payload:

- komponens-specifikus
- verziózható
- üzleti jelentésű
- szabadon bővíthető

---

### Példa architektúra

```text
┌──────────────────────────────────┐
│ Event Envelope                   │
├──────────────────────────────────┤
│ timestamp                        │
│ correlation_id                   │
│ trace_id                         │
│ component                        │
│ event_type                       │
│ source_of_truth                  │
│ schema_version                   │
└───────────────┬──────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│ Domain Payload                   │
├──────────────────────────────────┤
│ component-specific fields        │
│ business-specific fields         │
│ optional attributes              │
└──────────────────────────────────┘
```

---

## Szemantikai Tulajdonjog

> Az Event Envelope a platform tulajdona.
>
> A Payload a komponens tulajdona.

### Példák

#### Arcsi Core

```json
{
  "reasoning_rule": "R-001",
  "confidence": 0.84,
  "falsification_passed": true
}
```

#### Wisdom Layer

```json
{
  "wisdom_id": "W-102",
  "operation": "validate",
  "supersedes": "W-099"
}
```

#### Data Layer

```json
{
  "datasource": "SAP",
  "query_type": "READ",
  "dataset": "BOM"
}
```

---

## Verziózási Alapelv

> Az Envelope és a Payload egymástól
> függetlenül fejlődhet.

Példák:

```text
Envelope v1
Payload v5
```

vagy

```text
Envelope v2
Payload v7
```

Ez lehetővé teszi az események
visszafelé kompatibilis fejlődését.

---

## Összefoglalás

```text
Platform felelőssége
        │
        ▼
Event Envelope
        │
        ▼
Payload
        │
        ▼
Komponens felelőssége
```

> Az Event Envelope biztosítja,
> hogy minden esemény ugyanabban a
> trace-ökoszisztémában legyen kezelhető.
>
> A Payload biztosítja,
> hogy minden komponens megőrizhesse
> saját üzleti jelentését.

---

## Sorrendiség és Folytonosság

> Folytonossági alapelv
>
> Az Event Envelope nem csupán az esemény
> azonosítására szolgál.
>
> Az események közötti kapcsolatok,
> a sorrendiség és a helyesbítések
> visszakövethetősége is része a szerződésnek.

### Kötelező mezők bővítése

A trace-lánc integritásának és folytonosságának biztosítása érdekében az Event Envelope az alábbi mezőkkel egészül ki.

| Mező | Típus | Szerep |
|--------|--------|--------|
| event_id | String (ULID / UUIDv7) | Egyedi eseményazonosító |
| trace_level | Enum | Operational vagy Business |
| sequence_number | Integer | Correlation ID-n belüli sorszám |
| supersedes_event_id | String \| null | Helyesbített esemény hivatkozása |

### Eseményfolytonosság

```text
Correlation ID
       │
       ▼

Event #1
(seq: 1)

       │

Event #2
(seq: 2)

       │

Event #3
(seq: 3)
```

A sequence_number mező biztosítja,
hogy egy üzleti folyamat teljes eseménysora
rekonstruálható legyen.

---

### Helyesbítések (Supersession)

> Az esemény nem módosítható.
>
> A helyesbítés új eseményként jön létre,
> amely hivatkozik az eredeti eseményre.

### Működési séma

```text
Eredeti esemény
(event_id: evt_001)

       ▲
       │ supersedes_event_id
       │

Helyesbítő esemény
(event_id: evt_002)
```

### Következmények

Az eredeti esemény:

- megmarad a hash-láncban
- továbbra is auditálható
- nem módosul

A helyesbítő esemény:

- új event_id-t kap
- hivatkozik az eredetire
- felülírja annak üzleti jelentését

---

## Hiányzó Események Kezelése (Gap Detection)

> Trace teljességi alapelv
>
> A hiányzó esemény is esemény.
>
> Ha nem rögzítjük a hiányt,
> a trace látszólag teljes lesz,
> miközben valójában hiányos.

Elosztott rendszerekben:

- hálózati hiba
- időtúllépés
- komponens-leállás
- üzenetvesztés

következtében események maradhatnak ki.

A szerződés három védelmi mechanizmust definiál.

### 1. Sorszám-alapú láncellenőrzés

A sequence_number mező lehetővé teszi
az eseménylánc folytonosságának ellenőrzését.

```text
Event #1 (seq: 1)
         │
         ▼

Event #2 (seq: 2)
         │
         ▼

[ HIÁNYZÓ #3 ]
         │
         ▼

Event #4 (seq: 4)
         │
         ▼

trace.gap.detected
(missing_seq: 3)
```

Ha ugrás történik a sorszámok között,
a rendszer automatikusan generál egy:

```text
trace.gap.detected
```

eseményt.

---

### 2. Árva láncok felismerése

Bizonyos folyamatoknak kötelező lezáró
eseménnyel kell rendelkezniük.

Például:

```text
gateway.request.routed
          │
          ▼
reasoning.context.built
          │
          ▼
reasoning.decision.reached
```

Amennyiben a lezáró esemény
egy előre meghatározott időablakon belül
nem érkezik meg:

```text
trace.chain.incomplete
```

esemény jön létre.

### Cél

Bizonyítani, hogy:

- a folyamat elindult
- a folyamat nem zárult le
- a hiány nem naplózási hiba

---

### 3. Fail-Closed írási garancia

> Business Trace esetén
> a Zero Loss elv érvényesül.

A kibocsátó komponens:

- Arcsi Core
- Wisdom Layer
- Data Layer

csak akkor folytathatja az üzleti tranzakciót,
ha a Durable Queue visszaigazolta
az esemény befogadását.

### Működési modell

```text
Business Event
        │
        ▼

Durable Queue ACK
        │
        ▼

Transaction Commit
```

Ha az ACK nem érkezik meg:

```text
Business Event
        │
        ▼

Queue Failure
        │
        ▼

Transaction Abort
```

A folyamathoz kapcsolódó tranzakció
nem zárható le sikeresként.

---

> Gap Detection alapelv
>
> Egy hiányzó esemény ugyanúgy
> fontos információ lehet,
> mint egy létező esemény.
>
> A cél nem a tökéletes működés bizonyítása,
> hanem a működés teljes történetének
> rekonstruálhatósága.

---

## Standard Event Types (Esemény-szótár)

> Taxonómiai alapelv
>
> A szerződés határozza meg,
> hogyan kommunikálunk.
>
> A szótár határozza meg,
> miről beszélünk.
>
> Egységes eseménynevek nélkül
> nincs egységes értelmezés.

A Trace Emission Contract meghatározza az esemény formáját.

Az Event Dictionary meghatározza az esemény jelentését.

---

## Elnevezési Konvenció

Minden event_type három részből álló,
pontokkal elválasztott névteret követ:

```text
<domain>.<entity>.<action_past_tense>
```

### Domain

Az üzleti vagy technikai terület.

Példák:

```text
gateway
auth
reasoning
wisdom
data
ui
trace
audit
```

### Entity

Az érintett objektum vagy folyamatrész.

Példák:

```text
request
passport
context
decision
knowledge
source
approval
chain
```

### Action (Past Tense)

A már megtörtént esemény.

Példák:

```text
routed
validated
built
retrieved
reached
queried
signed
```

---

> Eseménynév alapelv
>
> A trace mindig megtörtént tényeket rögzít.
>
> Ezért az eseménynevek múlt idejű
> állapotváltozásokat írnak le.

### Ajánlott minták

```text
gateway.request.routed

auth.passport.validated

reasoning.context.built

reasoning.decision.reached

wisdom.knowledge.retrieved

data.source.queried
```

### Kerülendő minták

```text
DecisionMade

BuildContext

DataQuery

WisdomUpdate

ProcessData

DecisionEvent
```

---

## Szabványos Esemény-katalógus

### Infrastruktúra és Hozzáférés

> Operational Trace események

| Kategória | Event Type | Szemantikai Gazda | Mikor keletkezik? |
|------------|------------|------------|------------|
| Gateway | gateway.request.routed | MCP Gateway | Kérés beérkezése és továbbítása |
| Gateway | gateway.response.returned | MCP Gateway | Válasz visszaküldése |
| Gateway | gateway.credential.redacted | MCP Gateway | Érzékeny adatok kitakarása |
| Auth | auth.passport.validated | MCP Layer | Jogosultság ellenőrzése |
| Auth | auth.access.denied | MCP Layer | Hozzáférés megtagadása |

---

### Döntéshozatal és Következtetés

> Business Trace események

| Kategória | Event Type | Szemantikai Gazda | Mikor keletkezik? |
|------------|------------|------------|------------|
| Reasoning | reasoning.context.built | Arcsi Core | Kontextus összeállt |
| Reasoning | reasoning.principle.applied | Arcsi Core | Egy elv alkalmazásra került |
| Reasoning | reasoning.falsification.executed | Arcsi Core | Ellenpróba lefutott |
| Reasoning | reasoning.decision.reached | Arcsi Core | Döntés megszületett |
| Reasoning | reasoning.decision.corrected | Arcsi Core | Korábbi döntés helyesbítése |

---

### Tudáskezelés

> Wisdom események

| Kategória | Event Type | Szemantikai Gazda | Mikor keletkezik? |
|------------|------------|------------|------------|
| Wisdom | wisdom.knowledge.retrieved | Wisdom Layer | Tudáselem lekérdezése |
| Wisdom | wisdom.candidate.created | Wisdom Layer | Új tudásjavaslat létrejötte |
| Wisdom | wisdom.lifecycle.transitioned | Wisdom Layer | Életciklus-váltás |
| Wisdom | wisdom.knowledge.superseded | Wisdom Layer | Tudáselem kiváltása |

---

### Adatforrások és Felhasználói Interakció

> Business Trace események

| Kategória | Event Type | Szemantikai Gazda | Mikor keletkezik? |
|------------|------------|------------|------------|
| Data | data.source.queried | Data Layer | Külső adatforrás lekérdezése |
| Data | data.mutation.executed | Data Layer | Külső rendszer módosítása |
| UI | ui.prompt.submitted | Teams / WebUI | Felhasználói kérdés beküldése |
| UI | ui.approval.submitted | Teams / WebUI | Jóváhagyás vagy elutasítás |

---

### Rendszerintegritás és Audit

> System Trace események

| Kategória | Event Type | Szemantikai Gazda | Mikor keletkezik? |
|------------|------------|------------|------------|
| Trace | trace.gap.detected | Trace Store | Hiányzó sorszám észlelése |
| Trace | trace.chain.incomplete | Trace Store | Lezáratlan folyamat észlelése |
| Audit | audit.batch.signed | Governance / Store | Aláírt eseményköteg létrehozása |

---

## Event Lifecycle Példa

A következő események egy teljes üzleti folyamatot írhatnak le:

```text
gateway.request.routed
            │
            ▼

auth.passport.validated
            │
            ▼

reasoning.context.built
            │
            ▼

wisdom.knowledge.retrieved
            │
            ▼

data.source.queried
            │
            ▼

reasoning.falsification.executed
            │
            ▼

reasoning.decision.reached
            │
            ▼

ui.approval.submitted
```

Az eseményszótár célja,
hogy ezek a folyamatok minden komponensben
ugyanazzal a jelentéssel jelenjenek meg.

---

## Bővíthetőségi Szabály

> Governance alapelv
>
> Új eseménytípus bevezetése
> nem igényel központi kódmódosítást.
>
> Az új típust azonban regisztrálni kell
> a közös Schema Registry-ben.

### Kötelező regisztráció

Minden új event_type esetén:

```text
Event Type
      │
      ▼

Payload Schema
      │
      ▼

Schema Registry
```

rögzítendő:

- eseménynév
- szemantikai gazda
- payload séma
- verzió
- dokumentáció

---

## Kapcsolat a Trace Emission Contract-tal

```text
Event Envelope
        │
        ▼
Payload Schema
        │
        ▼
Event Type
        │
        ▼
Közös Jelentés
```

> Az Event Envelope biztosítja,
> hogy egy esemény feldolgozható legyen.
>
> Az Event Type biztosítja,
> hogy egy esemény értelmezhető legyen.

---