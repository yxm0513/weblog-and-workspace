import os
path = os.path.abspath(os.path.dirname(__file__))
file = os.path.join(path, "run.py")

execfile(file)