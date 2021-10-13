#HPfad

#WPfad
python MakePlot.py --tag=WPfad --outdir=WPfad/output/plots --histname=hMT --filelist=WPfad/output/filelist_Wlnu.txt --yaxis_log -uf -of --ytitle="Events / 5 GeV" --xtitle="m_{T} [GeV]"
python MakePlot.py --tag=WPfad --outdir=WPfad/output/plots --histname=hLepPt --filelist=WPfad/output/filelist_Wlnu.txt --yaxis_log -uf -of --ytitle="Leptons / 10 GeV" --xtitle="lep-p_{T} [GeV]"
python MakePlot.py --tag=WPfad --outdir=WPfad/output/plots --histname=hNLeps --filelist=WPfad/output/filelist_Wlnu.txt --yaxis_log -uf -of --ytitle="Events / 1" --xtitle="n_{leptons}"
python MakePlot.py --tag=WPfad --outdir=WPfad/output/plots --histname=hETmiss --filelist=WPfad/output/filelist_Wlnu.txt --yaxis_log -uf -of --ytitle="Events / 10 GeV" --xtitle="E_{T}^{miss} [GeV]"

#ZPfad
python MakePlot.py --tag=ZPfad --outdir=ZPfad/output/plots --histname=hMll --filelist=ZPfad/output/filelist_Zll.txt --yaxis_log -uf -of --ytitle="Events / 5 GeV" --xtitle="m_{ll} [GeV]"
python MakePlot.py --tag=ZPfad --outdir=ZPfad/output/plots --histname=hLepPt --filelist=ZPfad/output/filelist_Zll.txt --yaxis_log -uf -of --ytitle="Leptons / 10 GeV" --xtitle="lep-p_{T} [GeV]"
python MakePlot.py --tag=ZPfad --outdir=ZPfad/output/plots --histname=hNLeps --filelist=ZPfad/output/filelist_Zll.txt --yaxis_log -uf -of --ytitle="Events / 1" --xtitle="n_{leptons}"
