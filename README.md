# SchuelerProjekteATLASOpenData
Dies ist eine Liste von einigen Projekten für Schüler mit ATLAS Open Data / This is a list of projects for high school students using ATLAS Open Data.

## Einführung zur Teilchenphysik

In diesem Praktikum haben wir ein circa 20-minütige Einleitungsvideo erstellt, welches die Teilchenphysik im Bezug zur Arbeit mit Z-Bosonen einführt. Das Video findest du hier: https://youtu.be/G7fJ9sJ5moM.

Weiterführend kannst du dann Fragen im direkten Gespräch mit Deinem Betreuer diskutieren.

Eine gute textliche und ausführliche Einführung ist auch im Internet unter weltmaschine.de zu finden:
Über die Physik, die wir am LHC mit dem ATLAS Experiment durchführen: https://www.weltmaschine.de/physik/
Schaue Dir besonders das Standardmodell und das Higgs an - diese Seiten diskutieren unseren aktuellen Wissenstand.
Weiterhin kannst Du unter LHC und Experimente am LHC über die Experimente lernen, mit denen wir die Teilchenphysik studieren:
https://www.weltmaschine.de/cern_und_lhc/lhc/

Eine weitere kurze Zusammenfassung ist dieser CERN-Flyer:
https://www.weltmaschine.de/sites/sites_custom/site_weltmaschine/content/e36736/e42241/e42246/e42251/LHC-Guide_CERN-Brochure-2009-003-Ger.pdf


## Einführung zur Datenanalyse - Event Displays

Das Ziel Deines Schülerprojektes wird es sein, systematisch die Daten des ATLAS Experimentes zu analysieren. Um einen Einblick zu geben, wie dies (weniger systematisch aber mit grafischer Hilfe) funktioniert, verwenden wir Daten und Software des Masterclasses Programm.

Dazu gehe zum Link: https://atlas.physicsmasterclasses.org/de/index.htm
Es gibt zwei Analyse-Wege, die Du auswählen kannst, den W-Pfad, oder den Z-Pfad.
Dies sind zwei so genannte Kraftträgerteilchen, die die elektroschwache Kraft übertragen. Diese Kraft ist für zum Beispiel die Kernspaltung in Kernkraftwerken oder die Kernfusion innerhalb der Sonne verantwortlich.
Der Z-Pfad wird einfacher in der Ausführung sein, aber je nach dem Projekt an dem Du arbeiten wirst, kann der W-Pfad lehrreicher sein. Sprich mit Deinem Betreuer, welcher Pfad besser für Dich ist.

Zur Datenanalyse mit dem Programm HYPATIA haben wir ein weiteres Video erstellt, dieses findest Du hier: https://youtu.be/e2Qr5Pi2BMU. \
Dieses Video ist 10 Minuten lang und gibt Dir eine Anleitung, wie Du mit HYPATIA Daten auswertest.

### ZPfad
Wenn Du zum Punkt "An die Arbeit!" kommst, wirst Du gebeten, dass Event Display HYPATIA herunterzuladen. Wenn Du Deinen eigenen Laptop mitbringst, solltest Du dies tun, ansonsten spreche mit Deinem Betreuer, da das Programm sich eventuell schon auf dem Instituts-PC befindet.
HYPATHIA ist ein java Programm, dass betriebsunabhängig auf deinem PC laufen sollte.
Lade zunächst ein beliebiges Datenpaket herunter, wenn Du möchtest auch mehrere. Ein Datenpaket ist ungefähr 30MB groß.
Öffne nun das Programm Hypatia_7.4_Masterclass.jar und lade ein Datenpaket hoch. Diskutiere mit deinem Betreuer, wie man die Daten bewertet und was Du auswerten sollst. Du wirst einige Ereignisse bewerten müssen, möglicherweise mit mehreren Datenpaketen, um ein Resultat zu erhalten.

### WPfad

