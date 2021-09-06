import os, re, pathlib, time, sys
from datetime import datetime
import xml.dom, xml.dom.minidom
# From https://www.datacamp.com/community/tutorials/python-xml-elementtree
import xml.etree.ElementTree as ET

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Color, Fill, Border, PatternFill, Side, GradientFill, Alignment
# From https://stackoverflow.com/a/52494457/14923106
from openpyxl.styles import Alignment

import docx
from docx import Document
from docx.shared import Inches
# From https://stackoverflow.com/questions/56658872/add-page-number-using-python-docx
from docx.oxml import OxmlElement, ns
# From https://stackoverflow.com/questions/18595864/python-create-a-table-of-contents-with-python-docx-lxml
from docx.oxml.ns import qn
# From https://stackoverflow.com/questions/57189055/why-cant-i-import-wd-align-paragraph-from-docx-enum-text
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# Uses OpenPyXL to read the Excel File
# https://openpyxl.readthedocs.io/en/stable/
# Install it using [pip install openpyxl]

# Uses Python-DOCX to write the Word File
# https://python-docx.readthedocs.io/en/latest/
# Install it using [pip install python-docx]

class ExcelLogWriter(object):

    def __init__(self, strFileAbsolutePath, lstColumns, lstColumnWidths):

        binSuccess = True
        binSuccess = self.fnInitializer()
        self.binExists = self.fnFindFile(strFileAbsolutePath, lstColumns)

        return

    def fnInitializer(self):

        # VARIABLE DECLARATION
        self.strVersion = "0030"
        self.intLogLevel = 3
        self.strAuthor = "sandipan.com"

        self.strRegex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        self.strHyperLinkImage = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Icon_External_Link.svg/1200px-Icon_External_Link.svg.png"
        self.strHyperLinkImageName = "1200px-Icon_External_Link.svg.png"
        self.strSandipanImageName = "logo2-200x130.png"
        self.intTitlePageSpacers = 3

        # SET UP STYLE
        self.fntHeaderFont = Font(name = "Tahoma", size = 12, color = "444444", bold = True)
        self.sidSide = Side(border_style="double", color="444444")
        self.bdrBorder = Border(bottom = sidSide)
        self.filFill = PatternFill("solid", fgColor = "BBBBBB")
        self.fntEntryFont = Font(name = "Tahoma", size = 10, color = "444444", bold = False)

        self.intHeaderRow = 3
        self.strWorksheetName = "LOG"
        self.lstColumnID = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

        return True

    def fnFindFile(self, strFileAbsolutePath, lstColumns):

        # IF XLS FILE EXISTS
        if os.path.exists(strFileAbsolutePath):

            # IF IT OPENS
            try:
                objWorkbook = load_workbook(filename=strFileAbsolutePath)
            except:
                return False, "NOT EXCEL FILE"

            # IF WORKSHEET IS FOUND
            lstWorksheets = objWorkbook.sheetnames
            if self.strWorksheetName in lstWorksheets:
                objWorksheet = objWorkbook[self.strWorksheetName]

                binColumnMatch = True
                for intCtr, strColumnName in enumerate(lstColumns):
                    # CHECK COLUMN HEADERS AND SEE IF THEY MATCH
                    if objWorksheet[self.lstColumnID[intCtr] + str(self.intHeaderRow)] == strColumnName:
                        pass
                    else:
                        binColumnMatch = False

                if not binColumnMatch:
                    return False, "COLUMNS DO NOT MATCH"

            else:
                return False, "WORKSHEET NOT FOUND"

        else:
            return False, "FILE NOT FOUND"

    return True, "FILE OK"

# Create and Prepare Excel File
objWorkbook = Workbook()
objWorksheet = objWorkbook.active
objWorksheet.title = "SOW List"
objWorksheet.sheet_properties.tabColor = "8888FF"

# Process SOW Analaysis File Header Row
lstGxFource = ["GxFource", "GxDash", "GxMaps", "GxWave", "O2A", "Outsource2", "GxCare", "GxInfra", "GxTrace", "GxPrime", "GxEngage", "GxClaim", "RxWave"]
lstColumnHeaders = ["", "Client", "SOW Folder", "Doc Name", "Doc Path", "Doc TStamp", "Doc Date", "Doc Time", "SOW Title Lines", "Scope/Deliverable related paragraphs"]
for strGxFource in lstGxFource:
    lstColumnHeaders.append(strGxFource)
lstColumnRef = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
lstColumnWidths = [5, 20, 50, 75, 5, 15, 10, 10, 100, 100, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]
for intCtr, strHeader in enumerate(lstColumnHeaders):
    strCellReference = lstColumnRef[intCtr] + "1"
    objWorksheet[strCellReference] = strHeader
    objCell = objWorksheet[strCellReference]
    objCell.font = fntHeaderFont
    objCell.border = bdrBorder
    objCell.fill = filFill
    objWorksheet.column_dimensions[lstColumnRef[intCtr]].width = lstColumnWidths[intCtr]

