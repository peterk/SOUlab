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

### 4. Deep learning med word2vec

Word2vec tar en corpus av text och omvandlar till ordvektorer. Med dessa
går det att göra andra typer av analyser, t.ex. avständ mellan ord mm.
Det borde gå att arbeta med SOU-korpusen i
[word2vec](https://docs.google.com/a/peterkrantz.se/file/d/0B7XkCwpI5KDYRWRnd1RzWXQ2TWc/edit)
för att kunna göra
andra typer av analyser även om OCR-underlaget troligtvis kommer skapa
en del problem. gen_word2vec.py tränar en modell med SOU-datat:

```
python gen_word2vec.py ./data/
```

Körtiden kan vara någon timme för att skapa informationen. När det är
klart utforskar man enklast datamängden från python på kommandoraden.
Starta en ny python-tolk och testa enligt nedan:

```python
import gensim

# ladda den genererade modellen
model = gensim.models.Word2Vec.load("gensim2.model")


model.most_similar(u"amatör")
# [(u'amatörteater', musikföreningar', 0.7612131834030151), (u'folkdans', 0.7437361478805542), (u'symfonisk', 0.7418662309646606), (u'allsång', 0.7417885661125183)] ...


model.doesnt_match("stat kommun landsting ambassad".split())
# ambassad


model.most_similar(positive=[u'integritet', u'lag'], topn=1)
# [(u'datalagen', 0.7018075585365295)]

```
