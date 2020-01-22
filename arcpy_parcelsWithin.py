import os
import arcpy

# set workspace for project
arcpy.env.workspace = "C:/working_directory"

# assign variable to PowerLine file

fcLine = "PowerLine.shp"

print ('opening',fcLine,'...\n')

# retrieve length feature to use in calculation
cursorLine = arcpy.da.SearchCursor(fcLine, "SHAPE@LENGTH")

# go through each length, add up, round, and convert to miles
for f in cursorLine:
    print ("The length of the polyline is: ", round(f[0]/5280, 3), "miles\n")


# assign Parcels variable
fcParcels = "Parcels.shp"

print ('opening',fcParcels,'...\n')

# use describe to obtain properties from shapefile
desc = arcpy.Describe(fcParcels)

print('The fields are:')

# assign fields properly and get type
for field in desc.fields:
    fldName       = field.name
    fldWidth      = field.length
    fldPrecision  = field.precision
    fldTypeS      = field.type

#assign and print values
    values = (fldName,fldTypeS,fldWidth,fldPrecision)
    fmt    = '%s: %s (%d.%d)'
    print(fmt % values)



# make layer from parcels and select the parcels that cross the powerline
arcpy.MakeFeatureLayer_management(fcParcels, "parcelLyr")
arcpy.SelectLayerByLocation_management("parcelLyr", "intersect", fcLine, 0, "new_selection")

# obtain fields to print from those parcels selected using SearchCursor
parcelLyrCursor = arcpy.da.SearchCursor("parcelLyr", ["SITUSADDR", "area"])

# for each row print the address and area
for row in parcelLyrCursor:
    print ("Address: ", row[0], "Area: ", row[1])



fcBuffer = "fcBuffer.shp"

# check to see if filepath exists and remove
if os.path.exists(fcBuffer):
    os.remove(fcBuffer)

print ('finding Buffer around', fcLine, '...\n')

# apply buffer around powerline of 250 feet
arcpy.Buffer_analysis(fcLine, fcBuffer, "250 feet", "", "", "ALL")

# assign variable for final output parcelsWithin feature class
parcelsWithin = "parcelsWithin.shp"

# check if file exists and remove
if os.path.exists(parcelsWithin):
    os.remove(parcelsWithin)

print ('Creating output feature class', parcelsWithin, 'for all parcels within buffer......\n')

# select all parcels completely within the buffer and copy over to a new feature class
arcpy.SelectLayerByLocation_management("parcelLyr", "COMPLETELY_WITHIN", fcBuffer, 0, "new_selection")

arcpy.CopyFeatures_management("parcelLyr", parcelsWithin)

print ('Your file', parcelsWithin, 'has been created.')

#arcpy.SaveToLayerFile_management(parcelsWithin, "C:/working_directory/parcelsWithin.shp", "ABSOLUTE")
