import os
import sys

"""
__file__ is the curernt file eg: tests/conftest.py
dirname(...) = tests/ folder

os.path.join(..., "..")  this gets the parent folder (GroupProject)

os.path.abspath(...) this gets the absolute path for you

sys.path - list of places that are checked



"""


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path: #Is my project folder already in the list of places Python searches for imports
    sys.path.insert(0, PROJECT_ROOT)