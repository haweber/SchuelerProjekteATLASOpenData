# SchuelerProjekteATLASOpenData
Dies ist eine Liste von einigen Projekten für Schüler mit ATLAS Open Data / This is a list of projects for high school students using ATLAS Open Data.

## Einführung zur Teilchenphysik

Dies geschieht außerhalb der GitHub Umgebung in dem direkten Gespräch mit Deinem Betreuer.

Eine gute Einführung im Internet ist weltmaschine.de:
Über die Physik, die wir am LHC mit dem ATLAS Experiment durchführen: https://www.weltmaschine.de/physik/
Schaue Dir besonders das Standardmodell und das Higgs an - diese Seiten diskutieren unseren aktuellen Wissenstand.
Weiterhin kannst Du unter LHC und Experimente am LHC über die Experimente lernen, mit denen wir die Teilchenphysik studieren:
https://www.weltmaschine.de/cern_und_lhc/lhc/

Eine weitere kurze Zusammenfassung ist dieser CERN-Flyer:
https://www.weltmaschine.de/sites/sites_custom/site_weltmaschine/content/e36736/e42241/e42246/e42251/LHC-Guide_CERN-Brochure-2009-003-Ger.pdf


## Einführung zur Datenanalyse

Das Ziel Deines Schülerprojektes wird es sein, systematisch die Daten des ATLAS Experimentes zu analysieren. Um einen Einblick zu geben, wie dies (weniger systematisch aber mit grafischer Hilfe) funktioniert, verwenden wir Daten und Software des Masterclasses Programm.

Dazu gehe zum Link: https://atlas.physicsmasterclasses.org/de/index.htm
Es gibt zwei Analyse-Wege, die Du auswählen kannst, den W-Pfad, oder den Z-Pfad.
Dies sind zwei so genannte Kraftträgerteilchen, die die elektroschwache Kraft übertragen. Diese Kraft ist für zum Beispiel die Kernspaltung in Kernkraftwerken oder die Kernfusion innerhalb der Sonne verantwortlich.
Der Z-Pfad wird einfacher in der Ausführung sein, aber je nach dem Projekt an dem Du arbeiten wirst, kann der W-Pfad lehrreicher sein. Sprich mit Deinem Betreuer, welcher Pfad besser für Dich ist.

Wenn Du zum Punkt "An die Arbeit!" kommst, wirst Du gebeten, dass Event Display HYPATIA herunterzuladen. Wenn Du Deinen eigenen Laptop mitbringst, solltest Du dies tun, ansonsten spreche mit Deinem Betreuer, da das Programm sich eventuell schon auf dem Instituts-PC befindet.
HYPATHIA ist ein java Programm, dass betriebsunabhängig auf deinem PC laufen sollte.
Lade zunächst ein beliebiges Datenpaket herunter, wenn Du möchtest auch mehrere. Ein Datenpaket ist ungefähr 30MB groß.
Öffne nun das Programm Hypatia_7.4_Masterclass.jar und lade ein Datenpaket hoch. Diskutiere mit deinem Betreuer, wie man die Daten bewertet und was Du auswerten sollst. Du wirst einige Ereignisse bewerten müssen, möglicherweise mit mehreren Datenpaketen, um ein Resultat zu erhalten.

### Alternative Einführung zur Datenanalyse

Sollte HYPATHIA für Dich nicht funktionieren, kannst Du das Alternativprogramm Minerva ausprobieren: https://atlas-minerva.web.cern.ch/index.php?lang=de
Frage Deinen Betreuer für Die Daten.

## Deine Datenanalyse

### Einrichten

Natürlich können wir die Daten mit Billionen von Ereignissen nicht mit dieser Methode analysieren, sondern müssen dies systematischer machen.
Unsere Analyse-Tool in der Hochenergiephysik/Teilchenphysik ist ROOT.
Gehe zum Beispiel zu diesem Release und installiere das richtige Package für Dein Betriebssystem: https://root.cern/releases/release-62400/
Wenn Du ein Instituts-PC verwendest, wird höchstwahrscheinlich schon eine Version von ROOT installiert sein:
- Arbeitest du auf dem DESY Cluster, lädst du ROOT mit diesem Befehl:
```source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.08.04/x86_64-centos7-gcc48-opt/root/bin/thisroot.sh
```

