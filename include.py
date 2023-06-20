import os
import importlib.util
import sys



def include(file_name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, os.path.abspath(file_name))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
