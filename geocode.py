import arcpy
import csv
import urllib2
from geopy import geocoders
from arcpy import env

# Setup File Locations
env.workspace = "J:/292A Yakama Solid Waste/GIS/Layers/ISWMP"
siteSource = "existing_sites.csv"
siteGeocoded = "existing_sites_geocoded.csv"

# Geocoding
g = geocoders.Google()
fSource = open(env.workspace + "/" + siteSource, 'rb')
fGeocoded = open(env.workspace + "/" + siteGeocoded, 'wb')
try:
    reader = csv.reader(fSource)
    writer = csv.writer(fGeocoded)
    i = 0
    for row in reader:
        if i == 0:
            writer.writerow((row[0],row[1],"lat","lng"))
            i = i+1
        try:
            place, (lat, lng) = g.geocode(row[1])
            writer.writerow((row[0],row[1],lat,lng))
            print "%s: %.5f, %.5f" % (place, lat, lng)
        except:
            pass
finally:
    fSource.close()
    fGeocoded.close()

# Making the XY Event Layer
try:
    print "Beginning XY Event Layer Creation"
    # Setup    
    in_Table = siteGeocoded
    x_coords = "lng"
    y_coords = "lat"
    out_Layer = "GeocodedSites"
    saved_Layer = env.workspace + "/" + out_Layer + ".lyr"
    # Grab ESRI PRJ from spatialreference.org
    spRef = urllib2.urlopen("http://spatialreference.org/ref/epsg/4326/prj/")
    
    # Execute Tools
    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef.read())
    arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)
    print "Finished XY Event Layer Creation"
except:
    print arcpy.GetMessages()