Je nachdem, wie Du die Daten analysieren willst, brauchst du eventuell noch weitere Installationen, zum Beispiel: Falls Du bereits weißt, wie man mit Python programmiert, möchtest Du eventuell ROOT mit Python verwenden. In jenem Fall, muss dein PC natürlich Python haben.

Unsere Analyse wird danach sogenannte ROOT tuples verwenden, dass Datenformat, dass wir in ATLAS verwenden.
Für dieses Projekt verwenden wir ein vereinfachtes ROOT tuple, welches die ATLAS Kollaboration für die allgemeine Öffentlichkeit zur Verfügung stellt. Physik-Objekte wie Elektronen, Muonen, Jets, oder ETmiss sind schon erstellt, die Daten sind schon gefiltert. Außerdem sind Simulationen vorhanden, die uns eine Vorhersage gibt, wie sie aus der Theorie bestimmte physikalische Verteilungen berechnet wurden.

Je nach deinem Projekt wirst Du ein bestimmte Anzahl dieser ROOT tuples (oft auch ntuples genannt) herunterladen. Dies werden einige GB an Daten sein.

Wir haben drei Grundprojekte, welche W-, Z- oder Higgs-Bosonen analysieren. Je nachdem, wie schnell Du in Deinem Fortschritt bist, werden wir nach dem jeweiligen Grundprojekt weitere Fragestellungen an das Projekt hinzufügen. Es gibt nämlich viele Fragen, woran wir Wissenschafter forschen.
Um die Projekte herunterzuladen, bitte schaue Sie dir hier an.
https://github.com/haweber/SchuelerProjekteATLASOpenData

Die Daten, mit denen wir arbeiten werden, sind die ATLAS Open Data:
http://opendata.atlas.cern/release/2020/documentation/datasets/intro.html .
Dies sind Daten des ATLAS Experiments, die mit Hilfe von Proton-Proton-Kollisionen am LHC aufgenommen wurden. Diese Daten sind für die Öffentlichkeit freigegeben. Die ATLAS-Kollaboration hat die Daten schon vorbereitet, so sind beispielsweise alle Objekte wie Elektronen oder Muon schon rekonstruiert.

Am Anfang wird das Daten-Format vielleicht nicht einfach zu verstehen sein, deswegen bespreche insbesondere den Bereich "Full list of branches and variables" mit deinem Betreuer.

Das Ziel deines Projekt wird es sein, einen Analysepfad selbstständig auszuarbeiten und Resultate zu präsentieren. Doch wir haben dir einen Anfangs-Code zur Hilfestellung geschrieben. 
Du kannst diesen zu deinem Laptop herunterladen, indem du entweder den Code als ZIP-Datei herunterlädst. Oder besser noch es von git herunterlädst, z.B. durch ein Terminal-Command: `git clone https://github.com/haweber/SchuelerProjekteATLASOpenData.git`
Natürlich muss dein Laptop git verstehen.
Wenn Du technisch und im Programmieren schon genügend Erfahrung hast, kannst Du auch eine Fork von den Repository machen, und Deinen eigenen Code in Deine Fork hochladen. Ein Github Account ist kostenlos! Allerdings solltest Du dann ein Zertifikat erzeugen und das Projekt wie folgt herunterladen (verwende dein `username`):
```git clone git@github.com:username/SchuelerProjekteATLASOpenData.git```

Hier folgt eine Beschreibung der Projekte:

### W-Pfad

1.) Zuerst wirst du versuchen, W-Bosonen zu rekonstruieren.

2.) Dann wirst du versuchen, die Masse des W-Bosons zu bestimmen. Je nach Erfahrung kann dies unter Betrachtung des Physik-Untergrund geschehen oder nicht, und mithilfe eines kinematischen Fits oder nicht.

3.) Wenn Deine Zeit es zulässt, werden wir danach zusätzliche Fragestellungen erörtern. Dies kann zum Beispiel sein:

- Messe die Anzahl von positiv und negativ geladenen W-Bosonen. Was findest Du? Macht das Ergebnis Sinn?
- Messe die Anzahl von W-Bosonen-Zerfälle mit Muonen/Antimuonen und Elektronen/Positronen. Gibt es hier einen Unterschied. Ist dieser zu erwarten.
- Messe die Kinematik der W-Bosonen. Diese sind z.B. pT, eta, phi. Gibt es Unterschiede zur Theorie/Simulation?
    
