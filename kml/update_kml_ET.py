"""
Update a KML File's <name> element using
the comment value extracted from an HTML
table, stored in the <description> element.

Note, ElementTree output will create a prefix
of 'ns0' to represent the namespace. This
appears to not be parsable by QGIS, ArcDesktop,
but will work in Google Earth.
"""

from xml.etree import ElementTree
from BeautifulSoup import BeautifulSoup
import os, string, pdb

namespace = 'http://www.opengis.net/kml/2.2'
dataset = ElementTree.parse('./wwtp_testpit.kml') 
outFile = open('./wwtp_testpit_out.kml', "wb")
root = dataset.getroot()
placemarks = root.findall('{%s}Document/{%s}Folder/{%s}Placemark' % (namespace, namespace,
    namespace))

for placemark in placemarks:
    elemName = placemark.find('{%s}name' % namespace)
    print 'Original Name: ' + elemName.text 
    elemDesc = placemark.find('{%s}description' % namespace).text
    htmlDesc = BeautifulSoup(elemDesc)
    tables = htmlDesc.findAll('td')
    newName = tables[1].text
    elemName.text = newName
    print 'Comment Value: ' + newName
    print 'Updated Name: ' + placemark.find('{%s}name' % namespace).text

dataset.write(outFile)
outFile.close()