Der W-Pfad verwendet eine ältere Software: https://atlas-minerva.web.cern.ch/index.php?lang=de
Frage Deinen Betreuer für Die Daten.

## Deine Datenanalyse - große Datenmengen

### Einrichten

#### Software

Natürlich können wir die Daten mit Billionen von Ereignissen nicht mit dieser Methode analysieren, sondern müssen dies systematischer machen.
Unsere Analyse-Tool in der Hochenergiephysik/Teilchenphysik ist ROOT.

Um nicht die ganze Software herunterzuladen, verwenden wir Python mit uproot und anderen Modulen.
Dazu musst du:
- für Windows: Im Microsoft store Python (3) herunterladen
- Linux/MacOS: Python sollte nativ bereits installiert sein. 
- alternativ, lade Python herunter: https://www.python.org/downloads/
Für alle Fälle: überprüfe, dass du Python3 hast (Befehl: `python --version`)

Dann öffne ein Terminal (oder Shell/Powershell): Der Befehl `python` oder `py` sollte funktionieren, ansonsten diskutiere mit deinem Betreuer.

Um Module in python zu laden, brauchst du pip. Dies erhälst du über folgenden Befehl:
- Windows: `py -m ensurepip --upgrade`
- Linux/MacOS: `python -m ensurepip --upgrade` (manchmal brauchst du `python3 -m ensurepip --upgrade`
- alternativ: Siehe hier: https://pip.pypa.io/en/stable/installation/

Sobald du pip hast, kannst du Module laden:\
```python -m pip install argparse```\
```python -m pip install numpy```\
```python -m pip install matplotlib```\
```python -m pip install uproot```\
```python -m pip install uproot3_methods```\
Optional (zum Erstellen von Fits):\
```python -m pip install scipy```


Etwas, was gut wäre, ist einen Code-Editor zu verwenden.
Ein paar Vorschläge:
- Linux: emacs / kate / Visual Studio / sublime / gedit
- MacOS: XCode / sublime / Visual Studio / aquamacs
- Windows: sublime / Visual Studio / notepad++

#### Daten


Die Daten werden dir entweder über einen Link bereitgestellt, oder frage deinen Betreuer, dir diese zu erstellen. Deine Daten werden aus den ATLAS Open Data mithilfe des Programms in MakeFlatTrees erstellt. Sie sind ein stark vereinfachtes Format, welches nur die nötigsten Variablen enthält und alles andere herausstreicht.

Die so hergestellten Daten sollen sich im Verzeichnis MakeFlatTrees/OutputTrees befinden.

Je nach deinem Projekt wirst Du ein bestimmte Anzahl dieser ROOT tuples (oft auch ntuples genannt) herunterladen. Dies können einige GB (50 MB bis 6 GB) an Daten sein.

### Dein Projekt

Wir haben drei Grundprojekte, welche W-, Z- oder Higgs-Bosonen analysieren. Je nachdem, wie schnell Du in Deinem Fortschritt bist, werden wir nach dem jeweiligen Grundprojekt weitere Fragestellungen an das Projekt hinzufügen. Es gibt nämlich viele Fragen, woran wir Wissenschafter forschen.

Du kannst diesen zu deinem Laptop herunterladen, indem du entweder den Code als ZIP-Datei herunterlädst. Oder besser noch es von git herunterlädst, z.B. durch ein Terminal-Command: `git clone https://github.com/haweber/SchuelerProjekteATLASOpenData.git`
Natürlich muss dein Laptop git verstehen.

Die Projekte unterscheiden sich als WPfad, ZPfad, HPfad.
In allen Projekten gibt es ein Basis-Code, welche eine der grundlegenden Variablen ausgibt: AnalyzeData_XXXPath.py.
Es gibt aber auch eine Datei, die Pfad-unabhängig ist. Wenn du zum Beispiel beim Z-Pfad selbst versuchen möchtest, dass Z-Boson zu bestimmen und dessen Masse zu extrahieren, musst du diese Datei nehmen. Sie hat immer noch ein Beispiel zur Datenanalyse. Verwende dazu `AnalyzeData_Example.py`

Für den ZPfad ist es `AnalyzeData_ZPath.py`. Du kannst das Programm wie folgt durchführen:
```python AnalyzeData_ZPath.py```
(vielleicht musst du `python3` anstatt `python` schreiben)
Du kannst den Ort der Atlas-Daten mit `-in` angeben, und den Ort, wo du deine analysierten Daten speichern möchtest, kannst du mit `-sd` speichern, also z.B.
```python AnalyzeData_ZPath.py -in OrtDerAtlasDaten -sd MeinLieblingsverzeichnis```

Das Skript speichert im Augenblick die Masse der zwei Leptonen, welche aus einem Z entstanden sein können, als ein sogenanntes Histogramm ab. Schaue die Kommentare im Code an, um zu sehen, wie das gemacht wird.

Analog gibt es ```AnalyzeData_WPath.py```. Hier ist das Beispielhistogramm die transversale Masse von Lepton und Neutrino.

Schließlich gibt es noch das Skript ```AnalyzeData_HPath.py```. Das Beispiel hier ist die Masse aus vier Leptonen, welche aus einem Higgs Boson entsanden sein könnten.


Deine Aufgabe ist es, den Code zu erweitern und neue Information aus den Daten zu erhalten.

Mögliche Fragestellungen:
- Wie oft findet man Elektronen oder Muonen im Zerfall.
- Bei W-Bosonen: Was ist die Ladung dieser Bosonen?
- Bei H-Bosonen: Gibt es Unterschiede zwischen den beiden Lepton-Paaren?
- Was sind die kinematische Eigenschaften, Impuls, Energie, Flugrichtung?
- Kannst du die Masse aus einem Fit exakt extrahieren.
- Verstehst du, wie man Untergrund-Ereignisse und Signalereignisse unterscheiden kann?
- ...



### Figuren und Tabellen

Ein Teil, deine Ergebnisse zu dokumentieren, ist wichtig, Grafiken (oder Tabellen zu erzeugen). Du hast dazu das Skript ```Makeplot.py``` zur Verfügung, welches Grafiken für dich erzeugt. Für Tabellen gibt es kein vorgefertigtes Skript.
Schaue auch hier die Kommentare an, um das Skript zu verstehen. Hier hast du viele Möglichkeiten, Argumente an das Programm zu geben. Die wichtigsten sind:

- `hn`: Der Name des Histogramms, das du zeichnen möchtest (ist zwingend zu geben). Braucht einen string.
- `ly`: Zeichnet die y-Achse nicht linear, sondern logarithmisch (Abschnitte sind, 1, 10, 100, 1000, usw.). 
- `r`: Zeichnet neben der Hauptfigur auch das Verhältnis von Daten zur Simulation.
- `ht`: Titel für das Histogramm. Braucht einen string.
- `xt`: Beschriftet, was die x-Achse zeigt. Braucht einen string.
- `yt`: Beschriftet, was die y-Achse zeigt. Braucht einen string.
- `sp`: Zeigt dir den Plot direkt an.
- `ns`: Speichere den Plot **nicht** als Bilddatei ab.

Also kannst du z.B. so etwas schreiben:
```python MakePlot.py -hn "hmll"```\
Dies zeichnet einfach das Histogramm `hmll`.

Präziser wäre:\
```python MakePlot.py -hn "hmll" -ht "Zwei-Leptonen-Masse" -xt "m\${}_{ll}\$ [GeV/c\${}^2\$]" -yt "Events" -sp -ly -r```\
Hier erzeugst du das Verhältnis, die y-Achse ist logarithmisch, die Figur wird dir direkt angezeigt, und du beschriftest das Bild.

Um mehrere Figuren direkt zu zeichnen, kannst du dieses Programm verwenden:\
`source MakingMultiplePlots.sh $1`\
wobei `$1` entweder `H`, `W` oder `Z` sein muss, je nachdem welche Analyse du machst.

Viel Spaß!


## Rekonstruktion eines Ereignisses

Dieser Teil verlangt viel Eigeninitiative. Wir geben dir Hits (das heißt Treffer) im Detektor für ein einziges Ereignis, also die reine Detektormessungen. Deine Aufgabe ist es, die Impulse und Energie der dazugehörigen Spuren zu messen und damit die Z-Masse dieses einzelnen Ereignisses zu messen. Aus der Positionen der Hits und dem Wissen des Magnetfeldes im Detektor kann man den Impuls herleiten, etwas was in den vorhergehenden Teilen dieses Praktikum immer gegeben war. Um die Aufgabe einfach zu halten, geben wir dir nur die Messungen im inneren Spurendetektors. Dort herrscht ein konstantes Magnetfeld, welches in z-Richtung zeigt (also entlang der Protonenstrahlrichtung).
Wie der transversale Impuls, und damit der gesamte Impuls eines geladenen Teilchens mit der Messung im Detektor und dem Magnetfeld zusammenhängt, findest du zum Beispiel auf Seite 10 und 11 von https://indico.cern.ch/event/281572/contributions/1629104/attachments/517028/713352/Detektoren.pdf.
Falls du in der Schule noch nichts über Kräfte im Magnetfeld gehört hast, spreche mit deinem Betreuer.
Deine Aufgabe ist es also:

- Finde mithilfe der x- und y-Koordinaten der Hits eine Abschätzung der Sagitta s (auch Segmenthöhe genannt) und der Länge der Kreissehne L.
- Bestimme daraus den Radius der Teilchenspur und damit den Betrag des transversalen Impuls der Teilchen. 
- Mithilfe der Richtung im Detektor erhälst du automatisch die x- und y-Komponente der Impulse der Teilchen.
- Unter Berücksichtigung der z-Koordinaten der Hits kannst du auch die z-Komponente der Impulse bestimmen.
- Mit den Werten der Impulse, kannst du die Energie der Teilchen abschätzen (vergleiche Impuls mit der Masse von Elektronen oder Muonen).
    * Bemerke hier, dass man die Energie der Teilchen über diese Formel bestimmen kann: $(E)^2 = (mc^2)^2 + (p_x^2+p_y^2+p_z^2)c^2$.
- Wenn du die Energien hast, dann solltest du die Z-Massen-Messung für dieses eine Ereignis bestimmen können.
    * Die Z-Energie ist die Summe der Energien der beiden Zerfallsteilchen (Elektronen oder Muonen). Das gleiche gilt für jede Impulskomponente, die Summe der Impulskomponenten ist die Z-Impulskomponente. Mit der oberen Formel kann man somit die Z-Masse bestimmen.

Eine Liste der Hits kannst du wie folgt erhalten: 
Im gleichen Verzeichnis wie die AnalyzeData-Dateien existiert eine ATLAS_Detektor.py Datei. Du kannst etwas wie folgt im Terminal eingeben:\
``python ATLAS_Detektor.py -ef SingleEventHitData/ZeventXXX.txt -rh -ex -ph``\
wobei das `XXX` in `ZeventXXX.txt` ein Buchstabe zwischen `A` bis `O` ist. Es könnte sein, dass du `python3` schreiben musst.

Wenn due dieses Programm laufen lässt, passieren zwei Dinge. Erstens, werden die im Terminal die Hits von zwei Teilchenspuren angezeigt (alle Angaben sind in cm!). Zweitens öffnet sich ein neues Fenster, welches diese Hits auch visualisiert.

Du musst nun entweder mit Code, oder eventuell auch Blatt Papier und einem Stift die Rechnung durchführen, bis du die Z-Masse erhälst.
Neben der Z-Masse kannst du folgende Größen angeben: Impulse der Teilchen? Flugrichtung der Teilchen? Ladung der Teilchen?

Viel Spaß!

