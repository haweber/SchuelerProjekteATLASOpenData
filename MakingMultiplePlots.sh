if [[ $# -eq 0 ]] ; then
    echo "You did not provide an argument, please provide H, W, or Z as argument"
    #exit 1
elif [[ $1 == "H" ]]; then
    #HPfad
    echo "Hello H"
    python3 MakePlot.py -hn "hmllllnarrow" -ht "Vier-Leptonen-Masse" -xt "m\${}_{4l}\$ [GeV/c\${}^2\$]" -yt "Events / 5 GeV" -sp -r
    python3 MakePlot.py -hn "hmllllnarrow" -ht "Vier-Leptonen-Masse" -xt "m\${}_{4l}\$ [GeV/c\${}^2\$]" -yt "Events / 5 GeV" -sp 
    python3 MakePlot.py -hn "hmllll" -ht "Vier-Leptonen-Masse" -xt "m\${}_{4l}\$ [GeV/c\${}^2\$]" -yt "Events" -sp
    python3 MakePlot.py -hn "hmllll" -ht "Vier-Leptonen-Masse" -xt "m\${}_{4l}\$ [GeV/c\${}^2\$]" -yt "Events" -sp -r
elif [[ $1 == "W" ]]; then
    #WPfad
    echo "Hello W"
    python3 MakePlot.py -hn "hmTnarrow" -ht "Transversale-Masse" -xt "m\${}_{T}\$ [GeV/c\${}^2\$]" -yt "Events / 1 GeV" -sp -r
    python3 MakePlot.py -hn "hmTnarrow" -ht "Transversale-Masse" -xt "m\${}_{T}\$ [GeV/c\${}^2\$]" -yt "Events / 1 GeV" -sp -ly
    python3 MakePlot.py -hn "hmT" -ht "Transversale-Masse" -xt "m\${}_{T}\$ [GeV/c\${}^2\$]" -yt "Events" -sp -ly -r
    python3 MakePlot.py -hn "hmT" -ht "Transversale-Masse" -xt "m\${}_{T}\$ [GeV/c\${}^2\$]" -yt "Events" -sp -ly
    # python3 MakePlot.py -hn "hmTfull" -ht "Transversale-Masse" -xt "m\${}_{T}\$ [GeV/c\${}^2\$]" -yt "Events" -sp -ly -r
    # python3 MakePlot.py -hn "hmTfull" -ht "Transversale-Masse" -xt "m\${}_{T}\$ [GeV/c\${}^2\$]" -yt "Events" -sp -ly
elif [[ $1 == "Z" ]]; then
    #ZPfad
    echo "Hello Z"
    python3 MakePlot.py -hn "hmllnarrow" -ht "Zwei-Leptonen-Masse" -xt "m\${}_{ll}\$ [GeV/c\${}^2\$]" -yt "Events / 1 GeV" -sp -r
    python3 MakePlot.py -hn "hmllnarrow" -ht "Zwei-Leptonen-Masse" -xt "m\${}_{ll}\$ [GeV/c\${}^2\$]" -yt "Events / 1 GeV" -sp -ly
    python3 MakePlot.py -hn "hmll" -ht "Zwei-Leptonen-Masse" -xt "m\${}_{ll}\$ [GeV/c\${}^2\$]" -yt "Events" -sp -ly
    python3 MakePlot.py -hn "hmll" -ht "Zwei-Leptonen-Masse" -xt "m\${}_{ll}\$ [GeV/c\${}^2\$]" -yt "Events" -sp -ly -r
else
    echo "You need to provide argument H, W, or Z"
fi
