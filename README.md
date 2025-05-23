# Redesign Energiedashboard - Hackdays BE 2025

Readme in [German](docs/README.de.md)

[Data Hackdays BE 2025](https://hack.data-hackdays-be.ch/project/54) [EKDP Platform](https://www.ekdp.apps.be.ch)

Please note: All of the code that will be released into the first release `hackdays.2025.be` has been written by the team of hacking volunteers. They worked on the project during the Data Hackdays BE 2025, using open government data (OGD) and their private computers. I did not write any of the code in that release, but merely removed a few lines that included personal information to protect their privacy. As stated on the hackdays website, the code has already been published under the CC-BY 4.0 Licence. I created this repo so team members can easily get the code.

The same is true for the data used in the dashboard. All of it has already been published as OGD and been documented on opendata.swiss, along with the respective licences. While I provided the team with directions where they could find these OGD, it was left to them to transform it into a useful format. Since Github does not allow file uploads larger than 25 MB, I kicked out some unnecessary columns from the GWR building registry file.

For a live demo of the result, check out [streamlit cloud](https://redesign-energy-dashboard.streamlit.app/). Perhaps, there will be development on the repo in the future. The initial contribution by the hackers, however, will still be available under the tag `hackdays.2025.be`.

Furthermore, the team developed a second dashboard, using Microsoft PowerBI. Bear with me; I will go through the respective source code, too, and then upload it or integrate it into the streamlit code.

## References
For transparency, each source the team used is listed below. The date of access is 17.05.2025.
* [Federal Building Registry GWR](https://opendata.swiss/de/dataset/eidg-gebaude-und-wohnungsregister-energie-warmequelle-heizung)
	* [Docs Data Access](https://www.housing-stat.ch/de/madd/public.html)
	* [Docs Attributes](https://www.housing-stat.ch/de/docs/index.html), escpecially the [Code List](https://www.housing-stat.ch/files/Codeliste_Publikation_20240411.xlsx)
* [Electricity Production Plants](https://opendata.swiss/de/dataset/elektrizitatsproduktionsanlagen)
	* [Docs Data Model](https://www.bfe.admin.ch/bfe/de/home/versorgung/digitalisierung-und-geoinformation/geoinformation/geodaten/produktionsanlagen/elektrizitaetsproduktionsanlagen.html)
* [Minergie Buildings](https://opendata.swiss/de/dataset/anzahl-minergie-gebaude-in-gemeinden)
* [Realised PV Potential in Municipalities](https://opendata.swiss/de/dataset/energie-reporter)
	* [Docs Methodics](https://energiereporter.energyapps.ch/methodology#heading-solarstrom)
* [Energy Reporter](https://opendata.swiss/de/dataset/energie-reporter)
* [Municipalities Canton Bern](https://opendata.swiss/de/dataset/historisiertes-gemeindeverzeichnis-der-schweiz), or directly via [Excel Table With Current Municipalities](https://www.agvchapp.bfs.admin.ch/de) -> `Gemeindestand.xlsx`