Um den W-Pfad zu wählen, wirst du weiter zum Ordner WPfad gehen und dieses README weiterlesen.

**TO DO:** Dieser Pfad wurde noch nicht erarbeitet.
    
### Z-Pfad
1.) Zuerst wirst du versuchen, Z-Bosonen zu rekonstruieren.

2.) Dann wirst du versuchen, die Masse des Z-Bosons zu bestimmen. Je nach Erfahrung kann dies unter Betrachtung des Physik-Untergrund geschehen oder nicht, und mithilfe eines kinematischen Fits oder nicht.

3.) Wenn Deine Zeit es zulässt, werden wir danach zusätzliche Fragestellungen erörtern. Dies kann zum Beispiel sein:

- Messe die Anzahl von Z-Bosonen-Zerfälle mit Muonen/Antimuonen und Elektronen/Positronen. Gibt es hier einen Unterschied. Ist dieser zu erwarten.
    
- Messe die Kinematik der Z-Bosonen. Diese sind z.B. pT, eta, phi. Gibt es Unterschiede zur Theorie/Simulation?

Um den Z-Pfad zu wählen, wirst du weiter zum Ordner WPfad gehen und dieses README weiterlesen.

    
### Higgs-Pfad
1.) Zuerst wirst du versuchen, Higgs-Bosonen zu rekonstruieren. Hier gibt es den Vier-Leptonen und den Zwei-Photonen Pfad. Wir betrachten hier den Vier-Leptonen Pfad

2.) Kannst Du die Masse des Higgs Boson bestimmen. Hier ist es wichtig, den Untergrund zu kennen.

3.) Wenn Deine Zeit es zulässt, werden wir danach zusätzliche Fragestellungen erörtern. Dies kann zum Beispiel sein:

- Messe die Anzahl von Higgs-Bosonen-Zerfälle mit Muonen/Antimuonen und Elektronen/Positronen. Wir haben drei Möglichkeiten. Ein Muon-Antimuon-Paar plus ein Elektron-Positron-Paar, oder zwei Muon-Antimuon-Paare oder zwei Eletron-Positron-Paare. Gibt es Unterschiede und sind diese zu erwarten.

- Messe die Kinematik der Higgs-Bosonen. Diese sind z.B. pT, eta, phi. Gibt es Unterschiede zur Theorie/Simulation?
    
Um den Higgs-Pfad zu wählen, wirst du weiter zum Ordner HPfad gehen und dieses README weiterlesen.

**TO DO:** Dieser Pfad wurde noch nicht erarbeitet.


## Dokumentation

### Figuren

Ein Teil, deine Ergebnisse zu dokumentieren, ist es Grafiken und Tabellen zu erzeugen. Während ich dir es überlasse, eine Tabelle zu erzeugen, habe ich für die Grafikerzeugung ein Skript geschrieben, welches für alle Pfade funktioniert.
Es gibt es als MakePlot.C, aber hier beschreibe ich, wie man die Python-Version benutzt.
Grundsätzlich solltest du nichts am Python-Skript zu verändern brauchen, allerdings kannst du ganz am Ende die Funktionen sehen. Du kannst das Skript wie in MakingMultiplePlots.sh per Kommandozeile erzeugen.
Mit `source MakingMultiplePlots.sh` erzeugst du die drei Default-Plots vom Z-Pfad, die durch den bereits vorhandenen Code schon erstellt werden. Achtung, du musst dabei den Pfad zu deinen Verzeichnissen ändern, z.B. wenn du den W-Pfad bearbeitest. Ich hoffe die Beschreibung ist selbsterklärend, ansonsten sprich mit deinem Betreuer.
Sowohl das py-Skript als auch C-Macro lesen die Histogramme auch über eine txt-Datei ein. Der Grund für diesen Aufbau ist es, dass z.B. im ZPfad du einmal Z->ee/Z->mumu getrennt und ein andermal zusammengefasst betrachten willst. In der txt-Datei, welche im Beispiel  verwendet wird (z.B. ZPfad/output/filelist_Zll.txt) gibt es erklärende Kommentarzeilen (die, die mit # beginnen), die auch dieses Format erklären.
