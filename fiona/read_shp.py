__author__ = 'matt'
__date__ = '3/17/13'
"""
Read a shapefile, Export Contents Into New Projection.
Trying out this sweet projection:
http://www.spatialreference.org/ref/epsg/4179/

+proj=longlat +ellps=krass +towgs84=33.4,-146.6,-76.3,-0.359,-0.053,0.844,-0.84 +no_defs

See: https://github.com/Toblerity/Fiona/blob/master/src/fiona/crs.py
"""
from fiona import collection

with collection('Data/QGIS_Area.shp', 'r') as inSHP:
    outSchema = inSHP.schema.copy()

    outCRS = {'proj': 'longlat', 'ellps': 'krass', 'towgs84':'33.4,-146.6,-76.3,-0.359,-0.053,0.844,-0.84', 'no_defs':True}
    with collection('Data/output/reproj.shp', 'w', crs=outCRS,
                    driver='ESRI Shapefile', schema=outSchema) as out:
        for row in inSHP:
            out.write(row)