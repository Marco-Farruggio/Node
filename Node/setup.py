from setuptools import setup

APP = ["node.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": True,
    "packages": ["customtkinter", "requests"],
    "iconfile": "node_icon.icns",
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)