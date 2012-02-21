"""
Update name element from 'Point_generic' to
value of comment field.

TODO: Create generator function
"""

import BeautifulSoup
import os, string, pdb

# BeautifulSoup
bsInFile = open('./wwtp_testpit.kml','rb')
bsDataset = BeautifulSoup.BeautifulStoneSoup(bsInFile)
bsOutFile = open('./wwtp_testpit_out_bs.kml','wb')
bsPlacemarks = bsDataset.findAll('placemark')

# Beautiful Soup converts all tags to lower case
# Which causes errors in ArcGIS, QGIS, Google Earth
tags = {'document': 'Document', 'style':'Style',
        'icon':'Icon', 'iconstyle':'IconStyle',
        'folder':'Folder', 'placemark':'Placemark',
        'styleurl':'styleUrl','point':'Point',
        'altitudemode':'altitudeMode'}

# Loop through individual placemarks.
for placemark in bsPlacemarks:
    elemName = placemark.findChild('name')
    print 'Original Name: %s' % elemName.text
    htmlDesc = BeautifulSoup.BeautifulSoup(placemark.find('description').text)
    tables = htmlDesc.findAll('td')
    newName = tables[1].text
    print 'Comment Value: %s' % newName
    elemName.setString(newName)
    print 'Updated Name: %s' % placemark.findChild('name').text
    # Replace Entity-Encoded HTML
    placemark.description.setString(htmlDesc)

# Update casing on tags
for key, value in tags.items():
    updateItems = bsDataset.findAll(key)
    for item in updateItems:
        item.name = value

# Write results
bsOutFile.write(str(bsDataset))
bsOutFile.close()
