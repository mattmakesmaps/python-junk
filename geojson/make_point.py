"""
Test the creation of a point using the s. gillies reference implementation
geojson package.
"""
import geojson
from shapely.geometry import shape, asShape

p = geojson.Point([0.0,1.0])
p1 = geojson.Point([2.0,4.0])
print dir(p)
print p
print p.__geo_interface__

f = geojson.Feature(id=1,geometry=p,properties={'name':'Matt Point', 'place':'classroom'})
print f
f1 = geojson.Feature(id=2,geometry=p1,properties={'name':'Second Point', 'place':'Square'})

fc = geojson.FeatureCollection(features=[f,f1])

# Passing arbitrary strings as features is valid.
fcWonky = geojson.FeatureCollection(features=['blah', 'fleh'])
print fcWonky

print fc
print fc.__geo_interface__

print shape(p).buffer(1.0).area
print asShape(f.geometry).buffer(2.0).area
print shape(f.geometry).buffer(2.0).area

print geojson.dumps(p)
print geojson.dumps(f)
print geojson.dumps(fc)

for feat in fc.features:
    print feat.properties['name']
    feat.properties['buffSize'] = asShape(feat.geometry).buffer(2.0).area
    print feat.properties['buffSize']

print geojson.dumps(fc)
