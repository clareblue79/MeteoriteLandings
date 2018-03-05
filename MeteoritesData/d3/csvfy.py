"""
Filename: csvfy.py
Modified by: Chetna Mahajan and Clare Frances Lee
Modified date: 05.14.2017

A python script that formats the textfile in a correct csv format for our 
data visualization application for country data (countryName, ISO code, data)
"""

def makeIsoDict(csvFileName):
     """
     @param: takes in a string file name of a csv file of iso and country names  
     @return: a dictionary of country as a key and iso code as the value
     """
     isoDict = {"None": "None"}
     
     reader= open(csvFileName, "r")
     
     for line in reader:
        line = line.split(",") #split by comma
        country = line[0]
        iso = line[1]
        isoDict[country] = iso.replace("\n", '')
        
     return isoDict
    


def getISO(countryName, ISODict):
     """
     @param: a countryName string and dictionary of country as key and 
     ISO code as value
     @return: iso of the country from the ISO dictionary
     """
     return isoDict[countryName]


def cleanLine(line1, ISODict):
    """
   @param: a string which is a line from the first text file
   and a python dictionary containing country and iso code info  
   @return: a cleaned string  which is the line in csv format
    """
    line = line1.split('"') #split by quotes
    country = line[1]
    iso = getISO(country, ISODict)
    freq = line[2].replace("\t",'')
    cleaned = country + "," + iso + "," + freq
    return cleaned
        

def readfile(readName, writeName, ISODict):
    """
    @param: takes in two file names for input and output and a
    python dictionary containing country and iso values 
      
    @return: csv file with cleaned data
    """
    reader= open(readName, "r")
    writer = open(writeName, 'w')
    
    for line in reader :
        writer.write(cleanLine(line, ISODict))
    writer.close()
    
    
#isoDict = makeIsoDict("iso.csv")
#readfile('countryFrequency.txt', 'countryFrequency.csv', isoDict)