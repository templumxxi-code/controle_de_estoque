import os
import runpy
import sys

ROOT_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

os.chdir(FRONTEND_DIR)
runpy.run_path(os.path.join(FRONTEND_DIR, "app.py"), run_name="__main__")
