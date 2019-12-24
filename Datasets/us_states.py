#!/usr/bin/env python
"""Display US States.

"""

# import datetime
import ee
from ee_plugin import Map

# Map.setCenter(-110, 40, 5)
fc = ee.FeatureCollection('TIGER/2018/States')
    # .filter(ee.Filter.eq('STUSPS', 'MN'))

image = ee.Image().paint(fc, 0, 2)
Map.setCenter(-99.844, 37.649, 5)
Map.addLayer(image, {'palette': 'FF0000'}, 'TIGER/2018/States')
Map.addLayer(fc, {}, 'US States')

