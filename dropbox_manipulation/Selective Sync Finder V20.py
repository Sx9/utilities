# SELECTIVE SYNC FINDER
import os
import dropbox
from PIL import Image

strLocalDropBoxPath = "C:/Users/Sandipan/Desktop"
strRemoteDropBoxPath = ["Reporter","Reporter","Images","2019-Albums"]

# To-Do
# v12 - Pagination
# v11 - Focus only on folders
# v14 - Local check
# v20 - Recursive

# Find out if DropBox item ID is a folder
def fnIsDropBoxFolder(objDbx, objItemID):
    try:
        objEntries = objDbx.files_list_folder(objItemID).entries
        if len(objEntries)>0:
            return 1
        else:
            return 0
    except:
        return 0

# Load Root Folder Content List
def fnDropBoxFolderList(objDbx, objItemID):
    objResults = objDbx.files_list_folder(objItemID)
    binPagination = objResults.has_more
    if binPagination:
        strCursor = objResults.cursor
    while binPagination:
        print("There is more")    
        objResultsNext = objDbx.files_list_folder_continue(strCursor)
        binPagination = objResultsNext.has_more
        if binPagination:
            strCursor = objResultsNext.cursor
        objResults.entries.append(objResultsNext.entries)
    return objResults

def fnListOfLocalFolderEntries(strFolderName):
    try:
        return (1,os.listdir(strLocalDropBoxPath + "/" + strFolderName))
    except:
        return (0,[])

def fnIsLocal(strFolderPath, strFolderName):
    try:
        strParentFolderPath = strFolderPath[:(len(strFolderPath)-len(strFolderName))]
        # print("LOOKING FOR: " + strFolderName + " in " + strLocalDropBoxPath + "/" + strParentFolderPath)
        if strFolderName in os.listdir(strLocalDropBoxPath + "/" + strParentFolderPath):
            # print("Found")
            return 1
        elif strFolderName == "":
            # print("Root level")
            return 1
        else:
            # print("Not found")
            return 0
    except:
        return 0

# Recursion Process
def fnCompareFolder(objDbx, strFolderPath, strFolderName, objFolderId, intDepth):
    if 1:
        # print(strFolderPath[:(len(strFolderPath)-len(strFolderName))] + ":" + strFolderName + " is a folder")
        if fnIsLocal(strFolderPath, strFolderName):
            # It's local as well
            # print("It's local")
            objResult = fnDropBoxFolderList(objDbx, objFolderId)
            objResultEntries = objResult.entries
            binAnyLocal = 0
            binAllLocal = 1
            print("-> " * (intDepth + 1) + strFolderName + "")
            for objEntry in objResultEntries:
                strEntryId = objEntry.id
                strEntryName = objEntry.name
                strEntryPath = objEntry.path_display[1:]
                if fnIsLocal(strEntryPath, strEntryName):
                    binAnyLocal = 1
                else:
                    binAllLocal = 0
                if intDepth<4:
                    # If it's one directory deep
                    if fnIsDropBoxFolder(objDbx, strEntryId):
                        # It's a folder
                        fnCompareFolder(objDbx, strEntryPath, strEntryName, strEntryId, intDepth+1)
        else:
            # It's a folder but not local
            # print("-> " * (intDepth + 1) + strFolderName + " : NOT SELECTED")
            intOne = 1
    else:
        # it's not a folder
        return

# User Info
objDbx = dropbox.Dropbox('FIND-SECRET-FROM-DEVELOPMENT-DROPBOX-FOLDER')
print("%s" % objDbx.users_get_current_account().name.display_name)
print("-------------------------------------------")
print

# Load an image from Image Library and show it
objFolderId = ""
objEntries = fnDropBoxFolderList(objDbx, "").entries
for strFolder in strRemoteDropBoxPath:
    binFound = 0
    for objEntry in objEntries:        
        if objEntry.name == strFolder:
            objFolderId = objEntry.id
            objEntries = fnDropBoxFolderList(objDbx, objFolderId).entries
            binFound = 1
            break
    if binFound == 0:
        print("Path not found at remote folder")
        break
print(objEntries)

# Load Root Folders
'''
objResults = fnDropBoxFolderList(objDbx, "")
fnCompareFolder(objDbx, "", "", "", 0)

# Print Folder Tree
for objMetaData in objResults.entries:
    intTempCtr = 0
    strParentFolderName = objMetaData.name
    strParentFolderPath = objMetaData.path_display[1:]
    if strParentFolderName in os.listdir(strLocalDropBoxPath):
        print(objMetaData.name + " (+)")
        for objMetaData2 in fnDropBoxFolderList(objDbx, objMetaData.id).entries:
            intTempCtr = intTempCtr + 1
            strFolderName = objMetaData2.name
            if intTempCtr<10 and strParentFolderName in os.listdir(strLocalDropBoxPath):
                if fnIsDropBoxFolder(objDbx, objMetaData2.id):
                    strIsFolder = "(*)"
                else:
                    strIsFolder = ""
                # print("Searching for " + strFolderName + " in " + strLocalDropBoxPath + "::" + strParentFolderPath)
                if strFolderName in os.listdir(strLocalDropBoxPath + "/" + strParentFolderPath):
                    strIsLocal = "(+)"
                else:
                    strIsLocal = "(-)"
                print("-> " + strFolderName + " " + strIsFolder + " " + strIsLocal)
            elif strParentFolderName in os.listdir(strLocalDropBoxPath):
                # print("NOT LOCALLY AVAILABLE")
                break
            else:
                break
    else:
        print(objMetaData.name + " (-)")
'''
