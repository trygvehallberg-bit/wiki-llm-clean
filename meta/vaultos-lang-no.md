# VaultOS language/form pack — Norwegian (`no`)

> **Imported by `CLAUDE.md` via `@import` — not a wiki page.** No `kind:` frontmatter; outside wiki operations (§B.2).
>
> This is the **Norwegian language/form pack** for VaultOS: the section names, infobox field labels, and prose anti-patterns that fill the portable Part B pattern for a Norwegian wiki. It is **part of VaultOS but optional and swappable** — a non-Norwegian vault replaces it with its own `vaultos-lang-<xx>.md`. The *pattern* (which sections exist, that an infobox defines jargon, that prose must read as mother-tongue) stays in `CLAUDE.md` Part B; this pack supplies the Norwegian *fill*.
>
> **Provisional note (single source of truth):** these section names and field labels are currently **also hardcoded in the `wiki-*` skills**, which are not yet wired to read this file (deferred — see proposal-003 roadmap). Until that step, the skills + Part B remain the single source of truth; this pack mirrors them for portability staging. When the skills are parameterized, lint Check 9a should be extended to police config↔skill drift.

## Standard source-page section headings
- `## Nøkkelpåstander`
- `## Kontekst`
- `## Åpne spørsmål`
- `## Kryssreferanser`

**Transcript extension** (source pages whose `source_path` is under `raw/transcripts/`), inserted between `## Kontekst` and `## Åpne spørsmål`:
- `## Talere`
- `## Metadata for foredraget`
- `## Tidsstemplede høydepunkter`
- `## Spørsmål og svar` (optional)

**Synthesis pages** may use `## Hvor klyngen er stille` for what the cited sources collectively do not address.

## Infobox field labels (by kind)
Infobox field labels are Norwegian on wiki pages. The field *roles* (what each slot carries) are the portable pattern in §B.3 "Infobox sidebar"; the labels below are the Norwegian fill.

- **Source pages:** `Type` · `Foredragsholder/forfatter` · `Dato / arena` · `## Nøkkelbegreper`
- **Entity pages:** `Type` · `Rolle` · `Tilknytninger` · `Kilder` · `## Nøkkelbegreper`
- **Concept pages:** `Kort definisjon` · `Argumentert av` · `Relatert` · `## Nøkkelbegreper`

## Skrive- og strukturstandard (fire bøtter)

Den positive konstruksjonsregelen for wiki-prosa — hvordan en side bygges og leses — kuratert fra Store norske leksikons forfatterveiledning og Språkrådets klarspråk. Den styrer *all* skriving i vaulten: `/wiki-ingest` skriver førsteutkastet til standarden, `/wiki-editor` bruker den som målestokk, og `/wiki-query`/`/wiki-synthesis` følger den når de skriver prosa. De sju anti-mønstrene under («Naturlig norsk») er den negative siden av bøtte 3. Det portable skjelettet (bøtte-navnene) bor i `CLAUDE.md` §B.3; dette er det norske innholdet.

### Bøtte 1 — Struktur og disposisjon
- **Definisjon og ingress.** Første setning definerer oppslagsordet («X er …»); åpningsavsnittet er hele siden i miniatyr. Gå rett på saken — ikke «betegnelse for».
- **Stigende vanskelighetsgrad (omvendt pyramide).** Synkende viktighet, stigende vanskegrad: det enkleste og viktigste først, det smale og kompliserte sist. Welcome-mat-disiplinen gjelder også seksjonsåpninger, ikke bare sidens første linje.
- **Én side, ett tema.** Del flertydige oppslag i egne sider; bruk en hub når et tema er for stort for én side (companion-hub-/hub-konsept-mønsteret).
- **Riktig lengde, ikke maksimal.** Fortell det viktigste, ikke alt. Spenningen mot bok-ingestens «mett, ikke kort» løses slik: mett dybden i én meningsenhet, men del siden når den smelter sammen flere tema.
- **Beskrivende mellomtitler.** Allmenne stikkord («Årsak», «Behandling», «Bakgrunn») framfor kreative overskrifter — i tillegg til de kanoniske seksjonsnavnene over.
- **Lenketetthet og wikilenker.** Lenk rikelig inline med `[[wikilenker]]` (aldri rå stier), og samle videre lesning i `## Kryssreferanser` nederst. Inline-lenkene bærer den løpende teksten; bunnseksjonen bærer det leseren bør lese etterpå.
- **Callouts og infoboks.** Callouts brukes for semantisk type (ikke variasjon), og infoboks-disiplinen gjelder — begge definert i `CLAUDE.md` §B.3.

