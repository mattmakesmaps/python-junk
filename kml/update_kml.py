"""
Update name element from 'Point_generic' to
value of comment field.
"""

from xml.etree import ElementTree
import os
import pdb
import string
from BeautifulSoup import BeautifulSoup

dataset = ElementTree.parse('/home/matt/Desktop/wwtp_testpit.kml') 
root = dataset.getroot()
placemarks = root.findall('{http://www.opengis.net/kml/2.2}Document/{http://www.opengis.net/kml/2.2}Folder/{http://www.opengis.net/kml/2.2}Placemark')

for placemark in placemarks:
    elemName = placemark.find('{http://www.opengis.net/kml/2.2}name')
    print 'Original Name: ' + elemName.text 
    description = placemark.find('{http://www.opengis.net/kml/2.2}description').text
    htmlDesc = BeautifulSoup(description)
    tables = htmlDesc.findAll('td')
    realName = tables[1].text
    elemName.__setattr__('text',realName)
    print 'Comment Value: ' + realName
    print 'Updated Name: ' + placemark.find('{http://www.opengis.net/kml/2.2}name').text
