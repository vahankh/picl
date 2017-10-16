import logging

from importlib import import_module

class picl(object):

    # Internal class for loading models and other objects
    class loader(object):

        models = {}
        buckets = {}
        strategies = {}
        controllers = {}

        @staticmethod
        def model(model_name, db_config):

            if model_name in picl.loader.models:
                return picl.loader.models[model_name]

            try:
                ctrl_module = import_module("models.%s" % model_name)
            except ModuleNotFoundError:
                logging.error("Model `%s` not found" % model_name)
                return False

            mdl_class = getattr(ctrl_module, model_name)
            mdl_object = mdl_class(db_config)
            picl.loader.models[model_name] = mdl_object

            return mdl_object

        @staticmethod
        def strategy(strategy_name, model_name, db_config):

            if strategy_name in picl.loader.strategies:
                if model_name in picl.loader.strategies[strategy_name]:
                    return picl.loader.strategies[strategy_name][model_name]
            else:
                picl.loader.strategies[strategy_name] = {}

            try:
                ctrl_module = import_module("models.%s.%s" % (strategy_name, model_name))
            except ModuleNotFoundError:
                logging.error("Model `%s` not found for strategy `%s`" % (model_name, strategy_name))
                return False

            mdl_class = getattr(ctrl_module, model_name)
            mdl_object = mdl_class(db_config)
            picl.loader.strategies[strategy_name][model_name] = mdl_object

            return mdl_object

        @staticmethod
        def bucket(bucket_name, db_config):

            if bucket_name in picl.loader.buckets:
                return picl.loader.buckets[bucket_name]

            try:
                ctrl_module = import_module("buckets.%s" % bucket_name)
            except ModuleNotFoundError:
                logging.error("Bucket `%s` not found" % bucket_name)
                return False

            bkt_class = getattr(ctrl_module, bucket_name)
            bkt_object = bkt_class(**db_config)
            picl.loader.buckets[bucket_name] = bkt_object

            return bkt_object

        @staticmethod
        def controller(controller_name):

            if controller_name in picl.loader.controllers:
                return picl.loader.controllers[controller_name]

            try:
                ctrl_module = import_module("controllers.%sController" % controller_name.lower())
            except ModuleNotFoundError:
                logging.error("Controller `%s` not found" % controller_name)
                return False

            ctrl_class = getattr(ctrl_module, "%sController" % controller_name.lower())
            ctrl_object = ctrl_class()
            picl.loader.controllers[controller_name] = ctrl_object

            return ctrl_object

