KottiFlow ist ein Grüne-Welle-Assistent für Fahrräder. Das Ziel ist eine Unterstützung der Fahrradfahrer durch Anzeigen der Ampelphase, damit das Fahrtempo vom Fahrradfahrer angepasst werden kann.

In der folgenden Karte kann man sehen, wo die Ampeln installiert werden.
<img width="737" alt="KottiFlow" src="https://user-images.githubusercontent.com/107621070/174057782-e810d8c9-3013-4d28-882b-a8c0e18f9d2b.png">

Dieses Dokument dient primär der technischen Dokumentation.

##  Komponenten
Die für dieses Projekt benötigte Hardwarekomponenten werden hier aufgelistet:
* 3x Raspberry Pi 3
* 3x LED Matrizen
* 3x Adruino-Board

<img width="561" alt="Screenshot 2022-06-20 at 10 18 53" src="https://user-images.githubusercontent.com/107621070/174557306-728b0939-9bce-4b13-a20e-831957320059.png">
<iframe width="100%" height="300px" frameborder="0" allowfullscreen src="//umap.openstreetmap.fr/de/map/kottiflow_783062?scaleControl=false&miniMap=false&scrollWheelZoom=false&zoomControl=true&allowEdit=false&moreControl=true&searchControl=null&tilelayersControl=null&embedControl=null&datalayersControl=true&onLoadPanel=undefined&captionBar=false"></iframe><p><a href="//umap.openstreetmap.fr/de/map/kottiflow_783062">Vollbildanzeige</a></p>

KottiFlow

RSU (Road Side Unit)

Für den Prototyp haben wir mit einem Gerät von Swarco gearbeitet. Die RSU wird in der Regel für die "Vehicle-to-everything" Kommunikation eingesetzt. Zum Beispiel kann damit die Ampelphase an (dafür ausgerüstete) Autos übertragen werden. Für das Projekt KottiFlow verwenden wir 2 RSU Geräte. Einen Sender mit Kabelverbindung zum Ampelsteuergerät und einen Empfänger am KottiFlow. Eine RSU kann mit einem LAN-Kabel betrieben werden, da diese per Power-over-Ethernet (PoE) mit Strom versorgt wird.

Ampelsteuergerät

Dem Steuergerät der Ampel wurde ein spezielles Prognose-Modul (Software) hinzugefügt, welches per [MQTT](https://de.wikipedia.org/wiki/MQTT) die Ampelphasen an die Sender RSU übermittelt. Diese Software muss vom Ampelhersteller implementiert werden.

Fahrrad-Ampel

An der Ampel selbst ist keinerlei Änderung nötig. Diese wird weiterhin vom Ampelsteuergerät geregelt. KottiFlow hat keinen Rückkanal und dient nur der Visualisierung der Schaltzeiten dieser Ampel.






Field Guide

In diesem Dokument finden sich hilfreiche Tipps für den Umgang mit Problemen im Live-Betrieb.

WiFi Zugriff am Gerät

KottiFlow verbindet sich zu einem vordefiniertem Wartungs-Netzwerk. Dieses kann man z.B. per Handy Hotspot oder geteilter Verbindung vom Laptop erstellen. Nutzt man die richtigen Zugangsdaten (SSID und Passwort) sollte sich KottiFlow nach einer kurzen Zeit automatisch verbinden. Es ist der bCyber SSH "Wartungskey" hinterlegt.

KottiFlow Service

Der Python Code läuft als system.d Service und kann mit den folgenden Befehlen gesteuert werden:

KottiFlow stoppen: sudo service kottiflow stop
KottiFlow starten: sudo service kottiflow start
KottiFlow neustarten: sudo service kottiflow restart
KottiFlow Status: sudo service kottiflow status

Außerdem kann die Ausgabe vom Log mit: journalctl -u kottiflow angezeigt werden. Mit journalctl -u kottiflow -f bleibt die Ausgabe offen und streamt alle neuen Logs.

KottiFlow Zeitplan

Mit dem Programm at kann man KottiFlow Zeitgesteuert an und ausschalten. Das Vorgehen dabei ist wie folgt:

Als Root User (sudo su)
at -M 12:00 30.06.2021 eingeben. Der Flag -M verhindert, dass bei der Ausführung versucht wird eine E-Mail zu senden! Also benutzen!

Dann bekommt man eine Eingabeaufforderung, erkennbar an dem at> im Promt. Hier kann nun der Befehl, z.B. service KottiFlow stop, eingegeben werden, diesen mit Enter bestätigen und dann mit Strg + d den Prompt beenden. Danach erscheint eine Bestätigung wie job JOBNUMMER JOBDATUM als Bestätigung, dass der Befehl geklappt hat.

Mit atq kann man sich eingerichtete Jobs anschauen.

Mit at -c JOBNUMMER kann man sich den genauen Inhalt des Jobs anschauen. Der Befehl ist in einem Script gewrappt. Also nicht von der langen Ausgabe beirren lassen 😉

Mit at -d JOBNUMMER kann man einen Job löschen.

Weitere Informationen findet man auch in der at Dokumentation: https://linux.die.net/man/1/at

Netzwerk Zugriff im Steuergerät-Kasten

Das Netzwerk im Steuergerät hat eine direkte Verbindung in das städtische Netzwerk. Man könnte somit z.B. aus Versehen auf andere Geräte zugreifen. Eine einfache Möglichkeit das zu verhindern ist es, den Laptop nicht in den vorhanden Switch einzustecken, sondern das vorhandene Kabel zwischen Switch und PoE-Injector abzustecken und mit einem RJ45 zu RJ45 Adapter zu arbeiten. So, dass man physikalisch nur eine Verbindung zum PoE-Injector und der Sender-RSU hat.

Kein Empfang

Ein Problem (z.B. nach einem Stromausfall) kann sein, dass die rsu.conf-Datei auf dem Empfänger "zurückgesetzt" wurde.

Projektpartner:

[<img width="70" height="70" alt="Screenshot 2022-06-16 at 13 30 30" src="https://user-images.githubusercontent.com/107621070/174060790-d9e71d79-9389-4c0c-9272-6a89a32dda01.png">](https://www.fixmycity.de) [<img width="70" height="70" alt="Screenshot 2022-06-16 at 13 23 11" src="https://user-images.githubusercontent.com/107621070/174059941-b43acfea-c277-42dd-ae67-764d6a949d9a.png">](https://radbahn.berlin/de) [<img width="120" height="70" alt="Screenshot 2022-06-16 at 13 27 14" src="https://user-images.githubusercontent.com/107621070/174060289-97034880-98d3-45f0-a3d2-32935a4fa7de.png">](https://www.bht-berlin.de) [<img width="90" height="70" alt="Screenshot 2022-06-16 at 13 31 59" src="https://user-images.githubusercontent.com/107621070/174060993-bcc7e749-0de9-486d-b3cb-b15c1ab6a82e.png">](https://www.bvg.de/de)

