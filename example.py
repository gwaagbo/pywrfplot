# -*- coding:utf-8 -*-
"""
@author: Geir Arne Waagbø
"""

import mapWRF
import xzWRF

mapWRF.mapDomains(includePMSL=True)
xzWRF.xzCloudPlot(nest=4, time=45, plotTemp=True, plotRH=False)