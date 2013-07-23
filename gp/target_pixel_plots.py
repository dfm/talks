#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import kplr
import numpy as np

client = kplr.API()


def plot_target(obj, ind=None, nm=None):
    if nm is not None:
        nm += "_"
    else:
        nm = ""

    # Get the data.
    pix = obj.get_target_pixel_files(fetch=False, short_cadence=False)
    lc = obj.get_light_curves(fetch=False, short_cadence=False)

    # Choose the quarter.
    if ind is None:
        ind = np.random.randint(len(pix))
    pix = pix[ind]
    lc = lc[ind]

    # Make the pixel and light curve plots.
    lc_fig = lc.plot()
    lc_fig.savefig(nm + "lc.png")
    pix_fig = pix.plot()
    pix_fig.savefig(nm + "pixels.png")

    # Plot the images.
    with pix.open() as f:
        data = f[1].data
    flux = data["flux"]
    flux = flux[np.random.randint(len(flux))]

    pix_fig.clf()
    ax = pix_fig.add_axes([0, 0, 1, 1], frameon=False)
    ax.imshow(flux, cmap="gray", interpolation="nearest")
    pix_fig.savefig(nm + "img.png")

    ax.imshow(np.log(flux), cmap="gray", interpolation="nearest")
    pix_fig.savefig(nm + "img_log.png")


if __name__ == "__main__":
    obj = client.planet("32b")
    plot_target(obj, ind=4, nm="32")

    obj = client.planet("37b")
    plot_target(obj, ind=4, nm="37")

    obj = client.planet("62b")
    plot_target(obj, ind=4, nm="62")
