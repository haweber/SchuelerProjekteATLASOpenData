import uproot
import numpy as np
#import pandas as pd
#import uproot3_methods #if you want to use lorentzvectors
import argparse
import os
#from scipy.optimize import curve_fit

### Diese Funktion wird immer aufgerufen
def main(args):

    ntupledir = os.path.join(args.inputdir,"")
    ### zuerst laden wir die Daten mit uproot
    ### bemerke, der code crashed, falls die drei Dateien nicht existieren
    fileData = uproot.open(ntupledir+"data_2lep.root")["events"]
    fileSignal = uproot.open(ntupledir+"simulation_signal_2lep.root")["events"]
    fileBackground = uproot.open(ntupledir+"simulation_background_2lep.root")["events"]
    ### Hier bearbeiten wir die Daten. Damit wir den Code nicht dreimal wiederholen muessen (ATLAS-Daten, Sim,ulation von Z-Teilchen und Simulation von anderen Prozessen die Elektronen-Positron / Muon-Antimuon-Paare erzeigen)
    processEvents(fileData,      True, False,args)
    processEvents(fileSignal,    False,True, args)
    processEvents(fileBackground,False,False,args)

    ### Das ist das Ende dieser Funktion






### Diese Funktion verwenden wir, um Daten und Simulationen zu analysieren.
def processEvents(inputfile, isdata, issignal, args):
    ### Das brauchen wir spaeter - wo speichern wir unsere Resultate ab.    
    outdir = os.path.join(args.savedir,"")
    ### Stelle sicher, dass das Verzeichnis, in welche wir die Daten speichern wollen, existiert. Falls nicht, wird es erzeugt.
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    appendname = ""
    if isdata:
        appendname = "_Data.npz"
    elif issignal:
        appendname = "_Signal.npz"   
    else:
        appendname = "_Background.npz"

        
    ### zuerst laden wir die Daten in sogenannte numpy-Arrays
    arrays = inputfile.arrays()
    ### die Arrays sind hier beschrieben:
    """
    arrays["lep1_px"] # x-Komponente des Impulses des ersten Leptons, -999 falls Ereignisse keine Leptonen hat
    arrays["lep1_py"] # y-Komponente des Impulses des ersten Leptons, -999 falls Ereignisse keine Leptonen hat
    arrays["lep1_pz"] # z-Komponente des Impulses des ersten Leptons, -999 falls Ereignisse keine Leptonen hat
    arrays["lep1_E"]  # Energie des ersten Leptons, -999 falls Ereignisse keine Leptonen hat
    arrays["lep1_id"] # Lepton-ID (siehe unten) des ersten Leptons, -999 falls Ereignisse keine Leptonen hat
    arrays["lep2_px"] # x-Komponente des Impulses des zweiten Leptons, -999 falls Ereignisse nur ein Lepton hat
    arrays["lep2_py"] # y-Komponente des Impulses des zweiten Leptons, -999 falls Ereignisse nur ein Lepton hat
    arrays["lep2_pz"] # z-Komponente des Impulses des zweiten Leptons, -999 falls Ereignisse nur ein Lepton hat
    arrays["lep2_E"]  # Energie des zweiten Leptons, -999 falls Ereignisse nur ein Lepton hat
    arrays["lep2_id"] # Lepton-ID (siehe unten) des zweiten Leptons, -999 falls Ereignisse nur ein Lepton hat
    arrays["lep3_px"] # x-Komponente des Impulses des dritten Leptons, -999 falls Ereignisse nur zwei Leptonen hat
    arrays["lep3_py"] # y-Komponente des Impulses des dritten Leptons, -999 falls Ereignisse nur zwei Leptonen hat
    arrays["lep3_pz"] # z-Komponente des Impulses des dritten Leptons, -999 falls Ereignisse nur zwei Leptonen hat
    arrays["lep3_E"]  # Energie des dritten Leptons, -999 falls Ereignisse nur zwei Leptonen hat
    arrays["lep3_id"] # Lepton-ID (siehe unten) des dritten Leptons, -999 falls Ereignisse nur zwei Leptonen hat
    arrays["lep4_px"] # x-Komponente des Impulses des vierten Leptons, -999 falls Ereignisse nur drei Leptonen hat
    arrays["lep4_py"] # y-Komponente des Impulses des vierten Leptons, -999 falls Ereignisse nur drei Leptonen hat
    arrays["lep4_pz"] # z-Komponente des Impulses des vierten Leptons, -999 falls Ereignisse nur drei Leptonen hat
    arrays["lep4_E"]  # Energie des vierten Leptons, -999 falls Ereignisse nur drei Leptonen hat
    arrays["lep4_id"] # Lepton-ID (siehe unten) des vierten Leptons, -999 falls Ereignisse nur drei Leptonen hat
    arrays["met_px"]  # x-Komponente des transversalen fehlenden Impulses (Mass fuer Neutrino-Impuls)
    arrays["met_py"]  # y-Komponente des transversalen fehlenden Impulses (Mass fuer Neutrino-Impuls)
    arrays["weight"]  # Da man ja beliebig viele Simulationsereignisse produzieren kann, muss man diese Gewichten, damit sie der zu analysierenden Datenmenge entspricht. Dies macht man mit dieser Variable
    ### Kommentar zu lepton-ID: Identifikation, ob das Lepton ein Elektron (id == 11), Positron (id == -11), Muon (id == 13) oder Anti-Muon (id == -13) ist
    ### Kommentar zu met: Bei Proton-Proton-Kollisionen kann man kein met_pz abschaetzen, da Protonen keine fundamentalen Teilchen sind.
    """
    ### nun erstellen wir Masken:
    ### Ereignis muss genau zwei Leptonen haben
    twolep_mask = ((arrays['lep1_E' ] >= 0) & (arrays['lep2_E' ] >= 0) & (arrays['lep3_E'] < 0))
    ### Die zwei Leptonen muessen vom gleichen Typ sein (same flavor), aber auch ihre Antiteilchen (opposite sign), d.h. entweder 11*-11 == -121 oder 13*-13 == -169
    SFOS_mask = ((arrays['lep1_id']*arrays['lep2_id']==-121) | (arrays['lep1_id']*arrays['lep2_id']==-169))
    filters = np.invert(twolep_mask & SFOS_mask)
    #erzeuge gefilterte Objekte - fuer das Z-Boson interessieren uns nur Lepton 1, 2 und der weights-array, wir koennen aber auch met mitnehmen
    lep1_px = np.delete(arrays['lep1_px'],filters)
    lep1_py = np.delete(arrays['lep1_py'],filters)
    lep1_pz = np.delete(arrays['lep1_pz'],filters)
    lep1_E  = np.delete(arrays['lep1_E' ],filters)
    lep1_id = np.delete(arrays['lep1_id'],filters)
    lep2_px = np.delete(arrays['lep2_px'],filters)
    lep2_py = np.delete(arrays['lep2_py'],filters)
    lep2_pz = np.delete(arrays['lep2_pz'],filters)
    lep2_E  = np.delete(arrays['lep2_E' ],filters)
    lep2_id = np.delete(arrays['lep2_id'],filters)
    met_px = np.delete(arrays['met_px'],filters)
    met_py = np.delete(arrays['met_py'],filters)
    weight = np.delete(arrays['weight'],filters)

    #nun produzieren wir arrays fuer das Z boson
    Z_E  = lep1_E  + lep2_E
    Z_px = lep1_px + lep2_px
    Z_py = lep1_py + lep2_py
    Z_pz = lep1_pz + lep2_pz

    ### this is the mass-squared for Z-bosons: (mc^2)^2 = (lep1_E + lep2_E)^2 - [ ((lep1_px+lep2_px)c)^2 + ((lep1_py+lep2_py)c)^2 + ((lep1_pz+lep2_pz)c)^2 ]
    Z_mass_squared = (Z_E**2 - (Z_px**2 + Z_py**2 + Z_pz**2))
    ### Redefiniere Filter:
    filters = Z_mass_squared < 0 # es gibt pathologische Faelle, bei der diese Groesse negativ wird. Falls das passiert, koennen wir nicht die Wurzel ziehen.

    ### Filtere die pathologischen Faelle
    lep1_px = np.delete(lep1_px,filters)
    lep1_py = np.delete(lep1_py,filters)
    lep1_pz = np.delete(lep1_pz,filters)
    lep1_E  = np.delete(lep1_E ,filters)
    lep1_id = np.delete(lep1_id,filters)
    lep2_px = np.delete(lep2_px,filters)
    lep2_py = np.delete(lep2_py,filters)
    lep2_pz = np.delete(lep2_pz,filters)
    lep2_E  = np.delete(lep2_E ,filters)
    lep2_id = np.delete(lep2_id,filters)
    met_px = np.delete(met_px,filters)
    met_py = np.delete(met_py,filters)
    weight = np.delete(weight,filters)
    Z_E  = np.delete(Z_E ,filters)
    Z_px = np.delete(Z_px,filters)
    Z_py = np.delete(Z_py,filters)
    Z_pz = np.delete(Z_pz,filters)
    Z_mass_squared = np.delete(Z_mass_squared,filters)

    ### Jetzt koennen wir auch die Z-Masse bestimmen
    Z_m = Z_mass_squared**0.5 # Wurzel ziehen geht entweder ueber math.sqrt oder so wie hier, da fuer eine Variable 'a' gilt: sqrt(a) = a^0.5 (und ^ wird mit ** in python ausgedrueckt)
    print(Z_m,len(Z_m),type(Z_m))
    ### Nun sind wir soweit, dass wir einen Array mit allen Massen haben, die von Elektronen-Positronen- oder Muon-Antimuon-Paaren kommen und daher von Z-Bosonen kommen. Speichern wir diese Masse als Histogramme ab.
    ### Zuerst speichern wir alle Massen ab - das Histogram unterteilen wir in 100 Abschnitte
    ### hmll enthaelt die Summe fuer jeden Abschnitt, bins die unteren Grenzwert eines jeden Abschnitts
    hmll, mllbins = np.histogram(Z_m,100,weights=weight)
    ### Falls wir es brauchen sollten, finden wir noch die statistische Unsicherheit:
    hmll_unc = np.sqrt(np.histogram(Z_m, bins=mllbins, weights = weight**2)[0])

    ###Machen wir das selbe, aber nur fuer eine geringere Massenauswahl zwischen 40 - 140 GeV/c^2
    hmllnarrow, narrowmllbins = np.histogram(Z_m,100,range=(40.,141.),weights=weight) #bemerke dass die obere Range 140 + einmal die Abschnittsbreite ist
    hmllnarrow_unc = np.sqrt(np.histogram(Z_m, bins=narrowmllbins, weights = weight**2)[0])

    ### Nun speichern wir diese Werte komprimiert ab:
    ### Diese Numpy-Funktion speichert die Werte des Histogramms, den statistischen Filter und die Abschnitt-Grenzen in einer komprimierten Textdatei ab. Alternativ kannst du die savetxt fuer die unkomprimierte Text-Datei verwenden.
    np.savez_compressed(outdir+'hmll'+appendname,histo=hmll, uncertainty=hmll_unc, binning=mllbins)
    np.savez_compressed(outdir+'hmllnarrow'+appendname,histo=hmllnarrow, uncertainty=hmllnarrow_unc, binning=narrowmllbins)

    ### Das ist das Ende dieser Funktion. Sie laeuft jetzt drei mal fuer Daten, Signalsimulation und Untergrundsimulation
    
    
