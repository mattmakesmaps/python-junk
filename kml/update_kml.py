"""
Update name element from 'Point_generic' to
value of comment field.
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
pdb.set_trace()
