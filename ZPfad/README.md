# Analyse von Z-Bosonen

In dieser Übung geht es darum, Z-Bosonen in der Daten von Proton-Proton-Kollisionen zu finden und die Daten auszuwerten. Wie du schon in der Masterclass gelesen hast (https://atlas.physicsmasterclasses.org/de/zpath_zboson.htm), sind Z-Bosonen keine stabile Teilchen und zerfallen praktisch instantan. Ein möglicher Zerfall, der eine einfache Rekonstruktion zulässt, ist der in geladene Leptonen, besonders in ein Muon/Antimuon- oder Elektron/Positron-Paar. 

Deswegen werden wir das 2-Leptonen Datenset der ATLAS Open Data betrachten.
Wenn du auf die Open Data Webseite gehst, siehst du, dass dies 24GB an Daten sind.
http://opendata.atlas.cern/release/2020/documentation/datasets/files.html
Wenn du einzelne Dateien herunterladen möchtest, könnten wir mit ungefähr der Hälfte (12GB) arbeiten.

Die Dateien, die wir brauche:
- Alle Daten: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/Data/
- Simulation von Z-Zerfällen in Elektron/Positron-Paare: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/MC/mc_361106.Zee.2lep.root
- Simulation von Z-Zerfällen in Muon/Antimuon-Paare: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/MC/mc_361106.Zee.2lep.root
- Simulation von Z-Zerfällen in Tau/Antitau-Paare: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/MC/mc_361108.Ztautau.2lep.root
- Simulation von einem Untergrundprozess, der Top/Antitop-Paar-Produktion: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/MC/mc_410000.ttbar_lep.2lep.root
- Simulation von einem Untergrundprozess, der W-Boson-Paar-Produktion: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/MC/mc_363492.llvv.2lep.root

Um diese Daten auszuwerten, brauchen wir ein Programm, dass es lesen kann. Wie in der Einführung beschrieben, ist dieses Programm für uns ROOT. Da das für dich eventuell fremd ist, gibt es hier zwei Macros (eines für die direkte Verwendung von ROOT, welches auf C++ basiert; das andere verwendet Python).
Das Python Skript ist ErsteSchritte.py: Dies ist sehr langsam. Du kannst es mit folgendem Befehl ausführen (falls ROOT vorhanden ist): `python ErsteSchritte.py`
Besser ist: runAll.C / ScanEvents.C: Das Haupt-Macro mit dem Programm ist ScanEvents.C. Dieses wird über runAll.C aufgerufen (wenn ROOT vorhanden ist): `root -l -b -q runAll.C`

Die Ideen zu diesem Praktikum wurden bereits beschrieben:
1.) Zuerst wirst du versuchen, Z-Bosonen zu rekonstruieren.

2.) Dann wirst du versuchen, die Masse des Z-Bosons zu bestimmen. Je nach Erfahrung kann dies unter Betrachtung des Physik-Untergrund geschehen oder nicht, und mithilfe eines kinematischen Fits oder nicht.

3.) Wenn Deine Zeit es zulässt, werden wir danach zusätzliche Fragestellungen erörtern. Dies kann zum Beispiel sein:

- Messe die Anzahl von Z-Bosonen-Zerfälle mit Muonen/Antimuonen und Elektronen/Positronen. Gibt es hier einen Unterschied. Ist dieser zu erwarten.
    
- Messe die Kinematik der Z-Bosonen. Diese sind z.B. pT, eta, phi. Gibt es Unterschiede zur Theorie/Simulation?

Alles weitere besprichst du mit deinem Betreuer.
