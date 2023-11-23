# Erstellung der Daten - Ntuples

Die Daten für die Schülerprojekte werden über das Programm hier erstellt.
Da dieser Abschnitt ROOT braucht, lass dies über deinen Betreuer machen ... die Installation des ROOT-Softwarepakets hat bei früheren Internships die unterschiedlichsten technische Probleme aufgezeigt, deren Lösung zeitintensiv ist.

Die Idee des Programms hier ist es aus den ATLAS Open Data ein vereinfachtes und flaches Ntuple zu extrahieren, bei der einige Berechnungen bereits durchgeführt wurden.

Im Programm muss man eine Zeile anpassen

Das Programm läuft von selbst (wenn man ROOT installiert hat):
```root -l -b -q makeNTuples.C```
wobei man im code `nleps` zu `1`, `2`, oder `4` setzen muss. Diese Zahl gibt das Skimming der Leptonen an (1 Lepton für W-Bosonen, 2 Leptonen für Z-Bosonen und 4 Leptonen für H-Bosonen).


# Erstellung - Einzelne Ereignisse

Um einzelne Ereignisse für die Schüler zu erzeugen, brauchst du entweder ein ROOT-Ereignis oder Hypatia-Ereignis. Wähle am besten eines aus, dessen Masse nahe bei der Z-Boson Masse ist.
Danach notiere die Impulsbeträge $p$ (wichtig das der gesamte Impuls und nicht nur der transversale Impuls verwendet wird), Winkel $\phi$ und $\theta$ (nicht die Pseudorapidität) und die Ladung $q$ (1 oder -1) der beiden Zerfallsteilchen. Mit dem Befehl
```python3 DataPreparator_ATLAS_Detector.py -ef dummy.txt -th -ex -iH p1,phi1,theta1,q1,p2,phi2,theta2,q2```
Das Dezimalzeichen ist hierfür der Punkt. Ein Beispiel ist hier:
```python3 DataPreparator_ATLAS_Detector.py -ef dummy.txt -th -ex -iH 72.16,1.774,0.818,1.,48.47,-1.348,0.905,-1.```

Leider ist der Code sehr rudimentär, insbesonders kann der Code nicht automatisch Treffer in Barrel und Endcap unterscheiden, sodass du möglicherweise den Code anpassen musst, die kommentierten Zeilen in `DataPreparator_ATLAS_Detector.py` sollten dir Aufschluss geben, was zu tun ist.
Kopiere die erhaltenen truthhits und recohits in eine Textdatei, die wie `dummy.txt` aussieht. Danach kannst du den Code nochmals ablaufen lassen (aber jetzt mit deiner neuen `txt`-Datei). Dann kannst du überprüfen, ob du die Hits korrekt hast. Sobald alles korrekt aussiehst, kannst du die Datei an die Schüler weitergeben. Prinzipiell sollten die Ereignisse in `SingleEventHitData/` ausreichen.

