#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

import pyfits
import numpy as np
import matplotlib.pyplot as pl

with pyfits.open("kepler10-untrended.fits") as f:
    data = f[1].data
    time = np.array(data["TIME"])
    sap = np.array(data["SAPFLUX"])
    pdc = np.array(data["PDCFLUX"])
    flux = np.array(data["FLUX"])

pl.plot(time, sap - np.median(sap), ".k", alpha=1, ms=0.5)
inds = ~np.isnan(time)
pl.xlim(time[inds].min(), time[inds].max())
pl.ylim(-0.0035, 0.0035)
pl.xlabel("time [KBJD]")
pl.savefig("sap.png", dpi=300)

pl.clf()
pl.plot(time, pdc - np.median(pdc), ".k", alpha=0.8, ms=1)
pl.xlim(time[inds].min(), time[inds].max())
pl.ylim(-0.0035, 0.0035)
pl.xlabel("time [KBJD]")
pl.savefig("pdc1.png", dpi=300)

pl.ylim(-0.0013, 0.0013)
pl.savefig("pdc2.png", dpi=300)

pl.clf()
pl.plot(time, flux - np.median(flux), ".k", alpha=0.8, ms=1)
pl.xlim(time[inds].min(), time[inds].max())
pl.ylim(-0.0013, 0.0013)
pl.xlabel("time [KBJD]")
pl.savefig("untrend.png", dpi=300)

t1, t2 = 131.57439, 138.6781
p1, p2 = 0.8374903, 45.29404
pl.clf()
pl.plot((time - t1 + 0.5 * p1) % p1 - 0.5 * p1, flux - np.median(flux), ".k",
        alpha=1, ms=3)
pl.xlim(-0.1, 0.1)
pl.ylim(-0.0007, 0.0003)
pl.xlabel("phase")
pl.savefig("folded1.png", dpi=300)

pl.clf()
pl.plot((time - t1 + 0.5 * p1) % p1 - 0.5 * p1, pdc - np.median(pdc), ".k",
        alpha=1, ms=3)
pl.xlim(-0.1, 0.1)
pl.ylim(-0.0007, 0.0003)
pl.xlabel("phase")
pl.savefig("pdc-folded1.png", dpi=300)

pl.clf()
pl.plot((time - t2 + 0.5 * p2) % p2 - 0.5 * p2, flux - np.median(flux), ".k",
        alpha=1, ms=3)
pl.xlim(-0.5, 0.5)
pl.ylim(-0.0007, 0.0003)
pl.xlabel("phase")
pl.savefig("folded2.png", dpi=300)
