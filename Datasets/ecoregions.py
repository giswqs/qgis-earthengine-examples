import ee 
from ee_plugin import Map 

# Load a FeatureCollection from a table dataset: 'RESOLVE' ecoregions.
ecoregions = ee.FeatureCollection('RESOLVE/ECOREGIONS/2017')

# Display as default and with a custom color.
Map.addLayer(ecoregions, {}, 'default display', False)
Map.addLayer(ecoregions, {'color': 'FF0000'}, 'colored', False)


Map.addLayer(ecoregions.draw(**{'color': '006600', 'strokeWidth': 5}), {}, 'drawn', False)


# Create an empty image into which to paint the features, cast to byte.
empty = ee.Image().byte()

# Paint all the polygon edges with the same number and 'width', display.
outline = empty.paint(**{
  'featureCollection': ecoregions,
  'color': 1,
  'width': 3
})
Map.addLayer(outline, {'palette': 'FF0000'}, 'edges')