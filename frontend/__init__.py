# Defines directory as package, to allow importing files
import os
import sys

# Refers to paths regardless of the script location. 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
