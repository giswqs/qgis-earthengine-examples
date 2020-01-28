# GitHub URL: https://github.com/giswqs/qgis-earthengine-examples/tree/master/Tutorials/Keiko/glad_alert.py

import ee 
from ee_plugin import Map 

# Credits to: Keiko Nomura, Senior Analyst, Space Intelligence Ltd
# Source: https://medium.com/google-earth/10-tips-for-becoming-an-earth-engine-expert-b11aad9e598b
# GEE JS: https://code.earthengine.google.com/?scriptPath=users%2Fnkeikon%2Fmedium%3Afire_australia 

geometry = ee.Geometry.Polygon(
        [[[153.11338711694282, -28.12778417421283],
          [153.11338711694282, -28.189835226562256],
          [153.18943310693305, -28.189835226562256],
          [153.18943310693305, -28.12778417421283]]])
Map.centerObject(ee.FeatureCollection(geometry), 14)

imageDec = ee.Image('COPERNICUS/S2_SR/20191202T235239_20191202T235239_T56JNP')
Map.addLayer(imageDec, {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 1800
}, 'True colours (Dec 2019)')
Map.addLayer(imageDec, {
  'bands': ['B3', 'B3', 'B3'],
  'min': 0,
  'max': 1800
}, 'grey')

# GLAD Alert (tree loss alert) from the University of Maryland
UMD = ee.ImageCollection('projects/glad/alert/UpdResult')
print(UMD)

# conf19 is 2019 alert 3 means multiple alerts
ASIAalert = ee.Image('projects/glad/alert/UpdResult/01_01_ASIA') \
  .select(['conf19']).eq(3)

# Turn loss pixels into True colours and increase the green strength ('before' image)
imageLoss = imageDec.multiply(ASIAalert)
imageLoss_vis = imageLoss.selfMask().visualize(**{
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 1800
})
Map.addLayer(imageLoss_vis, {
  'gamma': 0.6
}, '2019 loss alert pixels in True colours')

# It is still hard to see the loss area. You can circle them in red
# Scale the results in nominal value based on to the dataset's projection to display on the map
# Reprojecting with a specified scale ensures that pixel area does not change with zoom
buffered = ASIAalert.focal_max(50, 'circle', 'meters', 1)
bufferOnly = ASIAalert.add(buffered).eq(1)
prj = ASIAalert.projection()
scale = prj.nominalScale()
bufferScaled = bufferOnly.selfMask().reproject(prj.atScale(scale))
Map.addLayer(bufferScaled, {
  'palette': 'red'
}, 'highlight the loss alert pixels')

# Create a grey background for mosaic
noAlert = imageDec.multiply(ASIAalert.eq(0))
grey = noAlert.multiply(bufferScaled.unmask().eq(0))

# Export the image
imageMosaic = ee.ImageCollection([
  imageLoss_vis.visualize(**{
    'gamma': 0.6
  }),
  bufferScaled.visualize(**{
    'palette': 'red'
  }),
  grey.selfMask().visualize(**{
    'bands': ['B3', 'B3', 'B3'],
    'min': 0,
    'max': 1800
  })
]).mosaic()

#Map.addLayer(imageMosaic, {}, 'export')

# Export.image.toDrive({
#   'image': imageMosaic,
#   description: 'Alert',
#   'region': geometry,
#   crs: 'EPSG:3857',
#   'scale': 10
# })
