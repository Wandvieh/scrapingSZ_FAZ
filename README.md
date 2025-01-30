# scrapingSZ_FAZ
Eine GUI zum Scrapen der SZ und FAZ und berechnen der Worthäufigkeiten. Das Skript wurde 2023 als Hausarbeit erstellt und ist auf den damaligen Aufbau der Seite angepasst. In der Zwischenzeit wurden die Websites der beiden Zeitungen überarbeitet, wodurch der Download nicht mehr funktioniert. Die GUI, die mit tkinter erstellt wurde, funktioniert weiterhin.

Mittels dem Interface habe ich alle Artikel zwischen dem 24.02. (Angriff Russlands auf die Ukraine) und März 2023 der SZ und der FAZ heruntergeladen. Dann habe ich die Worthäufigkeiten der 20 häufigsten Wörter in einer Term-Dokument-Matrix festgehalten und visualisiert.

Die hier nicht dargestellten svg-Dateien in images/ wurden mit anderen Daten zum Testen erstellt.

## Erstellung der Daten im Interface

![Datenerstellung im GUI](https://github.com/Wandvieh/scrapingSZ_FAZ/blob/main/images/GUI_Datenerstellung.jpg?raw=true)

![Datenanalyse im GUI](https://github.com/Wandvieh/scrapingSZ_FAZ/blob/main/images/GUI_Datenanalyse.jpg?raw=true)


## Ergebnisse

![Barchart: 20 häufigste Wörter nach Wörtern](https://github.com/user-attachments/assets/3fa20e69-c662-4a4c-9752-53d6326c4a51)

![Barchart: 20 häufigste Wörter nach Zeitungen](https://github.com/user-attachments/assets/90a51bfa-254d-4071-8e77-a6b0b5ec9346)


## Reflektion

Obwohl das Programm zum Erstellungszeitpunkt gut funktioniert hat, ist es mit einem neuen Design der Websiten hinfällig geworden. Der Aufwand, das Programm dauerhaft funtionieren zu lassen, ist höher, je öfter die Website umgestellt wird.

Die Charts sind nicht ordentlich benannt, so dass heute nicht mehr klar ist, welche Bedeutung die Y-Achse hat und ob die Skalierung der verschiedenen Bars dieselbe ist.