"""
H = np.loadtxt('hmll_wide')
plt.plot(H[1], H[0], drawstyle='steps-pre')
plt.show()
"""
"""
H = np.load('hmll_wide.npz')
hep.histplot(H['histo'], H['binning'])
#print(H.files)
#plt.plot(H['histo'], H['binning'][:-1], drawstyle='steps-pre')
#plt.show()


fig1, ax1 = plt.subplots()
ax1.hist(mass, bins=100, histtype="step")
ax1.set_xlabel(r"$Z_{mass}$ [GeV]")
ax1.set_title("Z Mass spectrum")
plt.show()

fig2, ax2 = plt.subplots()
ax2.hist(mass, bins=100, histtype="step", range=(0., 180.))
ax2.set_xlabel(r"$Z_{mass}$ [GeV]")
ax2.set_title("Z Mass spectrum")
plt.show()
"""


if __name__ == "__main__":

    # Define options
    ### Der Parser erlaubt Inputs beim Aufrufen der Funktion zu verwenden, z.B.
    ### 'python3 AnalyzeData_ZPath.py --process -sv "LieblingsVerzeichnis/"
    parser = argparse.ArgumentParser(description="Inputs for student projects")
    parser.add_argument('-in', '--inputdir', dest='inputdir', help='Directory with the input rootfiles'        , type=str, required=False, default='MakeFlatTrees/OutputTrees/')
    parser.add_argument('-sd', '--savedir', dest='savedir', help='Directory where to store the histogram files', type=str, required=False, default='HistogramData/')

    
    # Argument parser is set up
    args = parser.parse_args()

    # run Main function
    main(args)
