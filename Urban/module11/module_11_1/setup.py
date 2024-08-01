import os
import shutil
import sys
import subprocess
import time

ROOT_DIR = sys.path[1]

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
while not os.path.exists(rf'{ROOT_DIR}/.venv/Lib/site-packages/binance'):
    time.sleep(0.5)
shutil.copy('patch/client.py', rf'{ROOT_DIR}/.venv/Lib/site-packages/binance/client.py')
shutil.copy('patch/enums.py', rf'{ROOT_DIR}/.venv/Lib/site-packages/binance/enums.py')
print("Done")
