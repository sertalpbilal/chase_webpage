#!/usr/bin/python3

from flask_frozen import Freezer
from app import app
import shutil

def freeze_all():
    freezer = Freezer(app, with_static_files=True)
    freezer.freeze()
    shutil.copytree(src="static", dst="build/static", dirs_exist_ok=True)

if __name__ == "__main__":
    freeze_all()
