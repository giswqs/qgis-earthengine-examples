import ee 
from ee_plugin import Map 

# // This helper function returns a list of new band names.
# var getNewBandNames = function(prefix) {
#   var seq = ee.List.sequence(1, bandNames.length());
#   return seq.map(function(b) {
#     return ee.String(prefix).cat(ee.Number(b).int());
#   });
# };

# def getNewBandNames(prefix):


def getPrincipalComponents(centered, scale, region):
# getPrincipalComponents = function(centered, scale, region) {
  # Collapse the bands of the image into a 1D array per pixel.
  arrays = centered.toArray()

  # Compute the covariance of the bands within the region.
  covar = arrays.reduceRegion({
    'reducer': ee.Reducer.centeredCovariance(),
    'geometry': region,
    'scale': scale,
    'maxPixels': 1e9
  })

  # Get the 'array' covariance result and cast to an array.
  # This represents the band-to-band covariance within the region.
  covarArray = ee.Array(covar.get('array'))

  # Perform an eigen analysis and slice apart the values and vectors.
  eigens = covarArray.eigen()

  # This is a P-length vector of Eigenvalues.
  eigenValues = eigens.slice(1, 0, 1)
  # This is a PxP matrix with eigenvectors in rows.
  eigenVectors = eigens.slice(1, 1)

  # Convert the array image to 2D arrays for matrix computations.
  arrayImage = arrays.toArray(1)

  # Left multiply the image array by the matrix of eigenvectors.
  principalComponents = ee.Image(eigenVectors).matrixMultiply(arrayImage)

  # Turn the square roots of the Eigenvalues into a P-band image.
  sdImage = ee.Image(eigenValues.sqrt()) \
      .arrayProject([0]).arrayFlatten([getNewBandNames('sd')])

  # Turn the PCs into a P-band image, normalized by SD.
  return principalComponents \
      .arrayProject([0]) \
      .arrayFlatten([getNewBandNames('pc')]) \
      .divide(sdImage)
# }

