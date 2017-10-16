#!/usr/bin/python


import sys

from core.piclRouter import piclRouter
import core.piclLogger as piclLogger

from config import logging

piclLogger.init(logging.FILEPATH, logging.LEVEL)
piclRouter.route(sys.argv[1:2], sys.argv[2:])
