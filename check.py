#!/usr/bin/python3
import sys
from importlib import import_module

filename = sys.argv[1]

try:
    module_to_check = import_module(filename)
    print(module_to_check.__doc__)
except ModuleNotFoundError:
    print("Not found")
    pass
