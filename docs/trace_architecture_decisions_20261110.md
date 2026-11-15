# ARCSI UNIVERSE
## VÁLLALATI ARCHITEKTÚRA DÖNTÉSEK
### Trace Responsibility Model


*Dátum: 2026-11-10*

*Kontextus:* 
>Audi Universe, vállalati AI tervezés

*Fókusz:*
> Trace • Wisdom • Data Policy



---

## Kiindulópont

> Architektúra
>
> Az ARCSI Universe egy projektközpontú,
> tudás- és fejlődéskezelő vállalati platform,
> amely több rétegben kapcsolja össze a
> felhasználókat, a tudást, a döntési folyamatokat
> és a vállalati adatforrásokat.

### Architektúra rétegei

```text
┌────────────────────────────────────┐
│ User Roles                         │
│ Entra ID / Microsoft Graph         │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│ Teams + WebUI                      │
│ End User & Administration          │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│ MCP Layer                          │
│ Runtime Passport                   │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│ Governance Layer                   │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│ Wisdom Layer                       │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│ Arcsi Core                         │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│ MCP Gateway                        │
└────────────────┬───────────────────┘
                 ▼
┌────────────────────────────────────┐
│ Data Layer                         │
└────────────────────────────────────┘
```

### Rétegenkénti szerepkörök
|Réteg|	Feladat|
|----------|----------|
|User Roles|	Felhasználók, projekt tagok, vezetők, adminisztrátorok|
|Teams + WebUI|	Operatív és adminisztratív felület|
|MCP Layer|	Runtime Passport és kontextuskezelés|
|Governance Layer|	Policy, approval és compliance|
|Wisdom Layer|	Tudás, elvek és fejlődési minták|
|Arcsi Core|	Kontextusépítés és döntéshozatal|
|MCP Gateway|	Forgalomirányítás, trace begyűjtés|
|Data Layer|	Vállalati és projekt adatforrások|

## Tudás-életciklus 

```text
candidate
    ↓
under_review
    ↓
validated
    ↓
accepted
    ↓
active
    ↓
deprecated
    ↓
rejected 
```
### Stratégiai célok
  - Gyorsabb információhozzáférés
  - Kevésbé ismétlődő hiba
  - Hatékonyabb projektmunka
  - Jobb döntések (bizonyítékokkal)
  - Tudásmegtartás és fejlődés
  - Átlátható és auditálható működés
---


## A FŐ ARCHITEKTURÁLIS DÖNTÉS — TRACE FELELŐSSÉGI MODELL


KIINDULÓ FELVETÉS (módosítva):
  Az MCP Gateway felelős a trace rögzítésért és részletes naplózásért.

> Végleges döntés
>
> Az MCP Gateway nem a trace-rendszer központi feldolgozója.
>
> A Gateway a strukturált események
> begyűjtési és továbbítási pontja.
>
> A trace-adatok kezelésének szabályait
> a Governance Layer határozza meg.

---

## NÉGY KOMPONENS — HÁROM KÜLÖNBÖZŐ FELELŐSSÉGI SZEREP



| Komponens           | Szerep           | Kérdés, amire válaszol           |
|---------------------|------------------|----------------------------------|
| MCP Gateway         | Collection layer | Milyen esemény érkezett?         |
|                     |                  | (begyűjtés, minimális technikai  |
|                     |                  |  szűrés, correlation ID továbbít)|
| Durable Queue       | Transport Layer + Data Protection  | Hogyan jut el az esemény biztonságosan és változatlanul?        |
| Governance Layer    | Policy authority | Mit szabad kezdeni ezzel az      |
|                     |                  | eseménnyel?                      |
|                     |                  | (adatvédelem, hozzáférés,        |
|                     |                  |  maszkolás, retention, integritás)|
| Central Trace Store | Storage layer    | Hogyan őrizzük meg változatlanul |
|                     |                  | és visszakereshetően?            |
|                     |                  | (append-only tárolás,            |
|                     |                  |  eseménykapcsolatok, integritás) |




