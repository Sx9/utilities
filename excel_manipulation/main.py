import os, re, pathlib, time, sys
from excellogwriter import ExcelMLLogWriter

objFile = ExcelMLLogWriter("D:\\Dropbox (Sandipan.com)\\Development\\Utils\\excel_manipulation\\Logs.xlsx")

intTrainTimeStamp = int(time.time())
strTrainTimeStamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(intTrainTimeStamp))
objFile.fnTrainingUpdate(["BINARY", "24:48:1024", strTrainTimeStamp, 1024, "ABC"])

intPredictTimeStamp = int(time.time())
strPredictTimeStamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(intPredictTimeStamp))
objFile.fnPredictionUpdate(strTrainTimeStamp, [strPredictTimeStamp, "DEF.txt", .96, 0.9099])
