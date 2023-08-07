# Analyse von Higgs-Bosonen

In dieser Übung geht es darum, Higgs-Bosonen in der Daten von Proton-Proton-Kollisionen zu finden und die Daten auszuwerten. Wie du schon in der Masterclass gelesen hast (https://atlas.physicsmasterclasses.org/de/zpath_hboson.htm), sind Higgs-Bosonen keine stabile Teilchen und zerfallen praktisch instantan. Ein möglicher Zerfall, der eine einfache Rekonstruktion zulässt, ist der in zwei Z-Bosonen, und dann der Zerfall dieser in geladene Leptonen, besonders in ein Muon/Antimuon- oder Elektron/Positron-Paar. 

Deswegen werden wir das 4-Leptonen Datenset der ATLAS Open Data betrachten.
Wenn du auf die Open Data Webseite gehst, siehst du, dass dies 427MG an Daten sind.
http://opendata.atlas.cern/release/2020/documentation/datasets/files.html
Wenn du einzelne Dateien herunterladen möchtest, könnten wir mit ungefähr 290MB arbeiten.

Die Dateien, die wir brauche:
- Alle Daten: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/Data/
- Simulation von Higgs-Produktion im Gluon-Gluon-Fusionskanal: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_345060.ggH125_ZZ4lep.4lep.root
- Simulation von Higgs-Produktion im Vektorboson-Fusionskanal: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_344235.VBFH125_ZZ4lep.4lep.root
- Simulation von Higgs-Produktion im Assozierten Z-Produktionskanal: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_341947.ZH125_ZZ4lep.4lep.root
- Simulation von Higgs-Produktion im Assozierten W-Produktionskanal: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_341964.WH125_ZZ4lep.4lep.root
- Simulation von einem Untergrundprozess von Z-Zerfällen in Elektron/Positron-Paare: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_361106.Zee.4lep.root
- Simulation von einem Untergrundprozess von Z-Zerfällen in Muon/Antimuon-Paare: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_361106.Zee.4lep.root
- Simulation von einem Untergrundprozess von Z-Zerfällen in Tau/Antitau-Paare: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_361108.Ztautau.4lep.root
- Simulation von einem Untergrundprozess, der WZ-Bosonen-Paar-Produktion: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363491.lllv.4lep.root
- Simulation von einem Untergrundprozess, der ZZ-Bosonen-Paar-Produktion: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root

Um diese Daten auszuwerten, brauchen wir ein Programm, dass es lesen kann. Wie in der Einführung beschrieben, ist dieses Programm für uns ROOT. Da das für dich eventuell fremd ist, gibt es hier zwei Macros (eines für die direkte Verwendung von ROOT, welches auf C++ basiert; das andere verwendet Python).
Das Python Skript ist ErsteSchritte.py: Dies ist sehr langsam. Du kannst es mit folgendem Befehl ausführen (falls ROOT vorhanden ist): `python ErsteSchritte.py`
Besser ist: runAll.C / ScanEvents.C: Das Haupt-Macro mit dem Programm ist ScanEvents.C. Dieses wird über runAll.C aufgerufen (wenn ROOT vorhanden ist): `root -l -b -q runAll.C`

n.b. - während beide Wege funktionieren sollten, wurde nur das C-Macro getestet.

Die Ideen zu diesem Praktikum wurden bereits beschrieben:
1.) Zuerst wirst du versuchen, Higgs-Bosonen zu rekonstruieren. Hier gibt es den Vier-Leptonen und den Zwei-Photonen Pfad. Wir betrachten hier den Vier-Leptonen Pfad

2.) Kannst Du die Masse des Higgs Boson bestimmen. Hier ist es wichtig, den Untergrund zu kennen.

3.) Wenn Deine Zeit es zulässt, werden wir danach zusätzliche Fragestellungen erörtern. Dies kann zum Beispiel sein:

- Messe die Anzahl von Higgs-Bosonen-Zerfälle mit Muonen/Antimuonen und Elektronen/Positronen. Wir haben drei Möglichkeiten. Ein Muon-Antimuon-Paar plus ein Elektron-Positron-Paar, oder zwei Muon-Antimuon-Paare oder zwei Eletron-Positron-Paare. Gibt es Unterschiede und sind diese zu erwarten.

- Messe die Kinematik der Higgs-Bosonen. Diese sind z.B. pT, eta, phi. Gibt es Unterschiede zur Theorie/Simulation?

Alles weitere besprichst du mit deinem Betreuer.
