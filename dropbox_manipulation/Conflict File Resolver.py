#!../venv/Scripts/python.exe

import os, sys, pickle, os.path
from pathlib import Path
# from os import path
# from datetime import datetime

# TODO: Make this recursive and find other instances ...

strProblemPath = "D:\\Dropbox (Sandipan.com)\\Development\\Site Builder\\Mobirise\\experiment03-sandipan.com"
strProblemPath = "D:\\Dropbox (Sandipan.com)\\Development"
strProblemPath = "D:\\Dropbox (Sandipan.com)\\website-accounts"
strBackupFolderName = "back"
binAskForConfirm = True

def fnFixFilesInFolder(strFolderPath):

    lstFiles = os.listdir(strFolderPath)
    print("Files found in directory [%s]: [%s]" % (strFolderPath, lstFiles))

    for strFile in lstFiles:

        strFilePath = os.path.join(strFolderPath, strFile)

        if os.path.isdir(strFilePath):
            fnFixFilesInFolder(strFilePath)

        else:
            if "conflicted copy" in strFile:
                lstFilePieces = strFile.split("(")
                lstFileExt = strFile.split(".")
                if len(lstFileExt) > 1:
                    strFileExt = "." + lstFileExt[1]
                else:
                    strFileExt = ""
                lstFileOriginal = lstFilePieces[0].strip()
                strOrigFile = lstFileOriginal + strFileExt
                objOrigFile = Path(strOrigFile)
                print("File: [%s] v/s [%s]" % (strFile, strOrigFile))

                if strOrigFile in lstFiles:
                    print("File [%s] should be replaced by file [%s]" % (strFile, strOrigFile))

                    if binAskForConfirm:
                        strDecision = input("Replace (Y/N) [N]")
                    else:
                        strDecision = "y"

                    if strDecision.lower() == "x":
                        break

                    if strDecision.lower() == "y":
                        try:
                            os.replace(os.path.join(strFolderPath, strOrigFile), os.path.join(strBackupFolderPath, strOrigFile) + ".bak")
                            os.rename(os.path.join(strFolderPath, strFile), os.path.join(strFolderPath, strOrigFile))
                            print("Swapped")
                        except:
                            print("Failed")

strBackupFolderPath = os.path.join(strProblemPath, strBackupFolderName)
if not os.path.exists(strBackupFolderPath):
    os.mkdir(strBackupFolderPath)
fnFixFilesInFolder(strProblemPath)