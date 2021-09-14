#!../venv/Scripts/python.exe

import os, sys, pickle, os.path
from pathlib import Path
from datetime import datetime

strProblemPath = "D:\\Dropbox (Sandipan.com)\\Development\\Site Builder\\Mobirise\\experiment03-sandipan.com"

lstFiles = os.listdir(strProblemPath)

print("Files found in directory: [%s]" % lstFiles)

for strFile in lstFiles:

    if "conflicted copy" in strFile:

        lstFilePieces = strFile.split("(")
        strFileExt = strFile.split(".")[1]
        lstFileOriginal = lstFilePieces[0].strip()
        strOrigFile = lstFileOriginal + "." + strFileExt
        objOrigFile = Path(strOrigFile)
        print("File: [%s] v/s [%s]" % (strFile, strOrigFile))

        if strOrigFile in lstFiles:

            print("File [%s] should be replaced by file [%s]" % (strFile, strOrigFile))

            strDecision = input("Replace (Y/N) [N]")

            if strDecision.lower() == "y":

                if True:
                    os.rename(os.path.join(strProblemPath, strOrigFile), os.path.join(strProblemPath, strOrigFile) + ".bak")
                    os.rename(os.path.join(strProblemPath, strFile), os.path.join(strProblemPath, strOrigFile))
                    print("Swapped")
                else:
                    print("Failed")
                    continue

