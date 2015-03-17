The maps below can be produced using the methods in the module [mapWRF.py](http://code.google.com/p/pywrfplot/source/browse/trunk/mapWRF.py).

The running time is much longer for high resolution map plots. Adjust this using the variable mapResolution in [pywrfplotParams.py](http://code.google.com/p/pywrfplot/source/browse/trunk/pywrfplotParams.py).

The maps are produced to have the same projection that is used in WRF, but only the Lambert projection is currently supported. If your using another projection you can try to adjust the method `mapWRF._getMap`.

  1. A map of the outer domain showing the inner domain(s).<img src='http://pywrfplot.googlecode.com/files/domains.png' alt='Logo' />
  1. A map showing the elevation of terrain, with contour lines for surface presure and temperature.<img src='http://pywrfplot.googlecode.com/files/terrain.png' alt='Logo' />
  1. A map showing cloud coverage with cloud water content in the column.<img src='http://pywrfplot.googlecode.com/files/clouds.png' alt='Logo' />
  1. A map showing wind barbs for 10-meter wind.<img src='http://pywrfplot.googlecode.com/files/wind.png' alt='Logo' />