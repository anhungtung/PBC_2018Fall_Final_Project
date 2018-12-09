import logging
import argparse
from splinter import *
from visualizer import *

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)-0s] %(name)-0s >> %(message)-0s")
logger = logging.getLogger(__name__)

log_filename = datetime.datetime.now().strftime("log/tk%Y-%m-%d_%H_%M_%S.log")
console = logging.StreamHandler()
console.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

if __name__ == "__main__":
    arg_model = sys.argv[sys.argv.index("--model") + 1]

    parser = argparse.ArgumentParser(prog = 'Music_Mixer', epilog = 'Splinder Music Mixer and Pygame Dynamic GUI')
    parser.add_argument('--mixer', help = 'display mixer gui')
    parser.add_argument('--player', help = 'display mp3 player')

    args = parser.parse_args()

    if args.mixer :
        # Code Here
    elif args.player:
        # Code Here

    logger.debug(args)