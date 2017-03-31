import textmining_v3
import re
import csv
import glob, os

# parser.py

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

#If there is no series return empty!!!
def getSeries(filename):
    # read the files
    list = []
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    keyword = "series"
    # print the lines
    for line in lines:
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
    return list;

def write(list):
    # list = [["Patient1_Series", 1, 2], ["Patient2_Series", 2, 3], ["Patient3_Series", 4, 5]]
    out = open('C:\\Users\\M144964\\Desktop\\series.csv', 'w')
    for row in list:
        for column in row:
            # print(column)
            out.write('%s,' % column)  #add %d, for separate cells
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

def getFileNames(directory):
    fileNames = []
    os.chdir(directory)
    for file in glob.glob("*.txt"):
        # print(file)
        fileNames.append(file)
    # print(fileNames)
    return fileNames

def getAssnNum(filename):
    extension = ".txt"
    lengthOfFileName = len(filename)
    lengthOfExtension = len(extension)
    lengthOfAssnNum = lengthOfFileName - lengthOfExtension
    return filename[0:lengthOfAssnNum]

def main():
    seriesList = []
    directory = "C:\\Users\\M144964\\Desktop\\rad"
    # directory = "Z:\\MR\\7.0 Research Projects\\Anthony-Prostate-Project\\radreports"
    filenames = getFileNames(directory)
    for filename in filenames:
        AssnNum = getAssnNum(filename)
        series = getSeries(filename)
        series = [AssnNum] + series
        seriesList.append(series)
        # print(series)
        # print(seriesList)
        write(seriesList)

main()

