# TRACE DATA POLICY

## ARCSI UNIVERSE

### Data Protection, Retention & Cryptographic Audit Specification

*Dátum: 2026-11-11*

*Kontextus:*

> Audi Universe
>
> Vállalati AI tervezés

*Fókusz:*

> • Privacy & PII Protection
>
> • Access Control (RBAC)
>
> • Data Retention & Archiving
>
> • Cryptographic Key Management
>
> • Audit & Compliance

---

## Cél

> A Trace Responsibility Model meghatározza,
> ki miért felelős.
>
> A Trace Emission Contract meghatározza,
> mit és hogyan bocsátunk ki.
>
> A Trace Data Policy meghatározza,
> hogyan védjük, őrizzük és auditáljuk
> a rögzített adatokat.

A dokumentum célja a:

- GDPR megfelelőség
- EU AI Act megfelelőség
- vállalati adatbiztonság
- kriptográfiai auditálhatóság

biztosítása a teljes trace-életciklus során.

---

## Alapelv

> A trace-rendszer célja
> az átláthatóság és a visszakövethetőség.
>
> Nem a korlátlan adatgyűjtés.
>
> Minden rögzített adatnak:
>
> - indokoltnak
> - védettnek
> - szabályozott életciklusúnak
>
> kell lennie.

---

## Adatvédelmi Osztályozás és PII Kezelés

> Adatvédelmi alapelv
>
> A Trace Store nem tárolhat
> nyers személyes adatokat
> vagy hitelesítő titkokat.
>
> Az azonosíthatóságot
> kriptográfiai álnevesítés biztosítja.

### Adatvédelmi osztályok

| Szint | Adatkategória | Példák | Kezelés |
|---------|---------|---------|---------|
| 0 | Public Metadata | timestamp, event_type, trace_level | Normál tárolás |
| 1 | Credentialök | API kulcsok, tokenek, jelszavak | Azonnali eltávolítás |
| 2 | Személyes adatok (PII) | név, e-mail, Entra ID, IP | Álnevesítés |
| 3 | Üzleti bizalmas adatok | BOM, SAP, projektelv | Titkosított tárolás |

### Végrehajtási felelősségek

| Kategória | Végrehajtó réteg |
|------------|------------|
| Credential Redaction | MCP Gateway |
| Pseudonymization | Governance Layer |
| Encryption & RBAC | Trace Store |

---

## Álnevesítési Szabályok

### Kriptográfiai Álnevesítés (Pseudonymization)

> Adatvédelmi alapelv
>
> A trace-rendszernek képesnek kell lennie
> ugyanazon felhasználó műveleteinek
> összekapcsolására,
> anélkül hogy a Trace Store
> közvetlen személyazonosító adatot tárolna.

A személyazonosító adatok helyett:

```text
user_hash
```

kerül tárolásra.

A rendszer célja:

- a felhasználói aktivitás követhetősége
- az auditálhatóság biztosítása
- a személy közvetlen azonosíthatóságának elkerülése

---

### Működési séma

```text
user_id / email
        │
        ▼

Pseudonymization
(Salted Hash)
        │
        ▼

user_hash
```

---

### Gyakorlati jelentése

A Trace Store nem azt tudja, hogy:

```text
istvan.radics@audi.hu
```

hajtotta végre az eseményt.

A Trace Store azt tudja, hogy:

```text
user_hash = 8f2c1a...
```

ugyanabban a folyamatban több eseményben is szerepelt.

Ez lehetővé teszi:

- az eseménylánc követését
- a viselkedési minták elemzését
- az auditálhatóságot

anélkül, hogy a valódi személyazonosság
része lenne a trace-adatoknak.

---

### Kriptográfiai jellemzők

A hash:

- sózott (salted)
- rendszer-szintű
- rotálható
- egyirányú

A só (salt) célja,
hogy az azonos bemenetekből képzett
hashek kívülről ne legyenek
egyszerűen visszafejthetők vagy összehasonlíthatók.

---

> Fontos különbségtétel
>
> A pseudonymization nem anonimizálás.
>
> A kapcsolat a felhasználó és a user_hash között
> továbbra is létezhet,
> de csak a szigorúan védett
> Identity Mapping Vault-on keresztül.

---

### Break-Glass Eljárás

> A pseudonymization nem jelent
> végleges anonimizálást.
>
> Bizonyos jogi vagy biztonsági esetekben
> kontrollált visszafejtés lehetséges.

Feltételek:

- Security Officer jóváhagyás
- Compliance Officer jóváhagyás
- Audit nyomvonal kötelező

### Identity Mapping Vault

```text
user_hash
        │
        ▼

Identity Mapping Vault
        │
        ▼

Real Identity
```

