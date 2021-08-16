import argparse
import sys

from inputoutput.KeyHook import KeyHook
from inputoutput import Robot
from engine.Engine import Engine
from engine.State import State
from engine.Config import Config
from common import *

import logging

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auto", help="Use full auto", action="store_true")
    parser.add_argument("-c", "--crosshair", type=str, help="The name of the crosshair in use",
                        default="Dot")
    parser.add_argument("-p", "--pause-key", type=str, help="The key to pause the system",
                        default=";")
    parser.add_argument("-r", "--enemy-r", type=int, help="Enemy r value",
                        default=210)
    parser.add_argument("-g", "--enemy-g", type=int, help="Enemy g value",
                        default=0)
    parser.add_argument("-b", "--enemy-b", type=int, help="Enemy b value",
                        default=0)

    run(parser)


def run(parser):

    args = parser.parse_args()

    # Build state
    state = State()
    state.unlock(State.RUNNING)

    # Start keyhooks:
    print(f"Pause key: {args.pause_key}")
    background(KeyHook(args.pause_key, State.RUNNING).listen, [state])

    # Build config
    config = Config(
        args.auto,
        args.pause_key,
        args.crosshair,
        args.enemy_r,
        args.enemy_g,
        args.enemy_b
        )

    # Initialize the engine and run it:
    engine = Engine(config, state)
    while not state.get(State.RUNNING):
        print("Disabled; sleeping...")
        Robot.long_sleep(1)
    else:
        while True:
            if not state.get(State.RUNNING):
                print("Disabled; sleeping...")
                Robot.long_sleep(1)
            else:
                engine.run()


if __name__ == "__main__":

    def debug():
        # Debug setup:
        from debug import color_picker
        from inputoutput import bgr_filter
        import cv2

        # image = cv2.imread(r"C:\Users\Eric\Desktop\tmp.png") # bad first
        image = cv2.imread("img/Dot.png")
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)

        cv2.imwrite("img/Dot.png", blackAndWhiteImage)

    # debug()

    main()