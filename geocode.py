#!/usr/bin/python

#import arcpy
import time
import csv
import urllib2
from geopy import geocoders
#from arcpy import env

# Setup File Locations
workspace = "/home/matt/Projects/python-junk/data"
siteSource = "landfills.csv"
siteGeocoded = "landfills_geocoded.csv"

# Geocoding
g = geocoders.Google()
fSource = open(workspace + "/" + siteSource, 'rb')
fGeocoded = open(workspace + "/" + siteGeocoded, 'wb')

start = time.time()
try:
    reader = csv.reader(fSource)
    writer = csv.writer(fGeocoded)
    i = 0
    for row in reader:
        # Write column names to output file
        if i == 0:
            writer.writerow((row[0],row[1],"lat","lng"))
            i = i+1
        try:
            # concatenate (if necessary) columns required to make an address
            place, (lat, lng) = g.geocode(str(row[3] + " " + row[4] + " " + row[5] + " " + row[6]))
            writer.writerow((row[0],row[1],lat,lng))
            print "%s: %.5f, %.5f" % (place, lat, lng)
        except:
            pass
finally:
    fSource.close()
    fGeocoded.close()

# Making the XY Event Layer
"""
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
"""
print "elapsed time: %s" % (time.time() - start)