Adatfolyam:
```text
┌────────────────────────────────────┐
│ MCP Gateway                        │
│ Role: Collector                    │
└────────────────┬───────────────────┘
                 │
                 │ Structured Event
                 ▼
┌────────────────────────────────────┐
│ Durable Queue                      │
│ Role: Transport Layer              │
└────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────┐
│ Governance Layer                   │
│ Role: Policy Authority             │
└────────────────┬───────────────────┘
                 │
                 ▼
┌────────────────────────────────────┐
│ Central Trace Store                │
│ Role: Append-Only Storage Layer    │
└────────────────────────────────────┘
```
---

## Két Trace Szint

### Operational Trace

> Infrastruktúra és biztonsági nyomvonal
>
> A rendszer technikai működésének,
> hozzáféréseinek és végrehajtásának
> rekonstruálható története.

Jellemző kérdések:

- Ki kezdeményezte a kérést?
- Mikor történt?
- Melyik szolgáltatás fogadta?
- Engedélyezte-e a rendszer?
- Mennyi ideig tartott?
- Milyen technikai eredménnyel zárult?

Tulajdonságok:

| Jellemző | Érték |
|-----------|-----------|
| Fókusz | Infrastruktúra |
| Tartalom | Technikai események |
| Cél | Monitoring, audit, hibakeresés |
| Durability SLO | Best Effort |
| Elvesztés | Max. ~1 esemény / óra |

---

### Business / Reasoning Trace

> Tudás- és döntési nyomvonal
>
> A rendszer által felhasznált
> kontextusok, bizonyítékok,
> szabályok és eredmények
> strukturált rögzítése.

Jellemző kérdések:

- Milyen projektkontextus volt aktív?
- Milyen tudáselemeket használt a rendszer?
- Milyen elvek befolyásolták a döntést?
- Történt-e falsification?
- Milyen következtetés született?
- Történt-e állapot- vagy tudásváltozás?

Tulajdonságok:

| Jellemző | Érték |
|-----------|-----------|
| Fókusz | Döntések és tudás |
| Tartalom | Üzleti események |
| Cél | Auditálható döntéshozatal |
| Durability SLO | Zero Loss |
| Megőrzés | At-Least-Once |
| Deduplikáció | Idempotens |

---

> Fontos elv
>
> A Reasoning Trace nem a modell
> belső gondolatmenetének naplózása.
>
> A Reasoning Trace a döntéshez
> felhasznált:
>
> - források
> - alkalmazott elvek
> - ellenőrzési lépések
> - eredmények
>
> strukturált rögzítése.

Ennek előnyei:

- auditálhatóbb működés
- egyszerűbb megfelelőség
- GDPR-kompatibilisebb kezelés
- AI Act szempontból védhetőbb működés
- jobb visszakövethetőség

Kapcsolat a két trace-szint között

```text
┌───────────────────────┐         ┌───────────────────────┐
│ Operational Trace     │◄───────►│ Business Trace        │
│ (mit csinált)         │         │ (miért)               │
└───────────┬───────────┘         └───────────┬───────────┘
            │                                 │
            └────────────────┬────────────────┘
                             │
                        Correlation ID
                             │
                             ▼
                     Egységes történet
```

A két trace egymást kiegészíti.

Az Operational Trace megmutatja,
hogy a rendszer mit csinált.

A Business Trace megmutatja,
hogy miért jutott az adott eredményre.

---

## CORRELATION ID + W3C TRACE CONTEXT


Két különböző azonosító, két különböző célra:


| Azonosító      | Szint    | Cél              | Formátum            |
|----------------|----------|------------------|---------------------|
| Trace ID       | Technikai| Request lánc    | W3C traceparent (32 hex)     |
| Correlation ID | Üzleti   | Döntési lánc     | pl. REQ-2026-001    |


Példa adatfolyam:

```text
  TEAMS KÉRDÉS
    ↓

CORRELATION ID
(REQ-2026-001)
    ↓

MCP GATEWAY
    ├─ Operational Trace
    ├─ Arcsi Core
    │   └─ Reasoning Trace
    ├─ Wisdom Layer
    │   └─ Knowledge Trace
    └─ Data Layer
        └─ Data Access Trace
    ↓

TRACE COLLECTOR
    ↓

TRACE STORAGE
```

