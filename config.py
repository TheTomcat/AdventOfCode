import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPATE_FILE = "problem2.py.txt"
TEMPLATE_PATH = os.path.join(ROOT_DIR,"template",TEMPATE_FILE)
STORAGE_OBJ_FILE = 'db.pickle'
STORAGE_OBJ_PATH = os.path.join(ROOT_DIR, STORAGE_OBJ_FILE)
RUNNING_ALL = False