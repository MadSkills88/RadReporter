import textmining_v3
import re
import csv
import glob, os
from openpyxl import load_workbook

# Need to read what row the first series starts on for each file... not all of the start on prostate for example
# Also need to add way to skip over multiple rows... many files for example have series for row 5, 7, 10, 11... skips over 6, 8, 9
# ... work on getCategorizedSeries and categorizeSeries and their dependencies

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

# Returns a list of all the series numbers
def getSeries(filename):
    # read the files
    list = []
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    keyword = "series"
    count = 0
    # print the lines
    for line in lines:
        count += 1
        if len(line) > 1 and keyword in line.lower():
            seriesNumber = re.compile('series ([0-9]*)')
            seriesList = (seriesNumber.findall(line))
            for series in seriesList:
                list.append(series)
            # seriesIndexList = findAll(line, "series")
            # print(filename, seriesIndexList)
            # imageIndexList = findAll(line, "image")
            # print(imageIndexList)
            # count = 0
            # if len(seriesIndexList) > 0:
            #     for index in seriesIndexList:
            #         # print(line[index:imageIndexList[count]])
            #         # list.append(line[index+len("series")+1:imageIndexList[count]-1])
            #         list.append(line[index + len("series") + 1:regexList[count] - 1])
            #         count += 1
    # print (count)
    return list;

# Writes a list of lists (2D list) into a .csv file
def write(path, list):
    # list = [["Patient1_Series", 1, 2], ["Patient2_Series", 2, 3], ["Patient3_Series", 4, 5]]
    out = open(path, 'w')
    for row in list:
        for column in row:
            # print(column)
            out.write('%s,' % column)  #add %d, for separate cells
        out.write('\n')
    out.close()

# Writes for 2D list but space instead of comma between cells
def write2(path, list):
    # list = [["Patient1_Series", 1, 2], ["Patient2_Series", 2, 3], ["Patient3_Series", 4, 5]]
    out = open(path, 'w')
    for row in list:
        for column in row:
            out.write('%s ' % column)
        out.write('\n')
    out.close()

# Writes for 1D list
def write3(path, list):
    out = open(path, 'w')
    for item in list:
        out.write('%s,' % item)
        out.write('\n')
    out.close()

# def write():
#     list = [["Series"], [1, 2], [2, 3], [4, 5]]
#     out = open('C:\\Users\\M144964\\Desktop\\out.csv', 'w')
#     for row in list:
#         for column in row:
#             print (column)
#             if column == "Series": out.write('%s' % column)
#             else: out.write('%s;' % column)  #add %d, for separate cells
#         out.write('\n')
#     out.close()

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

# Returns line number of the first occurence of a keyword
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

# # Returns the overall index of the series in the file
# def getIndexOfSeries(filename):
#     # read the files
#     list = []
#     file = open(filename, "r")
#     data = file.read()
#     file.close()
#     keyword = "series"
#     # print the lines
#     if keyword in data.lower():
#         seriesNumber = re.compile('series ([0-9]*)')
#         seriesList = (seriesNumber.findall(data))
#         for series in seriesList:
#             list.append(series)
#     return list;

def getIndexOfSeries(filename):
    # read the files
    list = []
    file = open(filename, "r")
    data = file.read()
    file.close()
    keyword = "series"
    # print the lines
    if keyword in data.lower():
        seriesNumber = re.compile('series ([0-9]*)')
        for match in re.finditer(seriesNumber, data):
            index = match.start()
            list.append(index)
    return list;

#Categorize the series based on the category/line header they fall under
def categorizeSeries(filename):
    lineIndices = getIndexOfLineHeaders(filename)
    seriesIndices = getIndexOfSeries(filename)
    categoryList = []
    for seriesIndex in seriesIndices:
        for i in range(len(lineIndices)):
            if lineIndices[i-1] != 0:
                if seriesIndex < lineIndices[i] and seriesIndex > lineIndices[i-1]:
                    categoryList.append(i)
            if lineIndices[i-1] == 0:
                if seriesIndex < lineIndices[i] and seriesIndex > lineIndices[i-2]:
                    # very unelegant and ugly but too lazy to fix
                    if lineIndices[i-2] != 0:
                        categoryList.append(i-1)
                    else:
                        categoryList.append(i-2)
        if seriesIndex > lineIndices[len(lineIndices)-1]:
            categoryList.append(len(lineIndices))
    return categoryList

def getCategorizedSeries(filename):
    seriesList = getSeries(filename)
    categories = categorizeSeries(filename)
    # the first row with a series number in the file... The stuff we care about starts on row 7, PROSTATE
    # if len(categories) > 0:
    #     rowOfFirstSeries = categories[0]
    #     if rowOfFirstSeries > 7:
    #         difference = rowOfFirstSeries - 7
    #         j = 0;
    #         while j < difference:
    #             seriesList = [','] + seriesList
    #             j += 1
    i = 1
    count = 0
    while i < (len(categories)):
        if categories[i] > categories[i-1]:
            seriesList.insert(i + count, ',')
            count += 1
        i += 1
    return seriesList