Egyetlen kérés teljes életciklusa rekonstruálható.
A W3C Trace Context ajánlott, mert OpenTelemetry-kompatibilis
és más vállalati szolgáltatásokkal interoperábilis.

---

## SOURCE OF TRUTH — HIBRID MODELL


Nem egyetlen központi gazda van, hanem minden eseménynek
megvan a saját "szemantikai gazdája":


| Terület                                   | Események eredeti gazdája     |
|-------------------------------------------|-------------------------------|
| Infrastruktúra, hitelesítés, hozzáférés   | Gateway / IT                  |
| Reasoning és döntési folyamat             | Arcsi Core                    |
| Tudás- és elvváltozások                   | Wisdom Layer                  |
| Adatforrás-hozzáférések                   | Data Layer                    |


A közös Trace Store az események egységes, append-only gyűjteménye.

FONTOS KÜLÖNBSÉGTÉTEL:
  - Az esemény TARTALMÁNAK hiteles forrása az azt kibocsátó komponens.
  - A központi Trace Store az események közös, visszakereshető
    nyilvántartása.

A Gateway nem találhatja ki és nem értelmezheti az üzleti eseményeket.

---

## Trace Emission Contract

> Kulcsállítás
>
> A teljes modell legfontosabb dokumentuma
> nem a Gateway specifikáció,
> hanem a közös Trace Emission Contract.

### Mit szabályoz?

| Terület | Meghatározás |
|----------|----------|
| Kibocsátók | Mely komponensek küldenek eseményt |
| Triggerpontok | Mikor kötelező a trace |
| Eseményséma | Milyen mezők kötelezőek |
| Azonosítók | Trace ID és Correlation ID kapcsolata |
| Hiányzó események | Mi történik elveszett trace esetén |
| Minőségbiztosítás | Trace teljességi ellenőrzés |

### Kötelező trace-kibocsátók

- Arcsi Core
- Wisdom Layer
- Data Layer
- Teams UI
- Next.js WebUI

### Kötelező trace-események

- State mutation műveletek
- Falsification lépések
- Approval műveletek
- Knowledge retrieval
- Data access

### Minimális eseményséma

```text
timestamp
correlation_id
trace_id
component
event_type
source_of_truth

opcionális:
payload
context
severity
```

> Trace teljességi alapelv
>
> A hiányzó esemény is esemény.
>
> Ha nem rögzítjük a hiányt,
> a trace látszólag teljes lesz,
> miközben valójában hiányos.

---

## Adatvédelem — Három Kategória

### Credentialök

> Kritikus szabály
>
> Credential nem kerülhet:
>
> - naplóba
> - trace queue-ba
> - tartós tárolóba
> - illetéktelen komponenshez

A Gateway végezhet:

- Credential redaction
- Technikai szűrés

A Gateway nem végezhet:

- Üzleti policy döntést

### Személyes adatok

| Típus | Kezelés |
|---------|---------|
| Név | Álnevesítés |
| Email | Álnevesítés |
| User ID | Hash |
| IP-cím | Policy alapú kezelés |

Ajánlott:

```text
user_hash
```

nem pedig:

```text
real_user_id
```

Példa:

```text
user_id: 12345        →  user_hash: a3f8b2...
email: kovacs.bela@x  →  email_hash: 7c2e9a...
ip: 10.20.30.40       →  ip_scope: 10.20.x.x (policy)
```

### Üzleti bizalmas adatok

| Trace típus | Tartalom |
|-------------|-----------|
| Operational Trace | Metaadat |
| Business Trace | Ellenőrzött üzleti tartalom |

---

## Trace Integritás

> Integritási cél
>
> A Trace Store nem csupán tárolja az eseményeket.
>
> Biztosítania kell, hogy a történet
> utólag ne legyen észrevétlenül
> módosítható vagy manipulálható.

