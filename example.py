# -*- coding:utf-8 -*-
"""
@author Geir Arne Waagbø
@see http://code.google.com/p/pywrfplot/
"""

import mapWRF
import xzWRF
import tzWRF
import skewT

mapWRF.mapDomains(includePMSL=True)
xzWRF.xzCloudPlot(nest=4, time=45, plotTemp=True, plotRH=False)
skewT.skewTPlot(nest=4, time=45)
tzWRF.tzCloudPlot(nest=4)