### Bøtte 2 — Klarhet for leseren
- **Stranger-test** (første linje + infoboks). Begge skal være lesbare for en nysgjerrig nykommer som verken har lest kilden eller kjenner taleren. Testen dekker velkomstmatta (første linje + infoboks), ikke tapetet: bodyen under får bruke fagordene infoboksen definerer og siden handler *om*. Led med hva kilden hevder eller hva siden dekker; attribusjon kommer etter substansen.
- **Definer fagord én gang.** Bruk dublett («halsbetennelse (tonsillitt)») eller en inline-definisjon første gang ordet dukker opp. Forklar aldri ett fagord med et annet. Sidens vokabular defineres i infoboksens `## Nøkkelbegreper`, så bodyen kan bruke det fritt.
- **Jargon må gjøre arbeid, ellers kuttes den.** Et fagord er bærende hvis setningen kollapser uten det. Test: bytt ordet med sin egen definisjon — mister setningen ingenting, var ordet dekorativt.
- **Ikke smugle det du forklarer inn i analogien.** Krever X en analogi Y som bare gir mening via X, etterlater den leseren mer forvirret. Når du treffer noe som er bunnstoff for sitt eget felt — en primitiv — si det («regn som grunnfjell for denne siden») og legg en `[[wikilenke]]` nedover heller enn å lage en sirkulær analogi.

### Bøtte 3 — Prosa og setningsnivå
- **Lesbart språk.** Aktiv stemme; sett punktum heller enn å kjede setninger sammen; subjekt tidlig og bindeord mellom setningene; bryt opp innfløkte leddsetninger; avsnitt sjelden over ti linjer.
- **De sju anti-mønstrene** — den negative siden av denne bøtta. Se «Naturlig norsk — sju anti-mønstre» rett under.

### Bøtte 4 — Innhold, kilde og holdbarhet
- **Attribusjon og balanse.** Ingen implisitte verdidommer. Attribuer omstridte påstander («X hevder», «ifølge Y»). Gjør det eksplisitt når dokumentasjonen mangler.
- **Sitater peker til kilder, ikke til `raw/`.** Source-sidene er eneste sannhetspunkt for hva en kilde sier.
- **Skriv så det varer.** Ingen datostempling («nylig», «det siste året»); bruk konkrete årstall, og alltid et årstall for tall som endrer seg.
- **Media-logg-lagene.** Lest/sett er erfaringsdata (kan bære påstander); vil-lese/watchlist er mulighetsdata (bare som intensjon eller kandidat); leser-nå er foreløpig.

### Kort sjekkliste (ved skrivepunktet)
Kondensert form — én linje per bøtte — som ingest og redaktør peker til:
> **Struktur:** definer i første setning · viktigst først, stigende vanskelighet · én side, ett tema · lenk inline. **Klarhet:** stranger-test · definer fagord én gang. **Prosa:** aktivt, hele setninger · ingen anti-mønstre. **Innhold:** attribuer · ingen datostempling · sitater peker til kilder, ikke raw.

## Naturlig norsk — sju anti-patterns
Wiki-bodyen skal kjennes som norsk skrevet av en norsk skribent. Sju mønstre å unngå:
- *Feil preposisjon om språk.* Man skriver *på* et språk, ikke *i*. Tilsvarende *snakke på*, *oversette til/fra*, *publisere i (avis) / på (nettsted)*.
- *Hengende preposisjoner i engelsk mønster.* "Landsmålet Vinje skrev i" → "landsmålet som Vinje skrev på". Bruk "som" + preposisjon eller omformuler.
- *Agent-/prosess-nominaliseringer av latinske verb.* Verbet ("kodifisere") er fint norsk; substantivet ("kodifikator", "kodifisering") klinger jus-/byråkrat-akademisk. Bytt til verbform der det går. Test: "Jeg driver sjeldent med biologisering selv om jeg er biolog."
- *Telegram-bullets.* Komma-separerte fragment-tags og nominaliserings-sandwicher uten verb leser som hastverk. Bullets skal være hele setninger med verb; lengden styres av innholdet, ikke av at det skal "være kort".
- *AI-rhetoriske vendinger.* Kontrastiv negasjon ("det er X, ikke Y, som ...", "ikke bare X, men også Y") og signalfraser ("det er verdt å merke seg", "viktig her er at", "sentralt er") er retorisk staffasje. Bruk motsetning bare når den faktisk gjør semantisk arbeid.
- *Umerket anglisme.* Engelske leksemer (substantiv, verb, faste uttrykk) sklir uomformulert inn i norsk syntaks: "Status: live", "outgrows itself", "fails silently", "vanity-dashboard". Test: ville ordet trengt kursivering for å føles korrekt i en redigert norsk tekst? Hvis ja, omformuler (ofte med norsk verb, ikke 1:1-substantivbytte). Unntak: navngitte vault-primitiver og deres norske bøyninger (`source`, `entity`, `concept`, `synthesis`, `wikilink`, `infobox`, `ingest`/`ingestes`/`ingestet`/`re-ingestes`/`re-ingestet`, `lint`, `schema`, `trigge`/`trigges`/`trigget`).
- *Effektiv prosa, men hele setninger.* Konsisjon skal komme av å kutte staffasje — dekorative ord, gjentakelser, fyll — ikke av å amputere setningen. Mønsteret rammer også grammatisk komplette setninger: en tynn kopula-stump som bare slår fast et tall eller en kjensgjerning («Kravene er sju.») der leseren trenger en setning som *fører dem inn* i stoffet. Test: gjør setningen mer enn å avlevere et faktum — bærer den leseren videre til det neste? En kort setning er riktig når innholdet er kort, og feil når den er kappet for å «virke effektiv». (Søsken til *Telegram-bullets*: samme rot — konsist er ikke det samme som amputert — men her i prosa og også for verb-komplette stumper.)