### Integritási szintek

| Szint | Mechanizmus | Cél |
|---------|---------|---------|
| Alapszint | Append-Only | Véletlen módosítások elleni védelem |
| Emelt szint | Hash Chain | Eseménysorrend integritása |
| Audit-szint | Signed Batches | Kriptográfiai bizonyíthatóság |

### Integritási modell

```text
┌─────────────────────┐
│ Append-Only Store   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Hash Chain          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Signed Batches      │
└─────────────────────┘
```

### Alapszint

Az esemény:

- létrehozható
- lekérdezhető
- archiválható

Az esemény nem:

- írható felül
- módosítható
- törölhető jogosulatlan módon

### Emelt szint

Minden esemény tartalmazza:

```text
event_hash
previous_event_hash
```

Példa:

```text
Event A
   │
   └─ Hash A

Event B
   │
   ├─ Previous = Hash A
   └─ Hash B

Event C
   │
   ├─ Previous = Hash B
   └─ Hash C
```

Ha egy korábbi esemény módosulna,
a lánc megszakadna és az eltérés
észlelhetővé válna.

### Audit-szint

> Kriptográfiai bizonyíthatóság
>
> Az Emelt szint (Hash Chain) biztosítja,
> hogy az eseménylánc belsőleg konzisztens legyen.
>
> Önmagában azonban nem akadályozza meg,
> hogy valaki a teljes láncot módosítás után
> újraszámolja.

A Signed Batch célja egy külső,
időben rögzített bizonyíték létrehozása.

### Miért szükséges?

Hash Chain nélkül:

```text
Event B módosul
      │
      ▼
A változás nem feltétlenül észlelhető
```

Hash Chain esetén:

```text
Event B módosul
      │
      ▼
Hash eltérés keletkezik
      │
      ▼
A manipuláció észlelhető
```

Hash Chain + Signed Batch esetén:

```text
Event B módosul
      │
      ▼
A teljes lánc újraszámolható
      │
      ▼
De az eredeti aláírás
érvénytelenné válik
```

### Audit-folyamat

A rendszer időszakosan:

- kötegekbe rendezi az eseményeket
- hash-t számol a teljes kötegről
- digitálisan aláírja a hash-t
- archiválja az aláírt eredményt

```text
Events
   │
   ▼

Batch Hash
   │
   ▼

Digital Signature
   │
   ▼

Audit Archive
```

### Mit bizonyít az aláírás?

> A Signed Batch nem azt bizonyítja,
> hogy egy eseménylánc konzisztens.
>
> Azt bizonyítja,
> hogy a lánc egy korábbi időpillanatban
> pontosan ebben az állapotban létezett.

### Integritási lánc

```text
┌─────────────────────┐
│ Append-Only Store   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Hash Chain          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Signed Batches      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Audit Verification  │
└─────────────────────┘
```

### Eredmény

| Szint | Mit véd? |
|--------|----------|
| Append-Only | Véletlen vagy jogosulatlan módosítás |
| Hash Chain | Eseménysorrend integritása |
| Signed Batch | Utólagos manipuláció bizonyítható felismerése |
| Audit Verification | Független ellenőrizhetőség |

> Audit alapelv
>
> Az integritás végső célja nem csupán
> a manipuláció észlelése.
>
> Az integritás végső célja annak
> bizonyíthatósága, hogy a rendszer
> története egy adott időpillanatban
> pontosan milyen állapotban létezett.

---

> Integritási alapelv
>
> A Governance nem módosíthatja
> visszamenőleg a történetet.
>
> Ha egy eseményt helyesbíteni kell,
> új esemény keletkezik,
> amely hivatkozik az eredeti eseményre.

### Helyesbítési modell

```text
Original Event
        │
        ▼
Correction Event
        │
        ▼
Supersession Link
```

Az eredeti esemény:

- megmarad
- visszakereshető
- auditálható

A helyesbítő esemény:

- hivatkozik az eredetire
- felülírja annak jelentését
- nem törli a múltat

---

