#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Laird
#
# Created:     28/10/2019
# Copyright:   (c) Laird 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

file = ('C:\\Users\\Laird\\Desktop\\GEOG 378\\LAB_3\\CityPop.csv')

import math
#create a class  and assign init method for values from .csv file
class City(object):

    #entering empty variables for printPopChange getattr() function to call on
  pop1970 = ''
  pop1975 = ''
  pop1980 = ''
  pop1985 = ''
  pop1990 = ''
  pop1995 = ''
  pop2000 = ''
  pop2005 = ''
  pop2010 = ''


    #init method with proper vales
  def __init__(self, name='n/a', label = 'n/a', lat = 0, lon = 0, pop70 = 0,
  pop75 = 0, pop80 = 0, pop85 = 0, pop90 = 0, pop95 = 0, pop00 = 0, pop05 = 0,
  pop10 = 0):

    #28-Oct fixed self.pop values to correspond to empty variables for printPopChange method
        self.name = name
        self.label = label
        self.lat = lat
        self.lon = lon
        self.pop1970 = pop70
        self.pop1975 = pop75
        self.pop1980 = pop80
        self.pop1985 = pop85
        self.pop1990 = pop90
        self.pop1995 = pop95
        self.pop2000 = pop00
        self.pop2005 = pop05
        self.pop2010 = pop10



#28-Oct - The following section was not used, but was made for practice.

  #method to set parameters for proper lat, lon, print if not valid
  #def setlatlon(self,lat,lon):
    #if lat > 90 or lat < -90:
      #print('The latitiude value is not valid.\nThe value entered should be between -90 and 90.')
    #else:
       # self._lat = float(lat)
    #if lon > 180 or lon < -180:
      #print('The longitude value is not valid.\nThe value entered should be between -180 and 180.')
   # else:
      #self._lon = float(lon)

  #method for obtaining lat, lon if needed
  #def getlatlon(self):
    #return (self._lat,self._lon)


  #method for printDistance of two cities. To call use example Tokyo.printDistance(New Delhi)

  def printDistance(self, othercity):
    #get radians for self and othercity respective lat,lon
    #28OCT corrected issue setting self.lat as variable(switched to city1lat) to math.radians(self.lat) and causing misprint of attribute self.lat later to unintended radian value
    city1lat = math.radians(self.lat)
    city1lon = math.radians(self.lon)
    city2lat = math.radians(othercity.lat)
    city2lon = math.radians(othercity.lon)
    #formula for great circle
    formula = math.acos(math.sin(city1lat)*math.sin(city2lat) + math.cos(city1lat)*math.cos(city2lat) *math.cos((city1lon) - (city2lon)))

    #multiply by the radius of the earth which is approximately 6400 km​
    distance = formula * (6400)
    #rounding the distance
    distance = round(distance, 2)
    #print the string returning distance
    print('\n The distance between the two locations is ' + str(distance) + 'km.')


    #method for finding PopChange given a city and two years
  def printPopChange(self, year1, year2):

    #setting year1, year2 to match the variable in City class
    #convert to string and add 'pop' to beginning

    year1 = 'pop' + str(year1)
    year2 = 'pop' + str(year2)

    #call getattr() on given city with updated year1, year2 variables
    pop1 = getattr(self, year1)
    pop2 = getattr(self, year2)


    #if statement to capture cells from CityPop.csv with no data, else continue to formula
    if float(pop1) == 0 or float(pop2) == 0:
        print('No data is available for one or both years provided.')


    #subtract the years with negative sign in front to account for increase/decrease in population
    #then round and move to print statements according to the difference relative to zero
    #added abs() to else statement for decrease to read properly
    else:
        change = -(float(pop1) - float(pop2))
        change = round(change, 2)

        if change > 0:
            print('The population increased by', change, 'million between those years.')
        elif change == 0:
            print('The population stayed the same between those years.')
        else:
            print('The population decreased by', abs(change), 'million between those years.')


print("Starting +++++++++++++++++")


#try/except to prevent crash from file path no opening
try:
     f = open(file, 'rt')
except:
     print("can’t open",file)

#create list and headers for CityPop.csv
cityList = f.readlines()
headers = cityList[0].strip().split(',')


# List used to store each of the cities
myCities = []


# Read the columns from the cityList
# ----------------------------------
for row in range(1,len(cityList)):
    columnList = cityList[row].strip().split(',')


    # Get the attributes from each City record: city, label, latitude, longitude and yr1970
    # and assign it to myCity, which is a class of type 'City'
    myCity = City(columnList[3],columnList[4], float(columnList[1]), float(columnList[2]),columnList[5], columnList[6], columnList[7],
    columnList[8], columnList[9], columnList[10], columnList[11], columnList[12], columnList[13])


    # Append the attributes for the current city record to the 'myCities' list
    myCities.append(myCity)

# Close the CSV File
f.close()


# Pick the first city - it can be any city
selectedCity1 = myCities[2]

# Pick the second city
selectedCity2 = myCities[4]

#Pick a third city with zero values to test
selectedCity3 = myCities[8]

# Run the 'printDistance()' function for the two cities above
selectedCity1.printDistance(selectedCity2)

#Run printPopChange using two cities and two years
selectedCity1.printPopChange(1985,1990)
selectedCity2.printPopChange(1990, 1975)
selectedCity3.printPopChange(1970,1980)


#Conclude by printing all attributes
for city in myCities:
    print(city.name, city.label, city.lat, city.lon, city.pop1970, city.pop1975, city.pop1980,
    city.pop1985, city.pop1990, city.pop1995, city.pop2000, city.pop2005, city.pop2010)


print("done ...")