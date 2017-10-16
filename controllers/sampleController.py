import logging

from core.piclController import piclController
from core.picl import picl

from config.database import MYSQL_DB

class sampleController(piclController):

    def default(self, argument):
        """ Default Controller Action

        Arguments:
            argument (int) - Will expect --argument as command line input
            """
        logging.info("Processing CLI Request")

        mSample = picl.loader.model("Sample", MYSQL_DB)
        sSample = picl.loader.strategy("strategy1", "Sample", MYSQL_DB)

        mSample.get_filtered([])
        sSample.get_filtered([])

