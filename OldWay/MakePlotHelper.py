from enum import Enum
import ROOT

class MyColor(Enum):
    kWhite  = 0
    kBlack  = 1
    kGray   = 920
    kRed    = 632
    kGreen  = 416
    kBlue   = 600
    kYellow = 400
    kMagenta= 616
    kCyan   = 432
    kOrange = 800
    kSpring = 820
    kTeal   = 840
    kAzure  = 860
    kViolet = 880
    kPink   = 900
    
def ColorTranslator(colorstring):
    if type(colorstring) == int:
        return colorstring
    if type(colorstring) != str:
        print("no string given, return 1 (kBlack)")
        return 1
    colorintbase = 0
    colorintappend = 0
    temp = colorstring.split('+')
    if len(temp)>2:
        print ("Did not recognize string, return 1 (kBlack)")
        return 1
    if len(temp)==2:
        colorintappend += int(temp[1])
    else:
        temp = colorstring.split('-')
        if len(temp)==2:
            colorintappend -= int(temp[1])
    color = temp[0]
    color.replace('ROOT.','')
    return int(MyColor[color ].value)+colorintappend
    #return int(ROOT.EColor[temp[0] ].value)+colorintappend

#bla = 'kGreen'
#print(ColorTranslator(bla))
