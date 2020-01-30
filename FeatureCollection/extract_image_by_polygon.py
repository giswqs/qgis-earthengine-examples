import ee 
from ee_plugin import Map 

# Extract landsant image based on individual polygon
def extract_landsat(feature):
    geom = ee.Feature(feature).geometry()
    image = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
        .filterDate('2019-01-01', '2019-12-31') \
        .filterBounds(geom) \
        .median() \
        .clip(geom)
    return image

# Select the first five U.S. counties
counties = ee.FeatureCollection('TIGER/2018/Counties').toList(5)
Map.setCenter(-110, 40, 5)
Map.addLayer(ee.Image().paint(counties, 0, 2), {'palette': 'red'}, "Selected Counties")

# Extract Landsat image for each county
images = counties.map(extract_landsat)

# Add images to map
for i in range(0, 5):
    image = ee.Image(images.get(i))
    vis = {'bands': ['B5', 'B4', 'B3'], 'min': 0, 'max': 3000, 'gamma': 1.4}
    Map.addLayer(image, vis, 'Image ' + str(i+1))


