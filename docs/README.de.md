# Redesign Energiedashboard - Hackdays BE 2025

Readme in [Englisch](../README.md)

[Data Hackdays BE 2025](https://hack.data-hackdays-be.ch/project/54) [EKDP Plattform](https://www.ekdp.apps.be.ch)

Zur Info: Jeglicher Code, der erstmalig im Release [hackdays.2025.be](https://github.com/networkscientist/redesign-energy-dashboard/releases/tag/hackdays.2025.be) festgehalten wird, wurde von einem Team freiwilliger Hacker*innen erstellt. Diese arbeiteten während den Data Hackdays BE 2025 am Projekt. Dabei nutzten sie Open Government Data (OGD) sowie ihre privaten Computer. Ich habe keinen Code zu diesem ersten Release beigetragen, sondern lediglich einige Code-Zeilen entfernt, um die Privatsphäre der Teilnehmenden zu schützen. Wie auf der offiziellen Website der Data Hackdays BE 2025 vermerkt, wurde der Code bereits unter der Lizenz CC-BY 4.0 veröffentlicht. Dieses Repository habe ich erstellt, um den Team-Mitgliedern den einfach Zugang zu Ihrem Resultat zu ermöglichen.

Dies trifft auch auf die Daten zu, die für das Dashboard verwendet wurden. Alle verwendeten Datensätze wurden bereits als OGD auf [opendata.swiss](https://opendata.swiss) publiziert und dokumentiert (mit den zugehörigen Lizenbedingungen). Ich habe den Team-Mitgliedern zwar Hinweise gegeben, wie sie an die Daten gelangen, die Transformation in ein nützliches Format lag dann jedoch bei ihnen. Da Github keine File-Uploads > 25 MB erlaubt, habe ich einige Spalten aus dem GWR-Gebäude-Datensatz entfernt.

Eine Live-Demo des Resultats ist auf [streamlit cloud](https://redesign-energy-dashboard.streamlit.app/) abrufbar. Möglicherweise wird das Repository zukünftig weiter bearbeitet; das Erstprodukt der Hacker*innen wird jedoch weiter unter dem Tag [hackdays.2025.be](https://github.com/networkscientist/redesign-energy-dashboard/releases/tag/hackdays.2025.be) verfügbar bleiben.

Des Weiteren hat das Team ein zweites Dashboard mit Microsoft PowerBI erstellt. Hierzu bitte ich um ein wenig Geduld. Ich werde den Source Code anschauen und dann entscheiden, ob er in der Form hochgeladen oder in das Streamlit Dashboard integriert wird. Die Screenshot sind jedoch schon abgelegt.

## Bibliographie
Zur Transparenz werden die verwendeten Datenquellen im Folgenden gelistet. Das Abrufdatum ist jeweils der 17.05.2025.
* [Eidgenössisches Gebäude- und Wohnungsregister GWR](https://opendata.swiss/de/dataset/eidg-gebaude-und-wohnungsregister-energie-warmequelle-heizung)
	* [Dokumentation Datendownload](https://www.housing-stat.ch/de/madd/public.html)
	* [Dokumentation Attribute](https://www.housing-stat.ch/de/docs/index.html), escpecially the [Code List](https://www.housing-stat.ch/files/Codeliste_Publikation_20240411.xlsx)
* [Elektrizitätsproduktionsanlagen](https://opendata.swiss/de/dataset/elektrizitatsproduktionsanlagen)
	* [Dokumentation Datenmodell](https://www.bfe.admin.ch/bfe/de/home/versorgung/digitalisierung-und-geoinformation/geoinformation/geodaten/produktionsanlagen/elektrizitaetsproduktionsanlagen.html)
* [Minergiegebäude](https://opendata.swiss/de/dataset/anzahl-minergie-gebaude-in-gemeinden)
* [Realisiertes PV-Potenzial in Schweizer Gemeinden](https://opendata.swiss/de/dataset/energie-reporter)
	* [Dokumentation Methodik](https://energiereporter.energyapps.ch/methodology#heading-solarstrom)
* [Energie-Reporter](https://opendata.swiss/de/dataset/energie-reporter)
* [Gemeinden Kanton Bern](https://opendata.swiss/de/dataset/historisiertes-gemeindeverzeichnis-der-schweiz), oder direkt via [Excel-Tabelle mit aktuellem Gemeindestand.](https://www.agvchapp.bfs.admin.ch/de) -> `Gemeindestand.xlsx`