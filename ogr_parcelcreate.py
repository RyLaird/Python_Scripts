import os, sys, ogr, gdalconst



#set data directory for input and output files
dataDir = 'C:\\working_directory\\'

#set filename
filename = (dataDir + r"powerline.shp")

#set driver to open datasources
driver = ogr.GetDriverByName('ESRI Shapefile')

dataSource = driver.Open(filename, gdalconst.GA_ReadOnly)

#check if no file at location and exit if none
if dataSource is None:
    print('Failed to open file')
    sys.exit(1)

#set layer and feat for calculation
layer = dataSource.GetLayer(0)
feat = layer.GetNextFeature()

#set line variable for proper geometry and nPts to get points along line
line = feat.GetGeometryRef()
nPts = line.GetPointCount()

#create variable LineLength and set to 0
LineLength = 0


#go through each point in nPts and obtain x,y for calculation
for i in range(nPts-1):
    fi = line.GetPoint(i)
    xi = fi[0]
    yi = fi[1]
    #print(yi)

    gi = line.GetPoint(i+1)
    xj = gi[0]
    yj = gi[1]

    #formula for distance
    d = ((xi - xj) ** 2 + (yi - yj) ** 2) ** 0.5
    #convert feet to miles
    dmi = (d/5280)

    #at distance to LineLength and round
    LineLength += dmi
    LineLength = round(LineLength, 3)

print("The length of the power line is " + str(LineLength) + " miles")

#close dataSource
dataSource = None

#set filename and open Parcels.shp
filename2 = (dataDir + "Parcels.shp")
dataSource2 = driver.Open(filename2, gdalconst.GA_ReadOnly)

#if no file, exit
if dataSource2 is None:
    print('Failed to open file')
    sys.exit(1)

#assign variables for layer, name, geometry type
ParcelsLayer = dataSource2.GetLayer(0)
ParcelsName = ParcelsLayer.GetName()
ParcelsType = ParcelsLayer.GetGeomType()
ParcelsTypeS = ogr.GeometryTypeToName(ParcelsType)


print('Layer', ParcelsName, 'is a', ParcelsTypeS)

#assign variables for featureDefn, fieldCount
featureDefn = ParcelsLayer.GetLayerDefn()
fieldCount = featureDefn.GetFieldCount()

print("The layer's feature definition has the following", fieldCount, "fields:")

#loop through fields and assign variables for feature columns
for i in range(fieldCount):
    fieldDef = featureDefn.GetFieldDefn(i)
    fldName = fieldDef.GetNameRef()
    fldWidth = fieldDef.GetWidth()
    fldPrecision = fieldDef.GetPrecision()
    fldType = fieldDef.GetType()

    # convert integer ftype to text equiv
    fldTypeS = fieldDef.GetFieldTypeName(fldType)

    #assign values to print and format
    values = (fldName, fldTypeS, fldWidth, fldPrecision)
    fmt = '%s: %s (%d.%d)'
    print(fmt % values)

#assign variables to get number of features and print
featureCount = ParcelsLayer.GetFeatureCount()
print("Out of", featureCount, "total parcels, the following are crossed by the power line.\n")

#loop features to find which parcels cross the powerline, if crosses--print address and area
for i in range(featureCount):
    parcelFeat = ParcelsLayer.GetFeature(i)
    parcelPoly = parcelFeat.GetGeometryRef()
    if parcelPoly.Crosses(line) is True:
        print("Owner's address:", parcelFeat.GetField('SITUSADDR'), "- Area of parcel:", parcelFeat.GetField('AREA'))
    else:
        continue


#set LineBuffer to buffer 250ft around powerline
lineBuffer = line.Buffer(250)

print("....Creating shapefile with parcels that are located entirely within the a 250ft powerline buffer.\n")



#create shapefile from polygons

#set filename
OutputFileName= dataDir + "parcelsBuffer.shp"

#if file with name exists, first remove
if os.path.exists(OutputFileName):
    os.remove(OutputFileName)

#try creating using driver, if unable print statement and exit
try:
   outputDS = driver.CreateDataSource(OutputFileName)
except:
   print('Could not create output file', OutputFileName)
   sys.exit(1)

#assign new layer for parcels within buffer
newLayer = outputDS.CreateLayer('parcelsBuff', geom_type=ogr.wkbPolygon)

#if unable, print statement and exit
if newLayer is None:
   print("couldn't create layer for buffer in output DS")
   sys.exit(1)

#assign new layer def and set featureID to 0
newLayerDef = newLayer.GetLayerDefn()
featureID = 0

#go through parcels and find those completely within buffer
for i in range(featureCount):
    parcelFeat = ParcelsLayer.GetFeature(i)
    parcelPoly = parcelFeat.GetGeometryRef()

    #if parcel within buffer, add parcel to parcelsBuff
    if parcelPoly.Within(lineBuffer) is True:
        try:
            newFeature = ogr.Feature(newLayerDef)  # create feature
            newFeature.SetGeometry(parcelPoly)  # add geometry
            newFeature.SetFID(featureID)  # set id
            newLayer.CreateFeature(newFeature)  # add feature to layer
        except:
            print("error adding buffer")

            newFeature.Destroy()
    else:
        continue

#print successful and close
print("\nThe file has been successfully created.")
dataSource2 = outputDS = None





