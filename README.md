# SOUlab

Snabblabb med SOU-data efter blogginlägg. Läs mer på http://www.christopherkullenberg.se/relationer-i-souniversum/

Har du labbat själv? Bidra gärna med kod/analyser här.

## Installera dependencies

```
pip install -r requirements.txt
```

## Experiment

Dessa utgår från att textfiler för SOU:er finns tillgängliga i katalogen
"data". Ladda hem [SOU-zipfil (ca 800 Mb)](http://scientometrics.flov.gu.se/files/SOUtxtDecadeFiles.zip) och packa upp i mappen "data".

### 1. Skapa grafdata för användning i Gephi

Mycket simpel strängmatchning av "SOU \d\d\d\d:..." i SOU-texterna för
att möjliggöra referensanalys. Bygg SOU-databas med build_db.py först (en SQLite-databas kommer skapas):

```
python build_db.py ./data
```

Läs ut relationerna mellan SOU:er:

```
python parsesou.py ./data
```

Bygg grafdata i gexf-format med gen_graph.py:

```
python gen_graph.py soudata.gexf
```

Den sista filen kan sedan användas i verktyget Gephi för visualisering.


### 2. Frekvensanalys

Givet att grunddata har byggts upp enligt ovan är det enkelt att
generera antalet SOU:er per år med:

```
python gen_count.py > frekvens.csv
```

### 3. Hitta platsnamn

Filen features.txt innehåller svenska ortnamn hämtade från geonames.org.
Verktyget grep har stöd för [strängmatchning med Aho-Corasick](http://en.wikipedia.org/wiki/Aho–Corasick_string_matching_algorithm). För att mappa SOU:er mot ortnamn som förekommer i dem kör:

```
grep -owf features.txt data/30tal/*.txt
```


