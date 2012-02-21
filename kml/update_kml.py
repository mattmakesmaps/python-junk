"""
Update name element from 'Point_generic' to
value of comment field.
"""

import BeautifulSoup
import os, string, pdb

# BeautifulSoup
bsInFile = open('./wwtp_testpit.kml','rb')
bsDataset = BeautifulSoup.BeautifulStoneSoup(bsInFile)
bsOutFile = open('./wwtp_testpit_out_bs.kml','wb')
bsPlacemarks = bsDataset.findAll('placemark')

for placemark in bsPlacemarks:
    elemName = placemark.findChild('name')
    print 'Original Name: %s' % elemName.text
    htmlDesc = BeautifulSoup.BeautifulSoup(placemark.find('description').text)
    tables = htmlDesc.findAll('td')
    newName = tables[1].text
    print 'Comment Value: %s' % newName
    elemName.setString(newName)
    print 'Updated Name: %s' % placemark.findChild('name').text

bsOutFile.write(str(bsDataset))
bsOutFile.close()
