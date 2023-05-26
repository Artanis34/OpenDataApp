# Visualisierung Barrierefreies Reisen Dok
## Beschreibung
Visualisierung der Daten aller Haltestellen und Haltekanten der Schweizer Transportunternehmen, die vom BAV aufgefordert sind, die Zugänglichkeit zu erfassen.

| Daten der Punkte | Beschreibung |
| - |- |
| Name | Offizielle Bezeichnung einer Dienststelle welche von sämtlichen Abnehmern übernommen werden muss. |
| Ortschaft* | Ortschaft in welcher die Dienststelle liegt. |
| Status | Status über den Erfassungsstand der Dienststelle |
| Kanton* | Name des Kantons in welcher die Dienststelle liegt. |
| Dienststellen-ID | Nummer einer Dienststelle (Haltestelle) welche für die Schweiz von DiDok vergeben wird. Sie ist Teil des eineindeutigen Schlüssels für Dienststellen. |
| Service | Abkürzung der verantwortlichen Geschäftsorganisation. |

*leer , falls keine Daten vorhanden.

---

## Nutzen
Diese Website soll hauptsächlich dem BAV dienen, um den Transportunternehmen konkrete Direktionen zu geben, welche Stellen und Kanten noch erfasst oder vervollständigt werden müssen.

Schlussendlich kann die Seite verwendet werden um die der Stellen und Kanten der Schweiz (und näherer Umgebung) auf einem Blick zu haben.

---

## Anwendung
Die Seite funktioniert mit einfachen zoomen des Nutzers. Die Punkte werden zu Beginn geladen und positioniert und werden je nach Zoom-Level geclustert angezeigt. Zoomt man zu seinem gewünschten Punkt nahe genug, sind die Informationen der einzelnen Punkte 
einfach ablesbar, wenn man mit der Maus drauf klickt.

---
* Filter:
    - Service (Transportunternehmen)
    - Status (Erfassungsstand)
        - 0 : Daten nicht vollständig
        - 1 : Daten vollständig
        - 9 : keine Daten
* Wenn mehrer Punkte auf demselben Ort sind kann man mit einem Mausklick das Cluster aufspalten und dort die einzelnen Punkte, dann anklicken.
* Wenn für ein Punkt keine GeoDaten hinterlegt sind, werden diese statdessen auf der rechten Seite unter den Filtern angezeigt.
---

## Daten
Die Daten sind OpenData und werden per API wöchentlich aktualisiert... **TO DO**

---

## Über diese App
Diese App wurde im Rahmen der Bachelorvorlesung Durchführung eines Open Data Projekts der Forschungsstelle Digitale Nachhaltigkeit an der Universität Bern programmiert.

Für die Programmierung der App wurde [Pandas](https://pandas.pydata.org),.... **TO DO**

Der Source-Code ist auf [Github](https://github.com/Artanis34/OpenDataApp) frei zugänglich.

**Christian Gafner**  
Student BSc Computer Science, Universität Bern  
[Mail](mailto:christian.gafner@students.unibe.ch)

**Julien Chopin**  
Student BSc Computer Science, Universität Bern  
[Mail](mailto:julien.chopin@students.unibe.ch)  