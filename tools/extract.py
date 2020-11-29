#https://gist.github.com/sirex/b5fdf0228cf03f5b9076b5975c5591a5

from pandas.io.json import json_normalize
from SPARQLWrapper import SPARQLWrapper, JSON

def select(query, service='https://query.wikidata.org/sparql'):
    sparql = SPARQLWrapper(service)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return json_normalize(result['results']['bindings'])

query_string = """
SELECT DISTINCT ?business ?businessLabel ?officialname ?employees ?origindate ?profit ?assets ?equity ?markcap
(GROUP_CONCAT(DISTINCT ?industryLabel; SEPARATOR = ", ") AS ?industries)
(GROUP_CONCAT(DISTINCT ?ceoLabel; SEPARATOR = ", ") AS ?ceos)
(GROUP_CONCAT(DISTINCT ?chairLabel; SEPARATOR = ", ") AS ?chairs)
(GROUP_CONCAT(DISTINCT ?hqLabel; SEPARATOR = ", ") AS ?hqs)
(GROUP_CONCAT(DISTINCT ?groupLabel; SEPARATOR = ", ") AS ?groups)
WHERE {
  VALUES ?socialmediatypes {
    wdt:P2013
    wdt:P4264
    wdt:P2002
  }
  ?business (wdt:P31/(wdt:P279*)) wd:Q4830453;
    wdt:P17 wd:%s; #rotate this for each country
    ?socialmediatypes ?socialmedia.
  OPTIONAL { ?business wdt:P1128 ?employees. }
  OPTIONAL { ?business wdt:P1448 ?officialname. }
  OPTIONAL { ?business wdt:P571 ?origindate. }
  OPTIONAL { ?business wdt:P2295 ?profit. }
  OPTIONAL { ?business wdt:P452 ?industry. }
  OPTIONAL { ?business wdt:P2295 ?profit. }
  OPTIONAL { ?business wdt:P2403 ?assets. }
  OPTIONAL { ?business wdt:P2137 ?equity. }
  OPTIONAL { ?business wdt:P2226 ?markcap. }
  OPTIONAL { ?business wdt:P159 ?hq. }
  OPTIONAL { ?business (p:P169/ps:P169) ?ceo. }
  OPTIONAL { ?business wdt:P488 ?chair. }
  OPTIONAL { ?business wdt:P361 ?group. }
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en".
    ?business rdfs:label ?businessLabel.
    ?industry rdfs:label ?industryLabel.
    ?ceo rdfs:label ?ceoLabel.
    ?chair rdfs:label ?chairLabel.
    ?hq rdfs:label ?hqLabel.
    ?group rdfs:label ?groupLabel.
  }
}
GROUP BY ?business ?businessLabel ?officialname ?shortname ?employees ?origindate ?profit ?assets ?equity ?markcap
""" % "Q36"


data = select(query_string)
data.to_csv('test.csv')
print(data.head(10))
