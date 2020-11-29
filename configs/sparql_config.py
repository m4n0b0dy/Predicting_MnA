#general info
COUNTRIES = ['Q30','Q148','Q17','Q183','Q145','Q668','Q142','Q155','Q38','Q16','Q884','Q408','Q96','Q252','Q43','Q55','Q851','Q414','Q865','Q36','Q717','Q869','Q794','Q20','Q40','Q878','Q1033','Q801','Q258','Q27','Q35','Q334','Q833','Q928','Q739','Q843','Q298','Q33','Q902','Q79','Q881','Q45','Q419','Q664','Q796','Q218','Q262','Q846','Q232','Q1049','Q1028','Q736','Q25','Q214','Q854','Q115','Q786','Q774','Q114','Q842','Q836','Q858','Q800','Q219','Q77','Q224','Q924','Q822','Q1016','Q265','Q117','Q874','Q1008','Q948','Q810','Q750','Q974','Q398','Q1009','Q211','Q733','Q1036','Q953','Q792','Q837','Q783','Q424','Q754','Q691','Q889','Q805','Q954','Q963','Q819','Q1041','Q423','Q912','Q766','Q811','Q1027']

#entity info
ENTITY_QUERY_STRING = """
SELECT DISTINCT ?business ?businessLabel ?officialname ?employees ?origindate ?profit ?assets ?equity ?markcap ?country
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
		?socialmediatypes ?socialmedia;
		wdt:P17 ?country.
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
GROUP BY ?business ?businessLabel ?officialname ?employees ?origindate ?profit ?assets ?equity ?markcap ?country
"""
ENTITY_PATH = '../data/entities/{COUNTRY}.csv'

#edge info
EDGE_QUERY_STRING = """
SELECT DISTINCT ?company ?companyLabel ?owner ?ownerLabel ?acquiredate ?pointintime
WHERE {
  VALUES ?socialmediatypes {
    wdt:P2013
    wdt:P4264
    wdt:P2002
  }
  VALUES ?countries {
    wd:%s
  }
    VALUES ?propownership {
    p:P749
    p:P127
  }
  VALUES ?ownership {
    ps:P749
    ps:P127
  }
  ?company ?propownership ?ownStat;
    (wdt:P31/(wdt:P279*)) wd:Q4830453;
    ?socialmediatypes ?socialmediacompany.
  ?owner (wdt:P31/(wdt:P279*)) wd:Q4830453;
    wdt:P17 ?countries;
    ?socialmediatypes ?socialmediaowner.
  ?ownStat ?ownership ?owner.
  OPTIONAL { ?ownStat pq:P580 ?acquiredate. }
  OPTIONAL { ?ownStat pq:P582 ?enddate. }
  OPTIONAL { ?ownStat pq:P585 ?pointintime. }
  OPTIONAL { ?ownStat pq:P1107 ?proportion. }
  FILTER(((YEAR(?acquiredate)) > 1990 ) || (!(BOUND(?acquiredate))))
  FILTER(((YEAR(?pointintime)) > 1990 ) || (!(BOUND(?pointintime))))
  FILTER(!(BOUND(?enddate))) #must be unbound or nonexistent (current acq)
  FILTER((((?proportion > ".5"^^xsd:decimal) && (?proportion <= 1 )) || ((?proportion > 50 ) && (?proportion <= 100 ))) || (!(BOUND(?proportion))))
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 99999
"""
EDGE_PATH = '../data/edges/{COUNTRY}.csv'