> Supersession alapelv
>
> A történelem nem törlődik.
>
> A régi esemény obsolete státuszba kerül.
>
> Az új esemény hivatkozik rá.
>
> Ez biztosítja a folytonosságot,
> az auditálhatóságot és az átláthatóságot.

### Architekturális kapcsolat

```text
Governance Layer
        │
        │ szabályoz
        ▼

Trace Store
        │
        │ megőriz
        ▼

Audit Trail
        │
        │ bizonyít
        ▼

Trust
```

A Trace integritás célja nem pusztán
a tárolás biztonsága.

A cél annak bizonyíthatósága,
hogy a rendszer története
utólag sem módosult észrevétlenül.

---

## Három Specifikáció — Következő Lépések

> Architekturális alapelv
>
> A Trace Responsibility Model önmagában
> még nem tesz működőképessé egy rendszert.
>
> A modell implementálásához három,
> egymásra épülő specifikáció szükséges.

### A három dokumentum szerepe

| Dokumentum | Kérdés | Felelős |
|------------|---------|---------|
| Trace Responsibility Model | Ki miért felelős a trace életciklusában? | Architektúra |
| Trace Emission Contract | Milyen eseményeket és milyen formában kell kibocsátani? | Minden komponens |
| Trace Data Policy | Hogyan kezeljük az adatvédelmet, hozzáférést és megőrzést? | Governance |

### Kapcsolatuk egymással

```text
┌─────────────────────────────┐
│ Trace Responsibility Model  │
│ Ki miért felelős?           │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Trace Emission Contract     │
│ Mit kell kibocsátani?       │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Trace Data Policy           │
│ Hogyan kell kezelni?        │
└─────────────────────────────┘
```

### Ajánlott kidolgozási sorrend

#### 1. Trace Responsibility Model

Célja:

- szerepkörök tisztázása
- felelősségi körök meghatározása
- komponensek szétválasztása

Eredménye:

```text
Ki mit csinál?
```

---

#### 2. Trace Emission Contract

Célja:

- kötelező események meghatározása
- eseményséma létrehozása
- komponensek közötti egységes működés

Eredménye:

```text
Mit kell naplózni?
```

---

#### 3. Trace Data Policy

Célja:

- adatvédelmi szabályok rögzítése
- megőrzési időszakok definiálása
- hozzáférések szabályozása
- integritási követelmények meghatározása

Eredménye:

```text
Hogyan kell kezelni?
```

---

### Fejlesztési útvonal

```text
Felelősség
      │
      ▼
Kibocsátás ◄──────┐
      │           │
      ▼           │
Adatkezelés ──────┘  (iteratív)
      │
      ▼
Auditálható rendszer
```

> Gyakorlati megközelítés
>
> A sorrend nem véletlen.
>
> Először meg kell határozni,
> hogy ki felel az eseményekért.
>
> Ezután lehet definiálni,
> hogy milyen események léteznek.
>
> Végül szabályozható,
> hogy ezek az események
> hogyan kezelhetők és őrizhetők meg.

### Végállapot

```text
Trace Responsibility Model
            │
            ▼
Trace Emission Contract
            │
            ▼
Trace Data Policy
            │
            ▼
Governed Trace Architecture
```

A három dokumentum együtt alkotja az
ARCSI Universe teljes trace-governance keretrendszerét.

---

## Stratégiai Üzenet

> Elsődleges állítás
>
> Az Arcsi nem csupán a rendszer válaszát
> teszi visszakövethetővé.
>
> Az Arcsi a válaszhoz vezető döntési folyamat
> releváns, strukturált eseményeit is rögzíti.
>
> A technikai,
> adat-hozzáférési és
> üzleti trace-eket
> közös azonosítók kapcsolják össze,
> miközben az adatvédelmi és megőrzési szabályokat
> külön Governance Layer kezeli.

### Mit jelent ez a gyakorlatban?

```text
Operational Trace
        │
        ▼

Reasoning Trace
        │
        ▼

Knowledge Trace
        │
        ▼

Data Access Trace
        │
        ▼

Correlation ID
        │
        ▼

Egységes történet
```

