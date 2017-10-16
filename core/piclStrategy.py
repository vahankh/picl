import logging
import inspect

from core.picl import picl

from config.database import MMS_DB

class piclStrategy(picl):
    """
    Defines strategy for model classes and their implementations

    Usage:
    1. Add decorator `@piclStrategy._strategy` before model function definition.
    2. Add strategy directory in the models folder if doesn't exist
    3. Add model and class into that directory
    """

    isp_id = None
    md_id = None

    strategies = {}

    def _strategy(fnc):
        def magic(*args, **kwargs):

            logging.debug("Looking for strategy implementations")

            """ Begin parsing arguments and looking for isp_id and md_id """
            signatureParams = inspect.signature(fnc).parameters
            i = 0
            # check positional arguments
            for name, param in signatureParams.items():
                try:
                    if name == 'isp_id':
                        piclStrategy.isp_id = args[i]
                    if name == 'md_id':
                        piclStrategy.md_id = args[i]
                    i += 1
                except IndexError:
                    break

            # check keyword arguments
            if 'isp_id' in kwargs:
                piclStrategy.isp_id = kwargs['isp_id']

            if 'md_id' in kwargs:
                piclStrategy.md_id = kwargs['md_id']
            """ End argument parsing """

            # Check if strategy has been loaded already
            if not piclStrategy.isp_id is None and not piclStrategy.md_id is None:
                key = "%d-%d" % (piclStrategy.isp_id, piclStrategy.md_id)
                if not key in piclStrategy.strategies:
                    mMd = piclStrategy.loader.model("Md", MMS_DB)
                    piclStrategy.strategies[key] = mMd.get_warming_strategy(piclStrategy.isp_id, piclStrategy.md_id)
            elif not piclStrategy.isp_id:
                key = "%d" % (piclStrategy.isp_id)
                if not key in piclStrategy.strategies:
                    mIsp = piclStrategy.loader.model("mIsp", MMS_DB)
                    piclStrategy.strategies[key] = mIsp.get_warming_strategy(piclStrategy.isp_id)

            if piclStrategy.strategies[key] is None:
                logging.debug("No strategy found. Go to default implementation")
                return fnc(*args, **kwargs)

            logging.debug("Strategy `%s` found. Check for method implemention" % piclStrategy.strategies[key])
            model_name = args[0].__class__.__name__;
            sMd = picl.loader.strategy(piclStrategy.strategies[key], model_name, MMS_DB)

            if not hasattr(sMd, fnc.__name__) or not callable(getattr(sMd, fnc.__name__)):
                logging.info("Method `%s` is not implemented in `%s` strategy. Loading default implementation"
                             % (fnc.__name__, piclStrategy.strategies[key]))
                return fnc(*args, **kwargs)

            s_method = getattr(sMd, fnc.__name__)

            args = args[1:]

            logging.debug("Implementation `%s` is found in strategy `%s`" % (fnc.__name__, piclStrategy.strategies[key]))
            return s_method(*args, **kwargs)

        return magic
