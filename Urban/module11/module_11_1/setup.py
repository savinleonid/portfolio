import os
import sys
import subprocess
# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
os.chdir('.venv/Lib/site-packages/binance')
os.replace('patch/client.py', '.venv/Lib/site-packages/binance/client.py')
os.replace('patch/enums.py', '.venv/Lib/site-packages/binance/enums.py')
