import geocoder
import csv

def getCountryName(lat,lon):
    g = geocoder.google([lat, lon], method='reverse')
    return g.country_long


def cleanLine(line):
    """
   @param: a string which is a line from csv file
   @reutnr: checks if there is a null value, and returns the new 
   line with country names instead of longtitude and latitude 
    """
    #split line by comma
    #values = line.split(',')
    values = line[:9]
    print values
    lat = values[7]
    lon = values[8]
    
    if not str(lat) or not str(lon):
        values.append("None")
    elif abs(float(lat)) > 90:
       values.append("None")
    elif abs(float(lon)) > 180: 
        values.append("None")
    else:
        values.append(getCountryName(lat,lon))
    line = ",".join(map(str, values))
    return line + '\n'
        

def readfile(readName, writeName):
    file_reader= open(readName, "r+")
    read = csv.reader(file_reader)
    
    file_writer = open(writeName, 'w')
    
    #counter = 0
    for row in read :
        #counter += 1
        #if (counter+1)%6 == 0:
           # time.sleep(10)
        file_writer.write(cleanLine(row))
    file_writer.close()
    
readfile('meteoritelandings2.csv', 'meteoritesfinal3.csv')
