import mss, mss.tools
import time

import numpy as np

from common import Rectangle



# Take a screenshot for the specified AOI
#  aoi: a common.Rectangle
# Returns a numpy array of the screenshot
def capture(state, aoi=Rectangle(0, 0, 1920, 1080)):
    monitor = {"top": aoi.y, "left": aoi.x, "width": aoi.w, "height": aoi.h}
    state.lock("capture")
    with mss.mss() as sct:
        sct_img = sct.grab(monitor)
        data = np.array(sct_img)
    state.unlock("capture")
    return data