A cél nem csupán a rendszer viselkedésének
visszakereshetősége, hanem annak megértése is,
hogy egy adott eredmény hogyan alakult ki.

---

> Másodlagos állítás
>
> Nem a modell belső gondolatmenetét naplózzuk.
>
> A rendszer által felhasznált:
>
> - bizonyítékokat
> - forrásokat
> - szabályokat
> - ellenőrzési lépéseket
> - eredményeket
>
> rögzítjük strukturált formában.

### A két megközelítés különbsége

| Nem cél | Cél |
|----------|----------|
| Belső modellgondolatok | Döntési bizonyítékok |
| Rejtett reasoning | Auditálható reasoning |
| Modellállapot | Döntési kontextus |
| Nem reprodukálható folyamat | Rekonstruálható folyamat |

---

> Architekturális állítás
>
> Az Arcsi architektúrájában
> az infrastruktúra-,
> adat-hozzáférési és
> üzleti döntési nyomvonal
> egyetlen Correlation ID
> alatt kapcsolódik össze.

### Kapcsolódó nyomvonalak

```text
                 Correlation ID
                        │
     ┌──────────────────┼──────────────────┐
     │                  │                  │
     ▼                  ▼                  ▼

Operational      Knowledge        Business
   Trace            Trace           Trace

     │                  │                  │
     └──────────────────┼──────────────────┘
                        │
                        ▼

                Teljes történet
```

Ennek eredménye, hogy egyetlen kérés teljes
életciklusa visszakövethető:

- ki indította
- milyen tudást használt
- milyen adatokat ért el
- milyen döntések születtek
- milyen eredmény keletkezett

---

> Fontos megkülönböztetés
>
> Ez nem azért különleges,
> mert más rendszerek erre nem képesek.
>
> Az állítás lényege az,
> hogy az Arcsi architektúrájában
> ezek a nyomvonalak tudatosan
> összekapcsolt részei ugyanannak
> a kormányzott rendszernek.

### Üzenet egy mondatban

> Az Arcsi nemcsak válaszokat ad,
> hanem visszakövethetően dokumentálja
> a válaszokhoz vezető bizonyítékokat,
> döntési lépéseket és adatkapcsolatokat is.

---
## Filozófiai Összefüggés

> Az Arcsi filozófiája
>
> A Governance védi és szabályozza a történetet.
>
> A Trace megőrzi a történetet.
>
> A Wisdom a megfelelően értékelt
> tapasztalatokból tanulhat.

Az Arcsi Univerzum eredeti filozófiája
vállalati szintre emelve ugyanazt a logikát követi,
mint az egyéni Arcsi rendszer.

### Egyéni szint (jelenlegi működés)

| Terület | Megvalósítás |
|----------|----------|
| Governance | wisdom_supersede.py guard-ok |
| Trace | research_trace |
| Wisdom | wisdom.json |

### Vizuális modell

```text
┌─────────────────────┐
│ Governance          │
│ Supersession Rules  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Trace               │
│ research_trace      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Wisdom              │
│ wisdom.json         │
└─────────────────────┘
```

---

### Vállalati szint (tervezett modell)

| Terület | Megvalósítás |
|----------|----------|
| Governance | Policy Engine + Approval Workflow + Risk & Compliance |
| Trace | Operational Trace + Business Trace |
| Wisdom | Project Wisdom + Corporate Meta Wisdom + Knowledge Graph |

### Vizuális modell

```text
┌──────────────────────────────────┐
│ Governance Layer                 │
│ Policy + Approval + Compliance   │
└───────────────┬──────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│ Trace Layer                      │
│ Operational + Business Trace     │
└───────────────┬──────────────────┘
                │
                ▼
┌──────────────────────────────────┐
│ Wisdom Layer                     │
│ Project + Corporate Knowledge    │
└──────────────────────────────────┘
```

---

### Architekturális folytonosság

> Az Arcsi Universe nem új filozófiára épül.
>
> A vállalati architektúra
> a már bizonyított egyéni minták
> skálázott továbbfejlesztése.

