You must have a working Python installation that includes the [dependencies](InstallationTips.md).

Download the code using svn or use the [download](http://code.google.com/p/pywrfplot/downloads)-tab, or grab the Python code by browsing under the source tab (look in the [trunk](http://code.google.com/p/pywrfplot/source/browse/trunk/)-folder for the latest version).

You must have output files in the nc-format from WRF available in some directory on your computer. For some plots, output files from WPS (met-files) are also useful.

To avoid endless parameter lists, most settings are defined in the module [pywrfplotParams](http://code.google.com/p/pywrfplot/source/browse/trunk/pywrfplotParams.py). You must change these settings before you can make any plots.

Make you own Python file  ([Example](http://code.google.com/p/pywrfplot/source/browse/trunk/example.py)) and use the methods in the modules. For instance:

`mapWRF.mapDomains()`

or

`mapWRF.mapWind(nest=3,time=45)`

With pywrfplot you can make [Maps](Maps.md), [SkewTPlots](SkewTPlots.md), and XzAndTzPlots.