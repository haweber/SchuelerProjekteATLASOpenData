# Analyse von W-Bosonen

In dieser Übung geht es darum, W-Bosonen in der Daten von Proton-Proton-Kollisionen zu finden und die Daten auszuwerten. Wie du schon in der Masterclass gelesen hast (https://atlas.physicsmasterclasses.org/de/wpath_lhcphysics2.htm), sind W-Bosonen keine stabile Teilchen und zerfallen praktisch instantan. Ein möglicher Zerfall, der eine einfache Rekonstruktion zulässt, ist der in ein geladene und ein neutrales Lepton, wie zum Beispiel in ein Muon/Neutrino- oder Elektron/Neutrino-Paar. 

Deswegen werden wir das 1-Lepton Datenset der ATLAS Open Data betrachten.
Wenn du auf die Open Data Webseite gehst, siehst du, dass dies 58GB an Daten sind.
http://opendata.atlas.cern/release/2020/documentation/datasets/files.html
Wenn du einzelne Dateien herunterladen möchtest, könnten wir mit etwas weniger (46GB) arbeiten.

Die Dateien, die wir brauche:
- Alle Daten: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/Data/
- Simulation von dem Signal, W-Zerfälle in Elektron/Neutrino-Paar: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_361103.Wminusenu.1lep.root
- Simulation von dem Signal, W-Zerfälle in Positron/Neutrino-Paar: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_361100.Wplusenu.1lep.root
- Simulation von dem Signal, W-Zerfälle in Muon/Neutrino-Paar: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_361104.Wminusmunu.1lep.root
- Simulation von dem Signal, W-Zerfälle in Antimuon/Neutrino-Paar: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_361101.Wplusmunu.1lep.root
- Simulation von dem Signal, W-Zerfälle in Tau/Neutrino-Paar: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_361105.Wminustaunu.1lep.root
- Simulation von dem Signal, W-Zerfälle in Antitau/Neutrino-Paar: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_361102.Wplustaunu.1lep.root
- Simulation von einem Untergrundprozess, der Z-Zerfällen in Elektron/Positron-Paare: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_361106.Zee.1lep.root
- Simulation von einem Untergrundprozess, der Z-Zerfällen in Muon/Antimuon-Paare: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_361106.Zee.1lep.root
- Simulation von einem Untergrundprozess, der Z-Zerfällen in Tau/Antitau-Paare: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_361108.Ztautau.1lep.root
- Simulation von einem Untergrundprozess, der Top/Antitop-Paar-Produktion: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_410000.ttbar_lep.1lep.root
- Simulation von einem Untergrundprozess, der W-Boson-Paar-Produktion: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mc_363492.llvv.1lep.root
- Simulation von einem Untergrundprozess, der W-Boson-Paar-Produktion: https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/1lep/MC/mv_363493.lvvv.1lep.root
(Um die Liste kompakt zu halten, schreibe ich hier nicht weiter Simulationen auf)

Um diese Daten auszuwerten, brauchen wir ein Programm, dass es lesen kann. Wie in der Einführung beschrieben, ist dieses Programm für uns ROOT. Da das für dich eventuell fremd ist, gibt es hier zwei Macros (eines für die direkte Verwendung von ROOT, welches auf C++ basiert; das andere verwendet Python).
Das Python Skript ist ErsteSchritte.py: Dies ist sehr langsam. Du kannst es mit folgendem Befehl ausführen (falls ROOT vorhanden ist): `python ErsteSchritte.py`
Besser ist: runAll.C / ScanEvents.C: Das Haupt-Macro mit dem Programm ist ScanEvents.C. Dieses wird über runAll.C aufgerufen (wenn ROOT vorhanden ist): `root -l -b -q runAll.C`

Die Ideen zu diesem Praktikum wurden bereits beschrieben:
1.) Zuerst wirst du versuchen, W-Bosonen zu rekonstruieren.

2.) Dann wirst du versuchen, die Masse des W-Bosons zu bestimmen. Je nach Erfahrung kann dies unter Betrachtung des Physik-Untergrund geschehen oder nicht, und mithilfe eines kinematischen Fits oder nicht.

3.) Wenn Deine Zeit es zulässt, werden wir danach zusätzliche Fragestellungen erörtern. Dies kann zum Beispiel sein:

- Messe die Anzahl von positiv und negativ geladenen W-Bosonen. Was findest Du? Macht das Ergebnis Sinn?
- Messe die Anzahl von W-Bosonen-Zerfälle mit Muonen/Antimuonen und Elektronen/Positronen. Gibt es hier einen Unterschied. Ist dieser zu erwarten.
- Messe die Kinematik der W-Bosonen. Diese sind z.B. pT, eta, phi. Gibt es Unterschiede zur Theorie/Simulation?
    
Um den W-Pfad zu wählen, wirst du weiter zum Ordner WPfad gehen und dieses README weiterlesen.

Alles weitere besprichst du mit deinem Betreuer.