### A fejlődési út

```text
Személyes Arcsi
       │
       ▼
Research Trace
       │
       ▼
Wisdom Supersession
       │
       ▼
Projekt Wisdom
       │
       ▼
Corporate Wisdom
```

### Miért fontos a Trace?

A Trace nem csupán auditálási eszköz.

A Trace lehetővé teszi:

- döntések visszakövetését
- hibák elemzését
- tudásváltozások megértését
- működési minták felismerését
- metaelvek kialakítását

### A Trace szerepe az Arcsi Univerzumban

```text
Történet
    │
    ▼
Trace
    │
    ▼
Értékelés
    │
    ▼
Wisdom
    │
    ▼
Jobb döntések
```

---

> Filozófiai következtetés
>
> Az esemény önmagában nem tudás.
>
> A visszakövethető eseményből lehet tapasztalat.
>
> A kiértékelt tapasztalatból lehet Wisdom.
>
> Az Arcsi Universe ezt a fejlődési láncot
> próbálja vállalati szinten támogatni.

---

## Kulcselvek Összefoglalása

> Az Arcsi Universe trace-architektúrája néhány
> egyszerű, de következetesen alkalmazott
> alapelvre épül.
>
> Ezek az elvek határozzák meg a rendszer
> működését, felelősségi viszonyait és
> auditálhatóságát.

### Az architektúra alaptörvényei

| # | Elv |
|---|-----|
| 1 | Gateway = collector, nem processor |
| 2 | Governance = policy authority, nem history writer |
| 3 | Trace Store = storage layer, append-only működés |
| 4 | Adatfolyam: Gateway → Governance → Store |
| 5 | Credential hygiene a Gateway-ben, policy a Governance-ben |
| 6 | Két trace-szint: Operational + Business |
| 7 | Correlation ID és W3C Trace Context együtt használatos |
| 8 | Hibrid Source of Truth modell |
| 9 | Trace Emission Contract szabályozza az eseménykibocsátást |
| 10 | Integritás: append-only + hash chain + signed batches |
| 11 | A múlt nem írható át |
| 12 | A Reasoning Trace nem belső gondolatmenet |

---

### Az elvek kapcsolata

```text
Gateway
    │
    ▼
Governance
    │
    ▼
Trace Store
    │
    ▼
Audit Trail
    │
    ▼
Trust
```

---

### Felelősségi modell

```text
Gateway
    │
    └─ Begyűjt

Governance
    │
    └─ Szabályoz

Trace Store
    │
    └─ Megőriz

Wisdom
    │
    └─ Tanul
```

---

### Trace modell

```text
Operational Trace
         +
Business Trace
         +
Correlation ID
         +
Trace Integrity
         │
         ▼
Auditálható rendszer
```

---

> Integritási alapelv
>
> A rendszernek nem csupán helyesnek,
> hanem visszakövethetően helyesnek kell lennie.

---

> Governance alapelv
>
> A Governance nem írhatja át a történetet.
>
> A Governance szabályozza a történetet.

---

> Trace alapelv
>
> A Trace feladata nem a döntések létrehozása.
>
> A Trace feladata a döntések
> rekonstruálható megőrzése.

---

> Wisdom alapelv
>
> A Wisdom nem eseményeket,
> hanem kiértékelt tapasztalatokat kezel.

---

> Reasoning alapelv
>
> A Reasoning Trace nem a modell
> belső gondolatmenetének naplózása.
>
> A Reasoning Trace a döntéshez vezető
> bizonyítékok, források, ellenőrzések
> és következtetések strukturált nyilvántartása.

---

### Egy mondatos összefoglaló

```text
Gyűjtsd be.     →  Trace (MCP Gateway)
Szabályozd.     →  Governance Layer
Őrizd meg.      →  Trace Store
Értékeld ki.    →  Wisdom (falsification)
Tanulj belőle.  →  Wisdom (validated)
```

Ez az Arcsi Universe trace- és tudáskezelési
modelljének tömör megfogalmazása.

---



