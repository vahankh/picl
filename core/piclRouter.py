import logging
import argparse
import inspect
import glob
from os.path import dirname, basename, isfile
# from optparse import OptionParser
from importlib import import_module

# from core.piclController import piclController

class piclRouter(object):

    params = {}
    args = {}

    @staticmethod
    def route(request, params):
        """
        parse the request and parameters and route the action. display the generic help section when it's needed
        :param request: '{controller}/{method}' or '--help' string
        :param params: all arguments after '{controller}/{method}'
        :return: None
        """

        # no arguments or user requests for help?
        if len(request)==0 and len(params)==0 or '--help' in request:
            piclRouter.print_help()
            return

        piclRouter.params = params

        # determine controller and load it
        r_parts = request[0].split("/")
        controller = r_parts[0]
        try:
            ctrl_module = import_module("controllers.%sController" % controller)
        except ModuleNotFoundError:
            print("Controller `%s` not found" % controller)
            piclRouter.print_help()
            return

        ctrl_class = getattr(ctrl_module, "%sController" % controller)
        ctrl_object = ctrl_class()

        action = "default"
        if len(r_parts)>1:
            action = r_parts[1]

        # get the action method and check if it is defined
        try:

            action_method = getattr(ctrl_object, action)
        except:
            print("Method `%s` is not implemented in the `%s`" % (action, ctrl_module))
            piclRouter.print_help()
            return

        # parse arguments
        piclRouter.parse_args(action_method, params)

        # strategy_name = ""
        # if hasattr(ctrl_object, "strategy"):
        #     strategy_method = getattr(ctrl_object, "strategy")
        #     if callable(strategy_method):
        #         strategy_name = strategy_method(action_method, **piclRouter.args)
        #         return
        # print(strategy_name);

        if not '--help' in params:
            action_method(**piclRouter.args)

    @staticmethod
    def print_help():
        """
        Prints all controllers and public methods
        :return: None
        """

        modules = glob.glob(dirname(__file__) + "/../controllers/*Controller.py")
        modules = {basename(f)[:-3]: basename(f)[:-13] for f in modules}

        calls = []
        for module_name, controller_name in modules.items():
            ctrl_module = import_module("controllers.%s" % module_name)
            ctrl_class = getattr(ctrl_module, module_name)

            methods = inspect.getmembers(ctrl_class(), predicate=inspect.ismethod)
            methods = [f[0] for f in methods if not f[0].startswith('__')]

            for method in methods:
                if method=="default":
                    method = ""
                calls.append(("* %s/%s" % (controller_name, method)).strip("/"))

        print('\nSupported call are:')
        print('\n'.join(calls))

    @staticmethod
    def parse_args(action_method, params):
        """
        Parses all custom arguments using controller/method docstring
        :param action_method: controller action method to load docstring from
        :param params: input parameters to parse
        :return: None
        """

        # method's docstring contains method description and arguments specification in the following format
        # ""Method description

        #   Arguments:
        #   arg1 (int) - `arg1` description
        #   arg2 (str) - `arg2` description


        signatureParams = inspect.signature(action_method).parameters

        try:
            docStringLines = inspect.getdoc(action_method).splitlines()
        except AttributeError:
            return

        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description=inspect.getdoc(action_method).split("Arguments:")[0])

        types = {
            'int': int,
            'str': str,
            'bool': bool,
            'float': float
        }

        # arguments that have '--' prefix are considered optional by default.
        # to fix it we add argument group and add all required args into it
        requiredNamed = parser.add_argument_group('required named arguments')

        for name, param in signatureParams.items():
            parser_args = {}

            # does argument have default value?
            if not param.default == param.empty:
                parser_args['default'] = param.default
            else:
                parser_args['required'] = True

            for line in docStringLines:
                if name in line:
                    parts = line.split('-')
                    parser_args['help'] = '-'.join(parts[1:]).strip() # gets argument description
                    param_type_str = parts[0].split('(')[1].split(')')[0] # gets argument type in brackets

                    # if type is one of the global ones then load it from the dictionary
                    # otherwise ignore it (this part can be improved later to support custom callback types)
                    if param_type_str in types:
                        parser_args['type'] = types[param_type_str]

            # if argument doesn't have default value (required) add it to our `required` group
            if 'required' in parser_args and parser_args['required']==True:
                requiredNamed.add_argument('--%s' % name, **parser_args)
            else:
                parser.add_argument('--%s' % name, **parser_args)


        if '--help' in params:
            parser.print_help()
            return

        # do our custom controller/method defined argument parsing
        args = parser.parse_args(params)

        piclRouter.args = vars(args)