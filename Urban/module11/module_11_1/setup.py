import os
import shutil
import sys
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__package__))

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
os.chdir('.venv/Lib/site-packages/binance')
shutil.copy('patch/client.py', rf'{ROOT_DIR}/.venv/Lib/site-packages/binance/client.py')
shutil.copy('patch/enums.py', rf'{ROOT_DIR}/.venv/Lib/site-packages/binance/enums.py')
