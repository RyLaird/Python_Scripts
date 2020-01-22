import sys

# try to import numpy and exit if not available
try:
    import numpy as N
except:
    sys.exit('ERROR: cannot find numpy module.')

# try to import gdal, gdalconst and exit if not available
try:
    from osgeo import gdal, gdalconst
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

# function checks Driver for capability to read, create, createcopy
def checkDriver(Driver):

    canRead = canCreate = canCreateCopy = False

    if type(Driver) == str:
        try:
            Driver = gdal.GetDriverByName(Driver)
        except:
            pass

    if Driver != None: canRead = True

    try:
        metadata  = Driver.GetMetadata()
        if metadata.get(gdal.DCAP_CREATE) == 'YES': canCreate = True
    except:
        pass

    try:
        if metadata.get(gdal.DCAP_CREATECOPY) == 'YES': canCreateCopy = True
    except:
        pass

    return (canRead, canCreate, canCreateCopy)



# set directory for files dsIn(redband) and irband
dataDir = "C:\working_directory\landsat\landsat\\"

# Open dsIn for redband and use later for GeoTransfrom and GetProjection
dsIn = gdal.Open(dataDir + 'L71026029_02920000609_B30_CLIP.tif')
#if dsIn is None:
   # raise IOError('The file could not be opened.')

# Open irband for calculation of ndvi
irband = gdal.Open(dataDir + 'L71026029_02920000609_B40_CLIP.tif')
#if irband is None:
    #raise IOError('The file could not be opened.')

testX = irband.RasterXSize
testY = irband.RasterYSize

print(testX, testY)
print(testX*testY)
# Read bans as Array
redbandArray = dsIn.ReadAsArray()
irbandArray = irband.ReadAsArray()

# set as float for use in calculations in ndvi formula
red = redbandArray.astype(N.float32)
ir = irbandArray.astype(N.float32)

# set outName for new NDVI file
outName = dataDir + "NewNDVI.tif"

# choose format and get driver
format = 'GTiff'
outDriver = gdal.GetDriverByName(format)

# set variables for use in dsOut Create
newrows = dsIn.RasterYSize
newcols = dsIn.RasterXSize
newBands = 1
newdataType = gdalconst.GDT_Float32

# make sure driver is able to create
if checkDriver(outDriver)[1]:  # if we can create a new dataset
    print("Image being created....")
    pass
else:
    print("Sorry, can’t create new datasets in this format")

# Create dsOut with proper parameters

dsOut = outDriver.Create(outName, newcols, newrows, newBands, newdataType)
# set projection using dsIn
dsOut.SetProjection(dsIn.GetProjection())

# Transform using dsIn
dsOut.SetGeoTransform(dsIn.GetGeoTransform())

# set a no data value
# dsOut.SetNoDataValue(-999.)

# set numpy to divide zero
N.seterr(invalid='ignore')

# formula for ndvi
ndvi = N.divide((ir - red), (ir + red))

# writing new ndvi file
dsOut.GetRasterBand(1).WriteArray(ndvi)

# close out
dsIn = irband = dsOut = None
print("NVDI process complete.")