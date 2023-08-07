if [[ $# -eq 0 ]] ; then
    echo "You did not provide an argument, please provide H, W, or Z as argument"
    #exit 1
elif [[ $1 == "H" ]]; then
    #HPfad
    echo "Hello H"
elif [[ $1 == "W" ]]; then
    #WPfad
    echo "Hello W"
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
