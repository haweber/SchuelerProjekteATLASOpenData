# Erstellung der Daten

Die Daten für die Schülerprojekte werden über das Programm hier erstellt.
Da dieser Abschnitt ROOT braucht, lass dies über deinen Betreuer machen ... die Installation des ROOT-Softwarepakets hat bei früheren Internships die unterschiedlichsten technische Probleme aufgezeigt, deren Lösung zeitintensiv ist.

Die Idee des Programms hier ist es aus den ATLAS Open Data ein vereinfachtes und flaches Ntuple zu extrahieren, bei der einige Berechnungen bereits durchgeführt wurden.

Im Programm muss man eine Zeile anpassen

Das Programm läuft von selbst (wenn man ROOT installiert hat):
```root -l -b -q makeNTuples.C```
wobei man im code `nleps` zu `1`, `2`, oder `4` setzen muss. Diese Zahl gibt das Skimming der Leptonen an (1 Lepton für W-Bosonen, 2 Leptonen für Z-Bosonen und 4 Leptonen für H-Bosonen).