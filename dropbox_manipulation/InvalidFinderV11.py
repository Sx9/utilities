import os, sys, dropbox, pickle
from datetime import datetime

# Invalid / Incompatible Character finder
# https://help.dropbox.com/installs-integrations/sync-uploads/files-not-syncing

intLogLevel = 3
strDropBoxAccessKey = "FIND-SECRET-FROM-DEVELOPMENT-DROPBOX-FOLDER"
strInvalidCharacters = "/\\<>:\"|?*"
strInvalidEndCharacters = "."
intInvalidPathLength = 255
lstFolderToSearch = ["Work", "GalaxE", "FromSG-2012-AsOf-20171104", "Data", "Projects", "Arrow", "Arrow-GxTrace"]
lstFolderToSearch = ["Work", "GalaxE"]
lstFolderToSearch = ["Website Backups"]
lstFolderToSearch = ["Reporter", "Reporter"]
lstFolderToSearch = ["Apps"]
lstFolderToSearch = ["Sandipan Personal Data", "ComputerBackups", "iOS"]

# Initialize the DropBox connection using API key provided

def fnInitDropBox(strRootPath, strDropBoxAccessKey):

    lstRemoteDropBoxReporterPath = strRootPath.split("/")

    # User Info
    objDbx = dropbox.Dropbox('%s' % strDropBoxAccessKey)
    strDropBoxAccount = "DropBox Account: %s" % objDbx.users_get_current_account().name.display_name
    print(strDropBoxAccount)
    print("-" * len(strDropBoxAccount))
    print

    return objDbx

def fnDropBoxFolderList(objDbx, objItemID):
    objResults = dropbox.files.ListFolderResult()
    try:
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
    except:
        return objResults
    return objResults

# Finds out if the path provided is a folder

def fnIsDropBoxFolder(objDbx, objItem):
    try:
        if intLogLevel >= 4:
            print(objItem.path_display)
            print(objItem)
        if isinstance(objItem, dropbox.files.FolderMetadata):
            if intLogLevel >= 4:
                print("-> FILE")
            return True
        else:
            if intLogLevel >= 4:
                print("-> FOLDER")
            return False
    except:
        if intLogLevel >= 4:
            print("-> ERROR")
        # if intLogLevel >= 1:
            # print("%s" % objItem)
        return False
    # We need to fix the above - this is resulting in another DropBox API call for every item :(
    '''
    try:
        if len(self.fnDropBoxFolderList(objDbx, objItem.id).entries) > 0:
            if intLogLevel >= 3:
                print("%s IS A FOLDER" % objItem.name)
            return True
        else:
            if intLogLevel >= 3:
                print("%s IS AN EMPTY FOLDER" % objItem.name)
            return False
    except:
        if intLogLevel >= 3:
            print("%s IS NOT A FOLDER" % objItem.name)
        return False
    '''

def fnIsDropBoxFile(objDbx, objItem):
    try:
        if intLogLevel >= 4:
            print(objItem.path_display)
            print(objItem)
        if isinstance(objItem, dropbox.files.FileMetadata):
            if intLogLevel >= 4:
                print("-> FILE")
            return True
        else:
            if intLogLevel >= 4:
                print("-> FOLDER")
            return False
    except:
        if intLogLevel >= 4:
            print("-> ERROR")
        # if intLogLevel >= 1:
            # print("%s" % objItem)
        return False

# Finds out size of file in file path

def fnDropBoxFileSize(self, objDbx, strFilePath):
    try:
        intSize = objDbx.files_get_metadata(strFilePath).size
        if intLogLevel >= 2:
            print(strFilePath, intSize)
    except:
        return 0
    return intSize

def fnIsInvalid(strEntryName, strEntryPath):

    binInvalid = False
    intEntryLength = len(strEntryPath)
    if intEntryLength >= intInvalidPathLength:
        binInvalid = True
        if intLogLevel >= 2:
            print("Path length [%s] at %d is too long" % (strEntryPath, intEntryLength))
    for chrInvalider in strInvalidCharacters:
        if chrInvalider in strEntryName:
            binInvalid = True
            if intLogLevel >= 2:
                print("Entry name [%s] has invalid character [%s]" % (strEntryName, chrInvalider))
    chrFinalCharacter = strEntryName[len(strEntryName)-1]
    if chrFinalCharacter in strInvalidEndCharacters:
        binInvalid = True
        if intLogLevel >= 2:
            print("Entry name [%s] last character is invalid [%s]" % (strEntryName, chrFinalCharacter))

    return binInvalid
        
def fnValidateDropBoxFolder(objEntries, lstFolders, lstInvalids):

    for objEntry in objEntries:
        try:
            strEntryID = objEntry.id
            strEntryName = objEntry.name
            strEntryPath = objEntry.path_display
        except:
            break
        if fnIsInvalid(strEntryName, strEntryPath):
            lstInvalids.append([strEntryID, strEntryName, strEntryPath])
            if intLogLevel >= 1:
                print("FOLDER/FILE WITH ISSUE: %s" % strEntryPath)
        if (fnIsDropBoxFolder(objDbx, objEntry)):
            lstFolders.append([strEntryID, strEntryName, strEntryPath])
            if intLogLevel >= 3:
                intDepth = strEntryPath.count("/")
                print("%d: FOLDER: %s:%s" % (len(lstFolders), "-> " * intDepth, strEntryName))
            objEntries = fnDropBoxFolderList(objDbx, strEntryID).entries
            lstFolders, lstInvalids = fnValidateDropBoxFolder(objEntries, lstFolders, lstInvalids)

    return lstFolders, lstInvalids

def fnSaveData(strFilePath, lstToSave):

    try:
        with open(strFilePath, 'wb') as f:
            pickle.dump(lstToSave, f)
    except:
        return False

    return True

def fnLoadData(strFilePath):

    lstToLoad = []
    try:
        with open(strFilePath, 'rb') as f:
            lstToLoad = pickle.load(f)
    except:
        pass

    return lstToLoad

# MAIN PROGRAM

objDbx = fnInitDropBox(".", strDropBoxAccessKey)
objEntries = fnDropBoxFolderList(objDbx, "").entries
for strFolder in lstFolderToSearch:
    binFound = 0
    for objEntry in objEntries:        
        if objEntry.name == strFolder:
            objFolderId = objEntry.id
            objEntries = fnDropBoxFolderList(objDbx, objFolderId).entries
            binFound = 1
            break
    if binFound == 0:
        if intLogLevel >= 1:
            print("Album Root Path not found at remote folder")
        break
lstFolders = []
lstInvalids = []
lstFolders, lstInvalids = fnValidateDropBoxFolder(objEntries, lstFolders, lstInvalids)
print("Total %d issues across %d folders" % (len(lstInvalids), len(lstFolders)))

strPath = os.getcwd()
print(strPath)
datNow = datetime.now()
strTimestamp = int(datetime.timestamp(datNow))
strScanFolderPath = os.path.join(strPath, "Folders-Scanned-%s.pkl" % strTimestamp)
strScanIssuesPath = os.path.join(strPath, "Files-Issues-%s.pkl" % strTimestamp)
fnSaveData(strScanFolderPath, lstFolders)
fnSaveData(strScanIssuesPath, lstInvalids)

lstFolderScan = fnLoadData(strScanFolderPath)
lstInvalidFiles = fnLoadData(strScanIssuesPath)
print(lstFolderScan, lstInvalidFiles)
