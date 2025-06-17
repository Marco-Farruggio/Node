@echo off
cd "%~dp0"
python -m PyInstaller --onefile --noconsole --icon=node_icon.ico --add-data "node_icon.ico;." --add-data "edit_icon.png;." node.py
pause