---

## Hozzáférési Szabályok (RBAC)

> Hozzáférési alapelv
>
> Az írási és az olvasási jog
> szigorúan elválik.
>
> Senki sem rendelkezhet
> korlátlan módosítási jogosultsággal.

### Jogosultsági mátrix

| Szerepkör | Operational | Business | Identity Mapping | Audit |
|------------|------------|------------|------------|------------|
| Kibocsátó komponens | Append | Append | Nincs | Nincs |
| Üzemeltető | Olvasás | Metaadat | Nincs | Nincs |
| Projekt Tag | Nincs | Saját projekt | Nincs | Nincs |
| Knowledge Steward | Nincs | Tudásláncok | Nincs | Nincs |
| Auditor | Teljes | Teljes | Nincs | Verifikáció |
| Compliance + Security | Teljes | Teljes | Break-Glass | Teljes |

---

## Megőrzési és Archiválási Szabályok

> Megőrzési alapelv
>
> A megőrzési idő nem az adat értékét,
> hanem az adat bizonyítási és
> auditálási szerepét tükrözi.

### Tárolási életciklus

```text
Hot Storage
      │
      ▼

Warm / Cold Archive
(WORM)
      │
      ▼

Crypto-Shredding
```

### Retention Schedule

| Trace Típus | Hot Storage | Archive | Teljes Retention |
|------------|------------|------------|------------|
| Operational Trace | 30 nap | 60 nap | 90 nap |
| Business Trace | 1 év | 4-9 év | 5-10 év |
| Wisdom Lifecycle | Aktív életciklus | Archiválás | Korlátlan |
| Audit Batches | 1 év | 9 év | 10 év |

---

## GDPR és Append-Only Együttélése

### Crypto-Shredding

> A törlési kötelezettség
> nem írhatja felül
> az integritási követelményt.

A rendszer ezért nem törli:

- az eseményt
- a hash-t
- a láncot

Hanem a kulcsot semmisíti meg.

### Működési séma

```text
Encrypted Data
        │
        ▼

Encryption Key
        │
        ▼

Key Destruction
        │
        ▼

Data Irrecoverable
```

### Eredmény

| Elem | Megmarad |
|--------|--------|
| Event | ✓ |
| Hash Chain | ✓ |
| Audit Trail | ✓ |
| Visszaolvasható tartalom | ✗ |

---

## Kriptográfiai Kulcskezelés

> Kriptográfiai alapelv
>
> Egy digitális aláírás
> csak annyira megbízható,
> amennyire a privát kulcs védett.

### Kulcskezelési szabályok

#### Hardveres védelem

A privát kulcsok:

```text
HSM
```

vagy

```text
Enterprise KMS
```

rendszerben tárolhatók.

Exportálásuk tilos.

---

#### Kulcsrotáció

Példa:

```text
90 nap
```

A tényleges értéket a vállalati policy határozza meg.

### Rotációs modell

```text
Old Key
    │
    ▼

Retired

    │
    ▼

Archivált Public Key

    │
    ▼

New Key
```

---

#### RFC3161 Időbélyeg

Minden Audit Batch:

- aláírt
- időbélyegzett
- archivált

---

## Audit Verifikáció

> Audit alapelv
>
> Az auditáló rendszer nem módosíthatja
> a trace-t.
>
> Kizárólag ellenőrizheti azt.

### Audit Watchdog

```text
Trace Store
      │
      ▼

Hash Chain Verification
      │
      ▼

Signature Verification
      │
      ▼

Audit Report
```

### Ellenőrzési szintek

#### Napi

- Gap Detection
- Sequence ellenőrzés
- Hash Chain validáció

#### Heti / Havi

- Signed Batch ellenőrzés
- Időbélyegek ellenőrzése

#### Incidens

- P1 Security Incident
- Integritási vizsgálat
- Audit riport

---

## A Három Dokumentum Egysége

```text
┌───────────────────────────────────┐
│ Trace Responsibility Model        │
│ Ki mit csinál?                    │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│ Trace Emission Contract           │
│ Mit és hogyan írunk?              │
└───────────────┬───────────────────┘
                │
                ▼
┌───────────────────────────────────┐
│ Trace Data Policy                 │
│ Hogyan védjük és őrizzük meg?     │
└───────────────┬───────────────────┘
                │
                ▼
      GOVERNED TRACE ARCHITECTURE
```

---

> Végső alapelv
>
> A felelősségi modell adja a rendet.
>
> A kibocsátási szerződés adja a közös nyelvet.
>
> Az adatkezelési szabályzat adja a bizalmat.
>
> A három együtt teremti meg
> az auditálható és vállalati szinten
> védhető AI-rendszert.

---