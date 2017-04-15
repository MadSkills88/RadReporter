import textmining_v3
import re
import csv
import glob, os

### NEED TO SORT NEXUS!!! ###

# Finds all occurrences of a substring within a string
def findAll(str, sub):
    indexlist = []
    index = 0
    while index < len(str):
        index = str.find(sub, index)
        if index == -1:
            break
        indexlist.append(index)
        # print(sub, 'found at', index)
        index += len(sub)
    return indexlist

# Writes for 1D list
def write(path, list):
    out = open(path, 'w')
    for row in list:
        for column in row:
            # print(column)
            out.write('%s' % column)  # add %d, for separate cells
        out.write('\n')
    out.close()

# Returns all the file names in the directory
def getFileNames(directory):
    fileNames = []
    os.chdir(directory)
    for file in glob.glob("*.txt"):
        # print(file)
        fileNames.append(file)
    # print(fileNames)
    return fileNames

# Returns the AssnNum by removing .txt from file name
def getAssnNum(filename):
    extension = ".txt"
    lengthOfFileName = len(filename)
    lengthOfExtension = len(extension)
    lengthOfAssnNum = lengthOfFileName - lengthOfExtension
    return filename[0:lengthOfAssnNum]

# Returns number of lines in a file
def getNumberOfLines(filename):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    count = 0
    for line in lines:
        count += 1
    return count

# Returns line number of the first occurrence of a keyword
def getLineNumber(filename, keyword):
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    count = 0
    lineNumber = 0
    # if line contains the keyword then return the number of the line
    for line in lines:
        count += 1
        if keyword in line.lower(): lineNumber = count
    return lineNumber

# Returns the overall index of a keyword in the file (instead of only getting the index of the keyword within its line)
# Only works for the first instance
def getIndexOf(filename, keyword):
    file = open(filename, "r")
    data = file.read()
    # lines = file.readlines()
    file.close()
    index = 0
    # if line contains the keyword then return the number of the line
    if keyword in data: index = data.find(keyword)
    return index

# Returns a list of the indexes of the beginning of all the line headers (rows)
def getIndexOfLineHeaders(filename):
    indicesOfLines = []
    lineNames = ["Indications", "REPORT", "EXAM", "COMPARISON", "IMPRESSION", "HISTORY", "PROSTATE", "LOCAL STAGING", "LYMPH NODES", "BONES"]
    for lineName in lineNames:
        indicesOfLines.append(getIndexOf(filename, lineName))
    return indicesOfLines

# def test1():
#     list = []
#     directory = "C:\\Users\\M144964\\Desktop\\rad"
#     filenames = getFileNames(directory)
#     for filename in filenames:
#         file = open(filename, "r")
#         data = file.read()
#         file.close()
#         # thing = re.compile('invasion')
#         thing = re.compile('T[0-9]')
#         for match in re.finditer(thing, data):
#             index = match.start()
#             signal = data[index:index+2]
#             print(signal)
#             list.append(signal)
#         print('\n')
#     print(list)

# Sort by AssnNum
def sortLines(inputPath, outputPath):
    nexus = open(inputPath, "r")
    nexusLines = nexus.readlines()
    nexus.close()
    AssnNumList = []
    for line in nexusLines:
        if line != nexusLines[0]:
            AssnNum = int(line[12:20])
            AssnNumList.append(AssnNum)
            # print(AssnNum)
    print(AssnNumList)
    AssnNumList = sorted(AssnNumList, key=int)
    print(AssnNumList)
    for line in nexusLines:
        for num in AssnNumList:
            if str(num) in line:
                nexusLines[AssnNumList.index(num)] = line
    print(nexusLines)
    write(outputPath, nexusLines)

def addSignalWeighting(inputPath, outputPath, directory):
    list = []
    signal1 = 'T1'
    signal2 = 'T2'
    filenames = getFileNames(directory)
    for filename in filenames:
        file = open(filename, "r")
        data = file.read()
        file.close()
        if signal1 in data and signal2 in data:
            list.append(signal1 + ' ' + signal2)
        elif signal1 in data:
            list.append(signal1)
        elif signal2 in data:
            list.append(signal2)
        else:
            list.append('')
    print(list)
    print(len(list))
    nexus = open(inputPath, "r")
    nexusLines = nexus.readlines()
    nexus.close()
    # Because we want to skip the first line (the headers)
    lineNum = -1
    finalNexusLines = []
    for line in nexusLines:
        # gets rid of the '\n' after each line, and addes a ',' to create a separate cell
        line = line[1:len(line) - 1] + ","
        line += list[lineNum]
        print(line)
        lineNum += 1
        finalNexusLines.append(line)
    finalNexusLines[0] = "Date,AssnNum,ClinicNum,Name,Age,Sex,Scanner,Code,Description,Category,Coil,SignalWeight"
    print(finalNexusLines)
    write(outputPath, finalNexusLines)

def addIndications(inputPath, outputPath, directory):
    list = []
    # in no particular order
    indication1 = "Metastatic Prostate Ca"
    indication2 = "Elevated Prostate-Specific Antigen (PSA)"
    indication3 = "Ca Prostate NOS"
    indication4 = "Screening Exam Prostate Ca"
    indication5 = "Microhematuria NOS"
    indication6 = "Hyperplasia Prostate (BPH) Localized With Obstruction"
    indication7 = "Ca Prostate Chemical Recurrence (PSA)"
    indication8 = "Metastasis (Mets) To Lymph Node Multiple Site"
    indication9 = "Metastatic Prostate Ca"
    indication10 = "Hydronephrosis"
    indication11 = "Osteopetrosis"
    indication12 = "Prostate Exam (DRE) Abnormal"
    filenames = getFileNames(directory)
    for filename in filenames:
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        for line in lines:
            if "Indications" in line:
                indications = line[13:len(line)-1]
                list.append(indications)
                break
        file = open(filename, "r")
        data = file.read()
        file.close()
        if "Indications" not in data:
            list.append('')
    print(list)
    print(len(list))

    # nexus = open(inputPath, "r")
    # nexusLines = nexus.readlines()
    # nexus.close()
    # # Because we want to skip the first line (the headers)
    # lineNum = -1
    # finalNexusLines = []
    # for line in nexusLines:
    #     # gets rid of the '\n' after each line, and addes a ',' to create a separate cell
    #     line = line[1:len(line) - 1] + ","
    #     line += list[lineNum]
    #     print(line)
    #     lineNum += 1
    #     finalNexusLines.append(line)
    # finalNexusLines[0] = "Date,AssnNum,ClinicNum,Name,Age,Sex,Scanner,Code,Description,Category,Coil,SignalWeight,Indications"
    # print(finalNexusLines)
    # write(outputPath, finalNexusLines)

def main():
    # path = 'C:\\Users\\M144964\\Desktop\\mapper.csv'
    inputPath = 'C:\\Users\\M144964\\Desktop\\nexus.csv'
    outputPath = 'C:\\Users\\M144964\\Desktop\\nexus0.csv'
    directory = "C:\\Users\\M144964\\Desktop\\rad2"
    # addIndications(inputPath, outputPath, directory)
    sortLines(inputPath, outputPath)

main()