def writeMetaData():
    path = 'C:\\Users\\M144964\\Desktop\\metadata.csv'
    inputList = []
    # used to be called headers but that could be confusing
    categories = [["AssnNum", "Lines", "Indications-Index", "ORIGINAL/REVISED REPORT-Index", "EXAM-Index", "COMPARISON-Index", "IMPRESSION-Index", "HISTORY-Index", "PROSTATE-Index", "LOCAL STAGING-Index", "LYMPH NODES", "BONES-Index"]]
    inputsList = categories + inputList
    directory = "C:\\Users\\M144964\\Desktop\\rad"
    # directory = "Z:\\MR\\7.0 Research Projects\\Anthony-Prostate-Project\\radreports"
    filenames = getFileNames(directory)
    for filename in filenames:
        numberOfLines = getNumberOfLines(filename)
        AssnNum = getAssnNum(filename)
        inputs = getIndexOfLineHeaders(filename)
        inputs = [AssnNum] + [numberOfLines] + inputs
        inputsList.append(inputs)
        # print(series)
        # print(seriesList)
        write(path, inputsList)
        print(getIndexOfLineHeaders(filename))

# Get specific series... example: get prostate series by looking at all the series on row 7
def getSpecificSeries(filename, seriesRowNumber):
    specificSeries = []
    seriesList = getSeries(filename)
    categories = categorizeSeries(filename)
    for i in range(len(categories)):
        if categories[i] == seriesRowNumber:
            specific = seriesList[i]
            specificSeries.append(specific)
    return specificSeries

def getProstateSeries(filename):
    return getSpecificSeries(filename, 7)

def getLocalStagingSeries(filename):
    return getSpecificSeries(filename, 8)

def getLymphSeries(filename):
    return getSpecificSeries(filename, 9)

def getBoneSeries(filename):
    return getSpecificSeries(filename, 10)

def countOccurrences(filename, category, keyword):
    count = 0
    if category.lower() == "prostate":
        series = getProstateSeries(filename)
    elif category.lower() == "local_staging":
        series = getLocalStagingSeries(filename)
    elif category.lower() == "lymph":
        series = getLymphSeries(filename)
    elif category.lower() == "bone":
        series = getBoneSeries(filename)

    for serie in series:
        if serie == keyword:
            count += 1
    return count

# Collects all of the distinct series of the __category__ in a list... ex category: "prostate"
def parseDistinctSeries(category):
    directory = "C:\\Users\\M144964\\Desktop\\rad"
    filenames = getFileNames(directory)
    distinctSeries = []
    distinctSeriesNum = []
    for filename in filenames:
        if category.lower() == "prostate":
            series = getProstateSeries(filename)
        elif category.lower() == "local_staging":
            series = getLocalStagingSeries(filename)
        elif category.lower() == "lymph":
            series = getLymphSeries(filename)
        elif category.lower() == "bone":
            series = getBoneSeries(filename)

        for serie in series:
            if serie not in distinctSeries and serie != '':
                distinctSeries.append(serie)

    distinctSeriesNum = sorted(distinctSeries, key=lambda x: int(x))
    print (distinctSeriesNum)
    return distinctSeriesNum

def counter():
    count = 0
    category = "lymph"
    # Don't forget to change to path to match the category
    path = 'C:\\Users\\M144964\\Desktop\\countLymphSeries.csv'
    directory = "C:\\Users\\M144964\\Desktop\\rad"
    filenames = getFileNames(directory)
    keywords = parseDistinctSeries(category)
    countList = []
    # The list that will be written into path
    writtenList = []
    for keyword in keywords:
        for filename in filenames:
            count += countOccurrences(filename, category, keyword)
        countList.append(count)
        count = 0
    # since countList and keywords should be same length
    for i in range(len(countList)):
        writtenList.append(keywords[i] + "," + str(countList[i]))
    print (countList)
    write3(path, writtenList)
    # return countList

def main():
    path = 'C:\\Users\\M144964\\Desktop\\prostateSeries.csv'
    seriesList = []
    # used to be called headers but that could be confusing
    fields = [["AssnNum", "Series"]]
    seriesList = fields + seriesList
    directory = "C:\\Users\\M144964\\Desktop\\rad"
    # directory = "Z:\\MR\\7.0 Research Projects\\Anthony-Prostate-Project\\radreports"
    filenames = getFileNames(directory)
    for filename in filenames:
        AssnNum = getAssnNum(filename)
        # # series = getSeries(filename)
        # # print(series)
        series = getProstateSeries(filename)
        print(series)
        series = [AssnNum] + series
        seriesList.append(series)
        # # print(series)
        # # print(seriesList)
        write(path, seriesList)

        # print(getIndexOfLineHeaders(filename))
        # print (categorizeSeries(filename))
        # print (getCategorizedSeries(filename))

# countOccurrences('C:\\Users\\M144964\\Desktop\\rad2\\19908988-2.txt')
# main()
counter()
# parseDistinctSeriesProstate()
