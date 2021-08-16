from common import Constants
from inputoutput import Robot, ScreenshotManager
from inputoutput import find_bounding_rectangle, bgr_filter

import cv2

class Engine:

    def __init__(self, config, state):
        self.config = config;
        self.state = state

        # Get mask:
        try:
            self.mask = cv2.imread(f"img/{self.config.crosshair}.png", cv2.IMREAD_GRAYSCALE)
            self.mask = cv2.threshold(self.mask, 254, 255, cv2.THRESH_BINARY)[1]
        except FileNotFoundError:
            # TODO handle cleanly
            raise RuntimeError("Could not find mask for the specified crosshair!");
        self.aoi = find_bounding_rectangle(self.mask)
        # TODO actual logging
        print(f"[INFO] AOI: {self.aoi}")
        self.threshold = int(cv2.countNonZero(self.mask) * Constants.THRESHOLD_CONFIDENCE)
        print(f"[INFO] Threshold: {self.threshold}")

        # Configure filter:
        # todo make this actually configurable
        self.bgra_lower = [0, 0, 215, 0]
        self.bgra_upper = [25, 25, 255, 255]

        # Set up internal state:
        self.holding = False

    def run(self):
        raw = ScreenshotManager.capture(self.state, self.aoi)
        filtered = bgr_filter(raw, self.bgra_lower, self.bgra_upper)
        masked = cv2.bitwise_and(filtered, filtered, self.mask)
        if cv2.countNonZero(masked) > self.threshold:
            if not self.config.auto:
                Robot.click()
                Robot.range_sleep(Constants.MIN_CLICK_SLEEP_MS, Constants.MAX_CLICK_SLEEP_MS)
            else:
                Robot.click_hold()
                self.holding = True
        elif self.holding:
            Robot.click_release()
            self.holding = False
