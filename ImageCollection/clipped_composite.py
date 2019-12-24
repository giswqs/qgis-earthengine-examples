#!/usr/bin/env python
"""Composite an image collection and clip it to a boundary from a fusion table.

See also: Filtered Seasonal Composite, which filters the
collection by bounds instead.
"""

import datetime
import ee
from ee_plugin import Map


Map.setCenter(-110, 40, 5)

# Create a Landsat 7, median-pixel composite for Spring of 2000.
collection = (ee.ImageCollection('LE7_L1T')
              .filterDate(datetime.datetime(2000, 5, 1),
                          datetime.datetime(2000, 10, 31)))
image1 = collection.median()

# Clip to the output image to the California state boundary.
fc = (ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8')
      .filter(ee.Filter().eq('Name', 'Minnesota')))
image2 = image1.clipToCollection(fc)

# Select the red, green and blue bands.
image = image2.select('B4', 'B3', 'B2')
Map.addLayer(image, {'gain': [1.4, 1.4, 1.1]})
